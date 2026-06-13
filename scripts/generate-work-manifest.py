#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "images" / "work"
MANIFEST = WORK_DIR / "manifest.json"
WORK_SLIDES = ROOT / "js" / "work-slides.js"
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

files_js = ",\n".join(f'  "{name}"' for name in files)

WORK_SLIDES.write_text(
    f"""const WORK_IMAGE_DIR = "images/work/";

const WORK_IMAGE_FILES = [
{files_js}
];

function createWorkSlideImage(file, lazy = true) {{
  const img = document.createElement("img");
  img.src = `${{WORK_IMAGE_DIR}}${{file}}`;
  img.alt = "Work by Jaehyun Kim";
  if (lazy) {{
    img.loading = "lazy";
  }}
  return img;
}}

function buildWorkSlideshow(container) {{
  WORK_IMAGE_FILES.forEach((file, index) => {{
    const slide = document.createElement("div");
    slide.className = "slide slide-single";

    if (index === 0) {{
      slide.classList.add("slide-active");
    }}

    slide.appendChild(createWorkSlideImage(file, index !== 0));
    container.appendChild(slide);
  }});

  return WORK_IMAGE_FILES.length;
}}
""",
    encoding="utf-8",
)

print(f"Wrote {len(files)} images to {MANIFEST} and {WORK_SLIDES}")
