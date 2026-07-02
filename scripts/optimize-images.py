#!/usr/bin/env python3
"""Resize and re-encode site images for delivery optimization."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ORIGINALS_DIRNAME = "originals"
JPG_QUALITY = 88
WEBP_QUALITY = 86
OPTIMIZE_PROFILE = f"jpeg{JPG_QUALITY}-webp{WEBP_QUALITY}-originals-v1"

DESKTOP = (1440, 900)
MOBILE = (390, 844)

JAEHYUN_VARIANTS = {
    "01.jpg": "opening",
    "02.jpg": "single",
    "03.jpg": "single",
    "04.jpg": "single",
    "05.jpg": "single",
    "06.JPG": "single",
    "07.JPG": "single",
    "08.JPG": "single",
    "09.jpg": "reduced-forty",
    "10.JPG": "single",
    "11.JPG": "single",
    "12.JPG": "single",
    "13.JPG": "single",
    "14.JPG": "single",
    "15.jpg": "single",
    "16.JPG": "lower-left",
    "17.JPG": "single",
    "18.jpg": "single",
    "19.jpg": "contact",
    "20.jpg": "contact",
    "21.jpg": "contact",
    "22.jpg": "contact",
    "23.jpg": "single",
    "24.jpg": "single",
    "25.jpg": "single",
    "26.jpg": "pair",
    "27.jpg": "pair",
    "28.jpg": "reduced",
    "29.JPG": "single",
    "30.jpg": "small",
    "31.jpg": "closing",
}

WORK_SPREAD = {
    "06.jpg",
    "07.jpg",
    "08.jpg",
    "09.jpg",
    "10.jpg",
    "11.jpg",
    "20.jpg",
    "21.jpg",
    "22.jpg",
    "23.jpg",
}

WORK_SPREAD_TYPES = {"work-spread", "work-spread-lower", "work-spread-quad"}

# CSS caps: (landscape_w_vw, landscape_h_vh, portrait_w_vw, portrait_h_vh)
VARIANT_CAPS = {
    "opening": (76.5, 76.5, 81.6, 81.6),
    "single": (75.0, 75.0, 80.0, 80.0),
    "lower-left": (30.0, 30.0, 32.0, 32.0),
    "reduced": (60.0, 60.0, 64.0, 64.0),
    "reduced-forty": (36.0, 36.0, 38.0, 38.0),
    "small": (38.0, 52.0, 41.0, 55.0),
    "closing": (92.0, 92.0, 97.0, 97.0),
    "pair": (18.69, 35.23, 18.69, 35.23),
}


def originals_dir(image_dir: Path) -> Path:
    return image_dir / ORIGINALS_DIRNAME


def profile_stamp_path(image_dir: Path) -> Path:
    return image_dir / ".optimize-profile"


def display_box(variant: str, portrait: bool) -> tuple[int, int]:
    if variant == "info":
        desktop_w = 320 * 0.765
        mobile_w = MOBILE[0] * 0.44
        max_w = max(desktop_w, mobile_w)
        max_h = max_w * (3308 / 1210)
        return int(max_w * 2), int(max_h * 2)

    if variant == "contact":
        desktop_h = DESKTOP[1] * 0.24
        mobile_h = (MOBILE[1] - 126) / 2
        mobile_w = (MOBILE[0] - 50) / 2
        desktop_w = DESKTOP[0] * 0.45
        max_w = max(desktop_w, mobile_w)
        max_h = max(desktop_h, mobile_h)
        return int(max_w * 2), int(max_h * 2)

    if variant == "work-spread":
        desktop_h = DESKTOP[1] * 0.345
        mobile_h = (MOBILE[1] - 126) / 2
        mobile_w = (MOBILE[0] - 50) / 2
        desktop_w = DESKTOP[0] * 0.45
        max_w = max(desktop_w, mobile_w)
        max_h = max(desktop_h, mobile_h)
        return int(max_w * 2), int(max_h * 2)

    lw, lh, pw, ph = VARIANT_CAPS[variant]
    w_vw, h_vh = (pw, ph) if portrait else (lw, lh)

    max_w = max(DESKTOP[0] * w_vw / 100, MOBILE[0] * w_vw / 100)
    max_h = max(DESKTOP[1] * h_vh / 100, MOBILE[1] * h_vh / 100)

    mobile_landscape = (MOBILE[0] * 0.96, MOBILE[1] * 0.62)
    mobile_portrait = (MOBILE[0] * 0.82, MOBILE[1] * 0.78)
    if portrait:
        max_w = max(max_w, mobile_portrait[0])
        max_h = max(max_h, mobile_portrait[1])
    else:
        max_w = max(max_w, mobile_landscape[0])
        max_h = max(max_h, mobile_landscape[1])

    return int(max_w * 2), int(max_h * 2)


def fit_within(image: Image.Image, max_w: int, max_h: int) -> Image.Image:
    width, height = image.size
    scale = min(max_w / width, max_h / height, 1.0)
    if scale >= 1.0:
        return image.copy()
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return image.resize(new_size, Image.Resampling.LANCZOS)


def build_variant_lookup(
    work_gallery: list[dict] | None = None,
    jaehyun_gallery: list[dict] | None = None,
) -> dict[tuple[str, str], str]:
    lookup: dict[tuple[str, str], str] = {}

    if work_gallery:
        for slide in work_gallery:
            variant = "work-spread" if slide["type"] in WORK_SPREAD_TYPES else "single"
            for filename in slide["files"]:
                lookup[("work", filename)] = variant

    if jaehyun_gallery:
        for slide in jaehyun_gallery:
            if slide["type"] == "contact-sheet":
                variant = "contact"
            elif slide["type"] == "pair-spaced":
                variant = "pair"
            elif slide["type"] == "single":
                variant = slide.get("variant", "single")
            else:
                variant = "single"
            for filename in slide["files"]:
                lookup[("jaehyun", filename)] = variant

    return lookup


def legacy_variant_for(folder_key: str, filename: str) -> str:
    if folder_key == "info":
        return "info"
    if folder_key == "work":
        return "work-spread" if filename in WORK_SPREAD else "single"
    return JAEHYUN_VARIANTS.get(filename, "single")


def variant_for_file(
    folder_key: str,
    filename: str,
    variant_lookup: dict[tuple[str, str], str] | None = None,
) -> str:
    if variant_lookup:
        direct = variant_lookup.get((folder_key, filename))
        if direct:
            return direct

        name_stem = Path(filename).stem.lower()
        for (lookup_folder, lookup_name), variant in variant_lookup.items():
            if lookup_folder == folder_key and Path(lookup_name).stem.lower() == name_stem:
                return variant

    return legacy_variant_for(folder_key, filename)


def webp_path_for_web_jpg(web_jpg_path: Path) -> Path:
    return web_jpg_path.with_suffix(".webp")


def resolve_jpg_in_dir(image_dir: Path, filename: str) -> Path | None:
    if not image_dir.is_dir():
        return None

    direct = image_dir / filename
    if direct.is_file() and direct.suffix.lower() in {".jpg", ".jpeg"}:
        return direct

    target_stem = Path(filename).stem.lower()
    for path in image_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".jpg", ".jpeg"}:
            continue
        if path.stem.lower() == target_stem:
            return path

    return None


def resolve_original_path(image_dir: Path, filename: str) -> Path | None:
    return resolve_jpg_in_dir(originals_dir(image_dir), filename)


def resolve_web_jpg_path(image_dir: Path, filename: str) -> Path:
    existing = resolve_jpg_in_dir(image_dir, filename)
    if existing and existing.parent == image_dir:
        return existing
    return image_dir / filename


def list_original_jpgs(image_dir: Path) -> list[Path]:
    folder = originals_dir(image_dir)
    if not folder.is_dir():
        return []
    return sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg"}
    )


def profile_is_current(image_dir: Path) -> bool:
    stamp_path = profile_stamp_path(image_dir)
    if not stamp_path.is_file():
        return False
    return stamp_path.read_text(encoding="utf-8").strip() == OPTIMIZE_PROFILE


def write_profile_stamp(image_dir: Path) -> None:
    profile_stamp_path(image_dir).write_text(OPTIMIZE_PROFILE + "\n", encoding="utf-8")


def ensure_original(image_dir: Path, filename: str) -> Path | None:
    """Return preserved original path, migrating legacy root JPG once if needed."""
    existing = resolve_original_path(image_dir, filename)
    if existing is not None:
        return existing

    originals = originals_dir(image_dir)
    originals.mkdir(parents=True, exist_ok=True)

    legacy = resolve_jpg_in_dir(image_dir, filename)
    if legacy is None or legacy.parent == originals:
        return None

    target = originals / legacy.name
    if not target.is_file():
        shutil.copy2(legacy, target)
        print(f"Preserved original → {target.relative_to(ROOT)}")

    return target


def needs_optimization(original_path: Path, web_jpg_path: Path, image_dir: Path) -> bool:
    if not profile_is_current(image_dir):
        return True

    webp_path = webp_path_for_web_jpg(web_jpg_path)
    if not web_jpg_path.is_file() or not webp_path.is_file():
        return True

    original_mtime = original_path.stat().st_mtime
    return original_mtime > web_jpg_path.stat().st_mtime or original_mtime > webp_path.stat().st_mtime


def optimize_from_original(
    image_dir: Path,
    folder_key: str,
    filename: str,
    variant_lookup: dict[tuple[str, str], str] | None = None,
) -> dict:
    original_path = ensure_original(image_dir, filename)
    if original_path is None:
        raise FileNotFoundError(f"Original not found for {folder_key}/{filename}")

    web_jpg_path = resolve_web_jpg_path(image_dir, filename)
    original_bytes = original_path.stat().st_size
    original_mtime_before = original_path.stat().st_mtime

    with Image.open(original_path) as image:
        image = image.convert("RGB")
        portrait = image.height >= image.width
        variant = variant_for_file(folder_key, filename, variant_lookup)
        max_w, max_h = display_box(variant, portrait)
        resized = fit_within(image, max_w, max_h)

        resized.save(
            web_jpg_path,
            format="JPEG",
            quality=JPG_QUALITY,
            optimize=True,
            progressive=True,
        )
        webp_path = webp_path_for_web_jpg(web_jpg_path)
        resized.save(
            webp_path,
            format="WEBP",
            quality=WEBP_QUALITY,
            method=6,
        )

    original_mtime_after = original_path.stat().st_mtime
    if original_mtime_after != original_mtime_before:
        raise RuntimeError(f"Original file was modified unexpectedly: {original_path}")

    return {
        "original": str(original_path.relative_to(ROOT)),
        "web_jpg": str(web_jpg_path.relative_to(ROOT)),
        "webp": str(webp_path.relative_to(ROOT)),
        "variant": variant,
        "target_box": [max_w, max_h],
        "output_size": list(resized.size),
        "original_bytes": original_bytes,
        "jpg_bytes": web_jpg_path.stat().st_size,
        "webp_bytes": webp_path.stat().st_size,
    }


def collect_referenced_filenames(gallery: list[dict]) -> list[str]:
    filenames: list[str] = []
    seen: set[str] = set()
    for slide in gallery:
        for filename in slide["files"]:
            if filename not in seen:
                seen.add(filename)
                filenames.append(filename)
    return filenames


def referenced_stems(gallery: list[dict]) -> set[str]:
    return {Path(name).stem.lower() for slide in gallery for name in slide["files"]}


def cleanup_unreferenced_files(image_dir: Path, gallery: list[dict], label: str) -> list[str]:
    """Delete originals, web JPG, and WebP not listed in slides.txt."""
    keep = referenced_stems(gallery)
    deleted: list[str] = []

    originals = originals_dir(image_dir)
    if originals.is_dir():
        for path in list_original_jpgs(image_dir):
            if path.stem.lower() in keep:
                continue
            path.unlink()
            deleted.append(str(path.relative_to(ROOT)))

    for path in sorted(image_dir.iterdir()):
        if not path.is_file():
            continue
        stem = path.stem.lower()
        if stem in keep:
            continue
        if path.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
            path.unlink()
            deleted.append(str(path.relative_to(ROOT)))

    if deleted:
        print(f"Removed {len(deleted)} unreferenced file(s) from {label}:")
        for item in deleted:
            print(f"  - {item}")

    return deleted


def find_unreferenced_jpgs(image_dir: Path, referenced_filenames: list[str]) -> list[str]:
    referenced_stems = {Path(name).stem.lower() for name in referenced_filenames}
    unreferenced = []
    for path in list_original_jpgs(image_dir):
        if path.stem.lower() not in referenced_stems:
            unreferenced.append(path.name)
    return unreferenced


def optimize_gallery_images(
    work_dir: Path,
    jaehyun_dir: Path,
    work_gallery: list[dict],
    jaehyun_gallery: list[dict],
    *,
    include_info: bool = True,
) -> list[dict]:
    variant_lookup = build_variant_lookup(work_gallery, jaehyun_gallery)
    results: list[dict] = []
    touched_dirs: set[Path] = set()

    for gallery, image_dir, folder_key in (
        (work_gallery, work_dir, "work"),
        (jaehyun_gallery, jaehyun_dir, "jaehyun"),
    ):
        for filename in collect_referenced_filenames(gallery):
            original_path = ensure_original(image_dir, filename)
            if original_path is None:
                print(f"Warning: original not found for {folder_key}/{filename}")
                continue

            web_jpg_path = resolve_web_jpg_path(image_dir, filename)
            if not needs_optimization(original_path, web_jpg_path, image_dir):
                continue

            print(
                f"Optimizing {original_path.relative_to(ROOT)} "
                f"→ {web_jpg_path.relative_to(ROOT)}"
            )
            results.append(
                optimize_from_original(image_dir, folder_key, filename, variant_lookup)
            )
            touched_dirs.add(image_dir)

    if include_info:
        info_dir = ROOT / "images" / "info"
        if info_dir.is_dir():
            for original_path in list_original_jpgs(info_dir):
                filename = original_path.name
                web_jpg_path = resolve_web_jpg_path(info_dir, filename)
                if not needs_optimization(original_path, web_jpg_path, info_dir):
                    continue
                print(
                    f"Optimizing {original_path.relative_to(ROOT)} "
                    f"→ {web_jpg_path.relative_to(ROOT)}"
                )
                results.append(
                    optimize_from_original(info_dir, "info", filename, variant_lookup)
                )
                touched_dirs.add(info_dir)

            # Migrate legacy info JPG if originals folder was empty.
            if not list_original_jpgs(info_dir):
                for legacy in sorted(info_dir.iterdir()):
                    if not legacy.is_file():
                        continue
                    if legacy.suffix.lower() not in {".jpg", ".jpeg"}:
                        continue
                    ensure_original(info_dir, legacy.name)

    for image_dir in touched_dirs:
        write_profile_stamp(image_dir)

    return results


def write_report(results: list[dict]) -> None:
    summary = {
        "profile": OPTIMIZE_PROFILE,
        "jpg_quality": JPG_QUALITY,
        "webp_quality": WEBP_QUALITY,
        "original_bytes": sum(item["original_bytes"] for item in results),
        "jpg_bytes": sum(item["jpg_bytes"] for item in results),
        "webp_bytes": sum(item["webp_bytes"] for item in results),
        "files": len(results),
        "results": results,
    }
    report_path = ROOT / "scripts" / "optimize-images-report.json"
    report_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    folders = [ROOT / "images" / name for name in ("jaehyun", "work", "info")]
    results = []
    for folder in folders:
        folder_key = folder.name
        for original_path in list_original_jpgs(folder):
            filename = original_path.name
            web_jpg_path = resolve_web_jpg_path(folder, filename)
            if needs_optimization(original_path, web_jpg_path, folder):
                results.append(optimize_from_original(folder, folder_key, filename))
        if results:
            write_profile_stamp(folder)

    write_report(results)
    summary = {
        "files": len(results),
        "original_bytes": sum(item["original_bytes"] for item in results),
        "jpg_bytes": sum(item["jpg_bytes"] for item in results),
        "webp_bytes": sum(item["webp_bytes"] for item in results),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
