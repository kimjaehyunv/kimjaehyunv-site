const WORK_IMAGE_DIR = "images/work/";

function createWorkSlideImage(file, lazy = true) {
  const img = document.createElement("img");
  img.src = `${WORK_IMAGE_DIR}${file}`;
  img.alt = "Work by Jaehyun Kim";
  if (lazy) {
    img.loading = "lazy";
  }
  return img;
}

async function buildWorkSlideshow(container) {
  const response = await fetch(`${WORK_IMAGE_DIR}manifest.json`);
  if (!response.ok) {
    throw new Error("Failed to load work image manifest.");
  }

  const files = await response.json();

  files.forEach((file, index) => {
    const slide = document.createElement("div");
    slide.className = "slide slide-single";

    if (index === 0) {
      slide.classList.add("slide-active");
    }

    slide.appendChild(createWorkSlideImage(file, index !== 0));
    container.appendChild(slide);
  });

  return files.length;
}
