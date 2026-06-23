#!/usr/bin/env python3
"""Resize and re-encode site images for delivery optimization."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
JPG_QUALITY = 84
WEBP_QUALITY = 82

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

    # Mobile hero caps can exceed variant caps for some slides.
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


def variant_for(path: Path) -> str:
    folder = path.parent.name
    name = path.name
    if folder == "info":
        return "info"
    if folder == "work":
        return "work-spread" if name in WORK_SPREAD else "single"
    return JAEHYUN_VARIANTS.get(name, "single")


def webp_path(path: Path) -> Path:
    return path.with_suffix(".webp")


def optimize_image(path: Path) -> dict:
    original_bytes = path.stat().st_size
    with Image.open(path) as image:
        image = image.convert("RGB")
        portrait = image.height >= image.width
        variant = variant_for(path)
        max_w, max_h = display_box(variant, portrait)
        resized = fit_within(image, max_w, max_h)

        resized.save(
            path,
            format="JPEG",
            quality=JPG_QUALITY,
            optimize=True,
            progressive=True,
        )
        webp = webp_path(path)
        resized.save(
            webp,
            format="WEBP",
            quality=WEBP_QUALITY,
            method=6,
        )

    return {
        "path": str(path.relative_to(ROOT)),
        "variant": variant,
        "target_box": [max_w, max_h],
        "output_size": list(resized.size),
        "original_bytes": original_bytes,
        "jpg_bytes": path.stat().st_size,
        "webp_bytes": webp.stat().st_size,
    }


def main() -> None:
    folders = [ROOT / "images" / name for name in ("jaehyun", "work", "info")]
    results = []
    for folder in folders:
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() not in {".jpg", ".jpeg"}:
                continue
            results.append(optimize_image(path))

    summary = {
        "original_bytes": sum(item["original_bytes"] for item in results),
        "jpg_bytes": sum(item["jpg_bytes"] for item in results),
        "webp_bytes": sum(item["webp_bytes"] for item in results),
        "files": len(results),
        "results": results,
    }
    report_path = ROOT / "scripts" / "optimize-images-report.json"
    report_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("files", "original_bytes", "jpg_bytes", "webp_bytes")}, indent=2))


if __name__ == "__main__":
    main()
