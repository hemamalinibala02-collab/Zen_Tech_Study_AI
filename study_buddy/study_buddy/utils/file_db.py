"""Tiny JSON file 'database'. Auto-creates files & folders."""
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UPLOADS = ROOT / "uploads"
EXPORTS = ROOT / "exports"

FILES = {
    "users": DATA / "users.json",
    "tasks": DATA / "tasks.json",
    "notes": DATA / "notes.json",
    "quiz_history": DATA / "quiz_history.json",
    "revision": DATA / "revision.json",
    "settings": DATA / "settings.json",
}

DEFAULTS = {
    "users": [], "tasks": [], "notes": [],
    "quiz_history": [], "revision": [], "settings": {},
}


def ensure_storage():
    for p in (DATA, UPLOADS, EXPORTS):
        p.mkdir(parents=True, exist_ok=True)
    for key, path in FILES.items():
        if not path.exists():
            path.write_text(json.dumps(DEFAULTS[key], indent=2))


def load(key):
    ensure_storage()
    try:
        return json.loads(FILES[key].read_text() or "null") or DEFAULTS[key]
    except Exception:
        return DEFAULTS[key]


def save(key, data):
    ensure_storage()
    FILES[key].write_text(json.dumps(data, indent=2, default=str))


def next_id(items):
    return (max([i.get("id", 0) for i in items], default=0) + 1) if items else 1
