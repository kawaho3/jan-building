#!/usr/bin/env python3
"""Download and verify pinned official Jan assets for a CPU-only capability probe."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

GIB = 1024**3
APP_NAME = 'Jan_0.8.8_amd64.AppImage'
APP_URL = 'https://github.com/janhq/jan/releases/download/v0.8.8/'+APP_NAME
APP_BYTES = 712755704
APP_SHA = 'ef98314c0230e3066235fd195ff1ffdf652b85b264bbd9ddf337f99d077c9159'
MODEL_NAME = 'Jan-code-4b-Q4_K_M.gguf'
MODEL_REVISION = '76682f4d57a07a09e7bdaf11eb380dba823e0418'
MODEL_URL = 'https://huggingface.co/janhq/Jan-code-4b-gguf/resolve/'+MODEL_REVISION+'/'+MODEL_NAME
MODEL_BYTES = 2716066656
MODEL_SHA = '6f9bcb1fdced9494fc477af6ca7e6c0e203540da5343d370eb89c1391b3644e0'
WORKER_RELATIVE = Path('squashfs-root/usr/lib/Jan/resources/bin/jan-llama-worker')


def verify_asset(path: Path, expected_bytes: int, expected_sha: str) -> str:
    if path.stat().st_size != expected_bytes:
        raise ValueError(f'{path.name}: unexpected size {path.stat().st_size}; expected {expected_bytes}')
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream,'sha256').hexdigest()
    if actual != expected_sha:
        raise ValueError(f'{path.name}: SHA256 mismatch ({actual})')
    return actual


def get_asset(destination: Path, url: str, expected_bytes: int, expected_sha: str,
              reuse: Path | None = None) -> Path:
    if reuse is not None:
        path = reuse.resolve(strict=True)
        verify_asset(path,expected_bytes,expected_sha)
        print(f'Verified existing asset: {path.name}',flush=True)
        return path
    if destination.exists():
        verify_asset(destination,expected_bytes,expected_sha)
        print(f'Verified already downloaded asset: {destination.name}',flush=True)
        return destination
    destination.parent.mkdir(parents=True,exist_ok=True)
    part = destination.with_suffix(destination.suffix+'.part')
    print(f'Downloading pinned asset: {destination.name} ({expected_bytes} bytes)',flush=True)
    subprocess.run(['curl','--fail','--location','--silent','--show-error',
                    '--retry','3','--retry-delay','2','--connect-timeout','30',
                    '--max-time','900','--continue-at','-',
                    '--output',str(part),url],check=True)
    verify_asset(part,expected_bytes,expected_sha)
    part.replace(destination)
    print(f'Verified download: {destination.name}',flush=True)
    return destination


def disk_report(path: Path) -> dict:
    usage=shutil.disk_usage(path)
    return {'path':str(path),'total_bytes':usage.total,'used_bytes':usage.used,
            'free_bytes':usage.free,'free_gib':round(usage.free/GIB,3)}


def bootstrap(root: Path, min_free_gib: float, reuse_appimage: Path | None,
              reuse_model: Path | None, paths_json: Path | None) -> dict:
    root.mkdir(parents=True,exist_ok=True)
    root=root.resolve()
    before=disk_report(root)
    print('Disk before bootstrap: '+json.dumps(before),flush=True)
    if before['free_bytes'] < min_free_gib*GIB:
        raise RuntimeError(f'Need at least {min_free_gib:g} GiB free before bootstrap; have {before["free_gib"]:.3f} GiB. No download started.')
    if shutil.which('curl') is None:
        raise RuntimeError('curl is required; no packages will be installed automatically')
    app=get_asset(root/'downloads'/APP_NAME,APP_URL,APP_BYTES,APP_SHA,reuse_appimage)
    model=get_asset(root/'models'/MODEL_NAME,MODEL_URL,MODEL_BYTES,MODEL_SHA,reuse_model)
    application=root/'application'
    application.mkdir(exist_ok=True)
    worker=application/WORKER_RELATIVE
    marker=application/'verified-appimage-sha256.txt'
    if not (worker.is_file() and marker.is_file() and marker.read_text().strip()==APP_SHA):
        if worker.exists():
            raise RuntimeError('Existing extraction has no matching checksum marker; choose a fresh bootstrap root')
        if reuse_appimage is None:
            app.chmod(app.stat().st_mode|0o100)
        elif not os.access(app,os.X_OK):
            raise RuntimeError('Reused AppImage must already be executable; reuse never changes its permissions')
        extraction_log=application/'extraction.log'
        with extraction_log.open('w') as log:
            subprocess.run([str(app),'--appimage-extract'],cwd=application,
                           stdout=log,stderr=subprocess.STDOUT,check=True)
        if not worker.is_file():
            raise RuntimeError('Verified AppImage did not provide the expected Jan worker')
        marker.write_text(APP_SHA+'\n')
    result={'created_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
            'environment':{'cpu_logical':os.cpu_count(),
                           'memory_total_bytes':os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES'),
                           'gpu_device_present':Path('/dev/nvidia0').exists(),
                           'platform':sys.platform},
            'model':str(model),'worker':str(worker),'appimage':str(app),
            'app_version':'0.8.8','app_sha256':APP_SHA,
            'model_revision':MODEL_REVISION,'model_sha256':MODEL_SHA,
            'model_bytes':MODEL_BYTES,'appimage_bytes':APP_BYTES,
            'disk_before':before,'disk_after':disk_report(root),
            'gpu_required':False,'python_dependencies':'standard library only'}
    destination=paths_json or root/'paths.json'
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print('Bootstrap complete: '+json.dumps(result),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True,help='Dedicated writable runtime directory; do not commit it')
    parser.add_argument('--min-free-gib',type=float,default=8.0,help='Minimum free disk before any download (default: 8)')
    parser.add_argument('--reuse-appimage',type=Path,help='Verify and reuse an existing official AppImage')
    parser.add_argument('--reuse-model',type=Path,help='Verify and reuse an existing model without copying')
    parser.add_argument('--paths-json',type=Path,help='Small bootstrap metadata destination')
    args=parser.parse_args()
    if args.min_free_gib<0: parser.error('--min-free-gib must be nonnegative')
    if sys.version_info<(3,11): parser.error('Python 3.11+ is required')
    bootstrap(args.root,args.min_free_gib,args.reuse_appimage,args.reuse_model,args.paths_json)


if __name__=='__main__':
    main()
