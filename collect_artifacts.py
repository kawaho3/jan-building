#!/usr/bin/env python3
"""Stage only small probe metrics and logs; never stage models or weight backups."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shutil

ALLOWED_EXTENSIONS={'.json','.jsonl','.log','.txt','.md','.csv'}
FORBIDDEN_SUFFIXES={'.gguf','.appimage','.bin','.f32','.safetensors','.pt','.pth','.backup','.bak'}
FORBIDDEN_PARTS={'models','weights','backups','downloads','application'}
FILE_LIMIT=2*1024**2
TOTAL_LIMIT=25*1024**2


def collect(source: Path,destination: Path) -> dict:
    source=source.resolve(strict=True)
    destination=destination.resolve()
    if destination==source or source in destination.parents:
        raise ValueError('Artifact destination must be outside the source tree')
    destination.mkdir(parents=True,exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Artifact destination must be empty')
    copied=[]
    skipped=[]
    total=0
    for path in sorted(source.rglob('*')):
        if not path.is_file(): continue
        rel=path.relative_to(source)
        reason=None
        if path.is_symlink(): reason='symbolic link'
        elif not path.resolve().is_relative_to(source): reason='resolved outside artifact source'
        elif any(p.lower() in FORBIDDEN_PARTS for p in rel.parts): reason='runtime/weight directory'
        elif any(s.lower() in FORBIDDEN_SUFFIXES for s in path.suffixes): reason='model or binary weight suffix'
        elif path.suffix.lower() not in ALLOWED_EXTENSIONS: reason='extension not allowed'
        elif 'backup' in path.name.lower() or 'tensor-original' in path.name.lower(): reason='weight backup name'
        size=path.stat().st_size
        if reason is None and size>FILE_LIMIT: reason='file exceeds 2 MiB'
        if reason is None and total+size>TOTAL_LIMIT: reason='total would exceed 25 MiB'
        if reason:
            skipped.append({'path':str(rel),'bytes':size,'reason':reason})
            continue
        target=destination/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
        copied.append({'path':str(rel),'bytes':size})
        total+=size
    report={'copied':copied,'skipped':skipped,'total_bytes':total,
            'file_limit_bytes':FILE_LIMIT,'total_limit_bytes':TOTAL_LIMIT}
    (destination/'artifact-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--destination',type=Path,required=True)
    args=parser.parse_args()
    collect(args.source,args.destination)
