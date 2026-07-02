#!/usr/bin/env python3
"""Deprecated: use scripts/build-gallery.py instead."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = ROOT / "scripts" / "build-gallery.py"

print("Note: generate-work-manifest.py is deprecated. Using build-gallery.py instead.")
raise SystemExit(subprocess.call([sys.executable, str(BUILD_SCRIPT)]))
