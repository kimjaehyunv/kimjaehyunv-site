#!/usr/bin/env python3
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = ROOT / "images" / "work"
MANIFEST = WORK_DIR / "manifest.json"
WORK_SLIDES = ROOT / "js" / "work-slides.js"
INDEX_HTML = ROOT / "index.html"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

SPREAD_UPPER = ["06.jpg", "07.jpg", "08.jpg", "09.jpg"]
SPREAD_LOWER = ["10.jpg", "11.jpg"]
SPREAD_QUAD = ["20.jpg", "21.jpg", "22.jpg", "23.jpg"]
SPREAD_FILES = set(SPREAD_UPPER + SPREAD_LOWER + SPREAD_QUAD)
EXCLUDED_FILES = {"02.jpg", "03.jpg"}

WORK_SLIDES_TEMPLATE = '''const WORK_IMAGE_DIR = "images/work/";

const WORK_SLIDE_SEQUENCE = [
{sequence_js}
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

function buildWorkSpreadSlide(slide, slideData, lazy) {{
  slide.classList.add("slide-work-spread");
  const grid = document.createElement("div");
  grid.className = "work-spread-grid";

  if (slideData.type === "work-spread") {{
    slide.classList.add("slide-work-spread-upper");
  }} else if (slideData.type === "work-spread-lower") {{
    slide.classList.add("slide-work-spread-lower");
    grid.classList.add("work-spread-grid-lower");
  }} else if (slideData.type === "work-spread-quad") {{
    slide.classList.add("slide-work-spread-quad");
    grid.classList.add("work-spread-grid-quad");
  }}

  slideData.files.forEach((file) => {{
    grid.appendChild(createWorkSlideImage(file, lazy));
  }});

  slide.appendChild(grid);
}}

let workSpreadSyncScheduled = false;
let workSpreadResizeAttached = false;

function syncWorkSpreadGrids() {{
  if (isMobileView()) return;

  const upperSlide = document.querySelector("#work .slide-work-spread-upper");
  const lowerGrid = document.querySelector("#work .work-spread-grid-lower");
  if (!upperSlide || !lowerGrid) return;

  const upperImgs = upperSlide.querySelectorAll("img");
  if (upperImgs.length < 4) return;

  const col1 = Math.max(upperImgs[0].offsetWidth, upperImgs[3].offsetWidth);
  const col2 = upperImgs[1].offsetWidth;
  const col3 = upperImgs[2].offsetWidth;
  const row1Height = Math.max(
    upperImgs[0].offsetHeight,
    upperImgs[1].offsetHeight,
    upperImgs[2].offsetHeight,
  );

  if (!col1 || !col2 || !col3 || !row1Height) return;

  lowerGrid.style.gridTemplateColumns = `${{col1}}px ${{col2}}px ${{col3}}px`;
  lowerGrid.style.gridTemplateRows = `${{row1Height}}px auto`;
}}

function scheduleWorkSpreadSync() {{
  if (workSpreadSyncScheduled) return;
  workSpreadSyncScheduled = true;

  requestAnimationFrame(() => {{
    workSpreadSyncScheduled = false;
    syncWorkSpreadGrids();
  }});
}}

window.scheduleWorkSpreadSync = scheduleWorkSpreadSync;

function watchWorkSpreadImages(container) {{
  container.querySelectorAll(".slide-work-spread img").forEach((img) => {{
    if (img.complete) {{
      scheduleWorkSpreadSync();
    }} else {{
      img.addEventListener("load", scheduleWorkSpreadSync);
    }}
  }});
}}

function flattenWorkSequence(sequence) {{
  const flat = [];

  sequence.forEach((slideData) => {{
    if (slideData.type === "single") {{
      flat.push({{ ...slideData }});
      return;
    }}

    slideData.files.forEach((file) => {{
      flat.push({{ type: "single", files: [file] }});
    }});
  }});

  return flat;
}}

function buildWorkSlideshow(container, options = {{}}) {{
  const sequence = options.mobile
    ? flattenWorkSequence(WORK_SLIDE_SEQUENCE)
    : WORK_SLIDE_SEQUENCE;

  sequence.forEach((slideData, index) => {{
    const slide = document.createElement("div");
    slide.className = "slide";

    if (index === 0) {{
      slide.classList.add("slide-active");
    }}

    if (slideData.type === "single") {{
      slide.classList.add("slide-single");
      slide.appendChild(createWorkSlideImage(slideData.files[0], index !== 0));
    }} else if (
      slideData.type === "work-spread" ||
      slideData.type === "work-spread-lower" ||
      slideData.type === "work-spread-quad"
    ) {{
      buildWorkSpreadSlide(slide, slideData, index !== 0);
    }}

    container.appendChild(slide);
  }});

  if (options.mobile) {{
    return sequence.length;
  }}

  watchWorkSpreadImages(container);
  scheduleWorkSpreadSync();

  if (!workSpreadResizeAttached) {{
    workSpreadResizeAttached = true;
    window.addEventListener("resize", scheduleWorkSpreadSync);
  }}

  return sequence.length;
}}
'''


def sort_key(name: str):
    match = re.match(r"(\d+)(a)?", name, re.I)
    if match:
        return (int(match.group(1)), 1 if match.group(2) else 0, name.lower())
    return (999, 0, name.lower())


def spread_insert_index(file_list, first_file, removed_before):
    index = next(i for i, file in enumerate(file_list) if file == first_file)
    return index - removed_before


def bump_asset_version(version: str) -> None:
    html = INDEX_HTML.read_text(encoding="utf-8")
    html = re.sub(
        r'href="css/style\.css\?v=[^"]+"',
        f'href="css/style.css?v={version}"',
        html,
    )
    for asset in ("mobile.js", "slides.js", "work-slides.js", "main.js"):
        html = re.sub(
            rf'src="js/{re.escape(asset)}\?v=[^"]+"',
            f'src="js/{asset}?v={version}"',
            html,
        )
    INDEX_HTML.write_text(html, encoding="utf-8")


files = sorted(
    [
        path.name
        for path in WORK_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in EXTENSIONS
        and path.name not in EXCLUDED_FILES
    ],
    key=sort_key,
)

MANIFEST.write_text(json.dumps(files, indent=2) + "\n", encoding="utf-8")

sequence_entries = []
for file in files:
    if file in SPREAD_FILES:
        continue
    sequence_entries.append(f'  {{ type: "single", files: ["{file}"] }},')

upper_index = spread_insert_index(files, "06.jpg", 0)
sequence_entries.insert(
    upper_index,
    '  { type: "work-spread", files: ["06.jpg", "07.jpg", "08.jpg", "09.jpg"] },',
)

lower_index = spread_insert_index(files, "10.jpg", len(SPREAD_UPPER) - 1)
sequence_entries.insert(
    lower_index,
    '  { type: "work-spread-lower", files: ["10.jpg", "11.jpg"] },',
)

quad_index = spread_insert_index(
    files,
    "20.jpg",
    (len(SPREAD_UPPER) - 1) + (len(SPREAD_LOWER) - 1),
)
sequence_entries.insert(
    quad_index,
    '  { type: "work-spread-quad", files: ["20.jpg", "21.jpg", "22.jpg", "23.jpg"] },',
)

sequence_js = "\n".join(sequence_entries)
WORK_SLIDES.write_text(
    WORK_SLIDES_TEMPLATE.format(sequence_js=sequence_js),
    encoding="utf-8",
)

asset_version = date.today().strftime("%Y%m%d")
bump_asset_version(asset_version)

print(
    f"Wrote {len(files)} images to {MANIFEST}, {WORK_SLIDES}, "
    f"and bumped asset version to {asset_version}"
)
