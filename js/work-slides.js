const WORK_IMAGE_DIR = "images/work/";

const WORK_SLIDE_SEQUENCE = [
  { type: "single", files: ["01.jpg"] },
  { type: "single", files: ["04.jpg"] },
  { type: "single", files: ["05.jpg"] },
  { type: "work-spread", files: ["06.jpg", "07.jpg", "08.jpg", "09.jpg"] },
  { type: "work-spread-lower", files: ["10.jpg", "11.jpg"] },
  { type: "single", files: ["12.jpg"] },
  { type: "single", files: ["13.jpg"] },
  { type: "single", files: ["14.jpg"] },
  { type: "single", files: ["15.jpg"] },
  { type: "single", files: ["16.jpg"] },
  { type: "single", files: ["17.jpg"] },
  { type: "single", files: ["18.jpg"] },
  { type: "single", files: ["19.jpg"] },
  { type: "single", files: ["19a.jpg"] },
  { type: "work-spread-quad", files: ["20.jpg", "21.jpg", "22.jpg", "23.jpg"] },
  { type: "single", files: ["24.jpg"] },
  { type: "single", files: ["25.jpg"] },
  { type: "single", files: ["26.jpg"] },
  { type: "single", files: ["27.jpg"] },
  { type: "single", files: ["28.jpg"] },
  { type: "single", files: ["29.jpg"] },
  { type: "single", files: ["30.jpg"] },
  { type: "single", files: ["31.jpg"] },
];

function classifyPortraitImage(img) {
  const apply = () => {
    if (!img.naturalWidth || !img.naturalHeight) return;
    img.classList.toggle("img-portrait", img.naturalHeight >= img.naturalWidth);
  };

  if (img.complete) {
    apply();
  } else {
    img.addEventListener("load", apply, { once: true });
  }
}

function createWorkSlideImage(file, lazy = true) {
  const img = document.createElement("img");
  img.src = `${WORK_IMAGE_DIR}${file}`;
  img.alt = "Work by Jaehyun Kim";
  if (lazy) {
    img.loading = "lazy";
  }
  classifyPortraitImage(img);
  return img;
}

function buildWorkSpreadSlide(slide, slideData, lazy) {
  slide.classList.add("slide-work-spread");
  const grid = document.createElement("div");
  grid.className = "work-spread-grid";

  if (slideData.type === "work-spread") {
    slide.classList.add("slide-work-spread-upper");
  } else if (slideData.type === "work-spread-lower") {
    slide.classList.add("slide-work-spread-lower");
    grid.classList.add("work-spread-grid-lower");
  } else if (slideData.type === "work-spread-quad") {
    slide.classList.add("slide-work-spread-quad");
    grid.classList.add("work-spread-grid-quad");
  } else if (slideData.type === "work-spread-pair-vertical") {
    slide.classList.add("slide-work-spread-pair-vertical");
    grid.classList.add("work-spread-grid-vertical");
  }

  slideData.files.forEach((file) => {
    grid.appendChild(createWorkSlideImage(file, lazy));
  });

  slide.appendChild(grid);
}

let workSpreadSyncScheduled = false;
let workSpreadResizeAttached = false;

function syncWorkSpreadGrids() {
  if (typeof isMobileView === "function" && isMobileView()) return;

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

  lowerGrid.style.gridTemplateColumns = `${col1}px ${col2}px ${col3}px`;
  lowerGrid.style.gridTemplateRows = `${row1Height}px auto`;
}

function scheduleWorkSpreadSync() {
  if (workSpreadSyncScheduled) return;
  workSpreadSyncScheduled = true;

  requestAnimationFrame(() => {
    workSpreadSyncScheduled = false;
    syncWorkSpreadGrids();
  });
}

window.scheduleWorkSpreadSync = scheduleWorkSpreadSync;

function watchWorkSpreadImages(container) {
  container.querySelectorAll(".slide-work-spread img").forEach((img) => {
    if (img.complete) {
      scheduleWorkSpreadSync();
    } else {
      img.addEventListener("load", scheduleWorkSpreadSync);
    }
  });
}

function flattenWorkSequence(sequence) {
  const flat = [];

  sequence.forEach((slideData) => {
    if (slideData.type === "single") {
      flat.push({ ...slideData });
      return;
    }

    slideData.files.forEach((file) => {
      flat.push({ type: "single", files: [file] });
    });
  });

  return flat;
}

function getWorkImageFiles() {
  return flattenWorkSequence(WORK_SLIDE_SEQUENCE).map(
    (slideData) => slideData.files[0],
  );
}

function prepareWorkMobileSequence(sequence) {
  const result = [];

  sequence.forEach((slideData) => {
    if (slideData.type === "work-spread-quad") {
      result.push({
        type: "work-spread-pair-vertical",
        files: [slideData.files[0], slideData.files[1]],
      });
      result.push({
        type: "work-spread-pair-vertical",
        files: [slideData.files[2], slideData.files[3]],
      });
      return;
    }

    result.push(slideData);
  });

  return result;
}

function buildWorkSlideshow(container, options = {}) {
  container.className = "hero-slideshow";

  let sequence = WORK_SLIDE_SEQUENCE;
  if (options.workMobile) {
    sequence = prepareWorkMobileSequence(WORK_SLIDE_SEQUENCE);
  } else if (options.mobile) {
    sequence = flattenWorkSequence(WORK_SLIDE_SEQUENCE);
  }

  sequence.forEach((slideData, index) => {
    const slide = document.createElement("div");
    slide.className = "slide";

    if (index === 0) {
      slide.classList.add("slide-active");
    }

    if (slideData.type === "single") {
      slide.classList.add("slide-single");
      slide.appendChild(createWorkSlideImage(slideData.files[0], index !== 0));
    } else if (
      slideData.type === "work-spread" ||
      slideData.type === "work-spread-lower" ||
      slideData.type === "work-spread-quad" ||
      slideData.type === "work-spread-pair-vertical"
    ) {
      buildWorkSpreadSlide(slide, slideData, index !== 0);
    }

    container.appendChild(slide);
  });

  if (options.mobile) {
    return sequence.length;
  }

  watchWorkSpreadImages(container);
  scheduleWorkSpreadSync();

  if (!workSpreadResizeAttached) {
    workSpreadResizeAttached = true;
    window.addEventListener("resize", scheduleWorkSpreadSync);
  }

  return sequence.length;
}
