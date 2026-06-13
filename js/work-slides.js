const WORK_IMAGE_DIR = "images/work/";

const WORK_IMAGE_FILES = [
  "01.jpg",
  "02.jpg",
  "03.jpg",
  "04.jpg",
  "05.jpg",
  "06.jpg",
  "07.jpg",
  "08.jpg",
  "09.jpg",
  "10.jpg",
  "11.jpg",
  "12.jpg",
  "13.jpg",
  "14.jpg",
  "15.jpg",
  "16.jpg",
  "17.jpg",
  "18.jpg",
  "19.jpg",
  "20.jpg",
  "21.jpg",
  "22.jpg",
  "23.jpg",
  "24.jpg",
  "25.jpg",
  "26.jpg",
  "27.jpg",
  "28.jpg",
  "29.jpg",
  "30.jpg",
  "31.jpg",
];

function createWorkSlideImage(file, lazy = true) {
  const img = document.createElement("img");
  img.src = `${WORK_IMAGE_DIR}${file}`;
  img.alt = "Work by Jaehyun Kim";
  if (lazy) {
    img.loading = "lazy";
  }
  return img;
}

function buildWorkSlideshow(container) {
  WORK_IMAGE_FILES.forEach((file, index) => {
    const slide = document.createElement("div");
    slide.className = "slide slide-single";

    if (index === 0) {
      slide.classList.add("slide-active");
    }

    slide.appendChild(createWorkSlideImage(file, index !== 0));
    container.appendChild(slide);
  });

  return WORK_IMAGE_FILES.length;
}
