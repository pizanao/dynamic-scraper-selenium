import csv
import json
from pathlib import Path

from pydantic import BaseModel


def ensure_dir(p):
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def dump_json(path, rows):
    payload = [r.model_dump(mode='json') if isinstance(r, BaseModel) else r for r in rows]
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')


def dump_csv(path, rows):
    payload = [r.model_dump(mode='json') if isinstance(r, BaseModel) else r for r in rows]
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        if not payload:
            return
        wr = csv.DictWriter(f, fieldnames=list(payload[0].keys()))
        wr.writeheader()
        wr.writerows(payload)
