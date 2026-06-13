#!/usr/bin/env python3
import json
import re
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent.parent / "images" / "work"
MANIFEST = WORK_DIR / "manifest.json"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def sort_key(name: str):
    match = re.match(r"(\d+)", name)
    return int(match.group(1)) if match else name


files = sorted(
    [
        path.name
        for path in WORK_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in EXTENSIONS
    ],
    key=sort_key,
)

MANIFEST.write_text(json.dumps(files, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(files)} images to {MANIFEST}")
