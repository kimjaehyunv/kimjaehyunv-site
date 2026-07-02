#!/usr/bin/env python3
"""Build gallery.json from slides.txt and optimize referenced JPG images."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_optimize_spec = importlib.util.spec_from_file_location(
    "optimize_images",
    ROOT / "scripts" / "optimize-images.py",
)
if _optimize_spec is None or _optimize_spec.loader is None:
    raise ImportError("Could not load scripts/optimize-images.py")
optimize_images = importlib.util.module_from_spec(_optimize_spec)
_optimize_spec.loader.exec_module(optimize_images)

find_unreferenced_jpgs = optimize_images.find_unreferenced_jpgs
optimize_gallery_images = optimize_images.optimize_gallery_images
write_report = optimize_images.write_report
ensure_original = optimize_images.ensure_original
collect_referenced_filenames = optimize_images.collect_referenced_filenames

WORK_DIR = ROOT / "images" / "work"
JAEHYUN_DIR = ROOT / "images" / "jaehyun"
WORK_SLIDES_TXT = WORK_DIR / "slides.txt"
JAEHYUN_SLIDES_TXT = JAEHYUN_DIR / "slides.txt"
WORK_GALLERY = WORK_DIR / "gallery.json"
JAEHYUN_GALLERY = JAEHYUN_DIR / "gallery.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"}

WORK_KEYWORDS = {
    "spread": "work-spread",
    "spread-lower": "work-spread-lower",
    "spread-quad": "work-spread-quad",
}

JAEHYUN_VARIANT_KEYWORDS = {
    "opening",
    "closing",
    "reduced",
    "reduced-forty",
    "small",
    "lower-left",
}

JAEHYUN_LAYOUT_KEYWORDS = {
    "contact": "contact-sheet",
    "pair": "pair-spaced",
}


def parse_slides_txt(path: Path) -> list[tuple[str | None, list[str], int]]:
    """Return list of (keyword, files, line_number)."""
    entries: list[tuple[str | None, list[str], int]] = []

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        keyword: str | None = None
        content = line

        bracket_match = re.match(r"^\[([^\]]+)\]\s*(.*)$", line)
        if bracket_match:
            keyword = bracket_match.group(1).strip().lower()
            content = bracket_match.group(2).strip()

        if not content:
            print(f"Warning: {path}:{line_number} has a keyword but no files — skipped.")
            continue

        files = [part.strip() for part in re.split(r"\s*\+\s*", content) if part.strip()]
        if not files:
            print(f"Warning: {path}:{line_number} has no filenames — skipped.")
            continue

        entries.append((keyword, files, line_number))

    return entries


def image_exists(image_dir: Path, filename: str) -> bool:
    if optimize_images.resolve_original_path(image_dir, filename):
        return True
    if (image_dir / filename).is_file():
        return True
    stem = Path(filename).stem
    for ext in IMAGE_EXTENSIONS:
        if (image_dir / f"{stem}{ext}").is_file():
            return True
    return False


def build_work_gallery(entries: list[tuple[str | None, list[str], int]]) -> list[dict]:
    gallery: list[dict] = []

    for keyword, files, line_number in entries:
        if keyword is None:
            if len(files) != 1:
                print(
                    f"Warning: {WORK_SLIDES_TXT}:{line_number} "
                    f"multiple files without a keyword — treating as single slide with first file only."
                )
            gallery.append({"type": "single", "files": [files[0]]})
            continue

        slide_type = WORK_KEYWORDS.get(keyword)
        if slide_type is None:
            raise ValueError(
                f"{WORK_SLIDES_TXT}:{line_number} unknown keyword [{keyword}]. "
                f"Use: {', '.join(WORK_KEYWORDS)}"
            )

        gallery.append({"type": slide_type, "files": files})

    return gallery


def build_jaehyun_gallery(entries: list[tuple[str | None, list[str], int]]) -> list[dict]:
    gallery: list[dict] = []

    for keyword, files, line_number in entries:
        if keyword is None:
            if len(files) == 1:
                gallery.append({"type": "single", "files": files})
                continue

            if len(files) == 2:
                gallery.append({"type": "pair-spaced", "files": files})
                continue

            if len(files) == 4:
                gallery.append({"type": "contact-sheet", "files": files})
                continue

            raise ValueError(
                f"{JAEHYUN_SLIDES_TXT}:{line_number} "
                f"{len(files)} files without a keyword — add [contact], [pair], or use one file per line."
            )

        if keyword in JAEHYUN_VARIANT_KEYWORDS:
            if len(files) != 1:
                raise ValueError(
                    f"{JAEHYUN_SLIDES_TXT}:{line_number} [{keyword}] expects exactly one file."
                )
            gallery.append({"type": "single", "files": files, "variant": keyword})
            continue

        slide_type = JAEHYUN_LAYOUT_KEYWORDS.get(keyword)
        if slide_type is None:
            raise ValueError(
                f"{JAEHYUN_SLIDES_TXT}:{line_number} unknown keyword [{keyword}]. "
                f"Use: {', '.join(sorted(JAEHYUN_VARIANT_KEYWORDS | set(JAEHYUN_LAYOUT_KEYWORDS)))}"
            )

        gallery.append({"type": slide_type, "files": files})

    return gallery


def validate_files(image_dir: Path, gallery: list[dict], label: str) -> None:
    for slide in gallery:
        for filename in slide["files"]:
            if not image_exists(image_dir, filename):
                print(f"Warning: {label} image not found: {image_dir / filename}")


def write_gallery(path: Path, gallery: list[dict]) -> None:
    path.write_text(json.dumps(gallery, indent=2) + "\n", encoding="utf-8")


def report_new_jpgs(image_dir: Path, gallery: list[dict], label: str) -> None:
    referenced = [filename for slide in gallery for filename in slide["files"]]
    unreferenced = find_unreferenced_jpgs(image_dir, referenced)
    if unreferenced:
        print(f"Note: {label} folder has JPG files not listed in slides.txt:")
        for name in unreferenced:
            print(f"  - {name}")
        print("  Add them to slides.txt to include them on the site.")


def prepare_originals(image_dir: Path, gallery: list[dict]) -> None:
    for filename in collect_referenced_filenames(gallery):
        ensure_original(image_dir, filename)


def main() -> int:
    if not WORK_SLIDES_TXT.is_file():
        print(f"Error: missing {WORK_SLIDES_TXT}", file=sys.stderr)
        return 1
    if not JAEHYUN_SLIDES_TXT.is_file():
        print(f"Error: missing {JAEHYUN_SLIDES_TXT}", file=sys.stderr)
        return 1

    try:
        work_entries = parse_slides_txt(WORK_SLIDES_TXT)
        jaehyun_entries = parse_slides_txt(JAEHYUN_SLIDES_TXT)

        work_gallery = build_work_gallery(work_entries)
        jaehyun_gallery = build_jaehyun_gallery(jaehyun_entries)

        prepare_originals(WORK_DIR, work_gallery)
        prepare_originals(JAEHYUN_DIR, jaehyun_gallery)

        validate_files(WORK_DIR, work_gallery, "WORK")
        validate_files(JAEHYUN_DIR, jaehyun_gallery, "JAEHYUN")

        report_new_jpgs(WORK_DIR, work_gallery, "WORK")
        report_new_jpgs(JAEHYUN_DIR, jaehyun_gallery, "JAEHYUN")

        print("")
        print("Step 1/3: Building web JPG + WebP from originals/ (originals are never modified)...")
        optimize_results = optimize_gallery_images(
            WORK_DIR,
            JAEHYUN_DIR,
            work_gallery,
            jaehyun_gallery,
        )
        write_report(optimize_results)
        if optimize_results:
            print(f"Optimized {len(optimize_results)} image(s).")
        else:
            print("All web JPG/WebP files are already up to date.")

        print("")
        print("Step 2/3: Building gallery.json...")
        write_gallery(WORK_GALLERY, work_gallery)
        write_gallery(JAEHYUN_GALLERY, jaehyun_gallery)

        print(f"Wrote {len(work_gallery)} slides → {WORK_GALLERY.relative_to(ROOT)}")
        print(f"Wrote {len(jaehyun_gallery)} slides → {JAEHYUN_GALLERY.relative_to(ROOT)}")
        return 0
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except ImportError as error:
        print(
            "Error: Pillow is required. Install with: python3 -m pip install Pillow",
            file=sys.stderr,
        )
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
