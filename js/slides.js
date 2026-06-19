const IMAGE_DIR = "images/jaehyun/";

const JAEHYUN_SLIDE_SEQUENCE = [
  { type: "single", files: ["01.jpg"], variant: "opening" },
  { type: "single", files: ["02.jpg"] },
  { type: "single", files: ["03.jpg"] },
  { type: "single", files: ["04.jpg"] },
  { type: "single", files: ["05.jpg"] },
  { type: "single", files: ["06.JPG"] },
  { type: "single", files: ["07.JPG"] },
  { type: "single", files: ["08.JPG"] },
  { type: "single", files: ["09.jpg"], variant: "reduced-forty" },
  { type: "single", files: ["10.JPG"] },
  { type: "single", files: ["11.JPG"] },
  { type: "single", files: ["12.JPG"] },
  { type: "single", files: ["13.JPG"] },
  { type: "single", files: ["14.JPG"] },
  { type: "single", files: ["15.jpg"] },
  { type: "single", files: ["16.JPG"], variant: "lower-left" },
  { type: "single", files: ["17.JPG"] },
  { type: "single", files: ["18.jpg"] },
  { type: "contact-sheet", files: ["19.jpg", "20.jpg", "21.jpg", "22.jpg"] },
  { type: "single", files: ["23.jpg"] },
  { type: "single", files: ["24.jpg"] },
  { type: "single", files: ["25.jpg"] },
  { type: "pair-spaced", files: ["26.jpg", "27.jpg"] },
  { type: "single", files: ["28.jpg"], variant: "reduced" },
  { type: "single", files: ["29.JPG"] },
  { type: "single", files: ["30.jpg"], variant: "small" },
  { type: "single", files: ["31.jpg"], variant: "closing" },
];

function createSlideImage(file) {
  const img = document.createElement("img");
  img.src = `${IMAGE_DIR}${file}`;
  img.alt = "Photograph by Jaehyun Kim";
  return img;
}

function flattenJaehyunSequence(sequence) {
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

function getJaehyunImageFiles() {
  return flattenJaehyunSequence(JAEHYUN_SLIDE_SEQUENCE).map(
    (slideData) => slideData.files[0],
  );
}

function buildHeroSlideshow(container, options = {}) {
  container.className = "hero-slideshow";

  const sequence = options.mobile
    ? flattenJaehyunSequence(JAEHYUN_SLIDE_SEQUENCE)
    : JAEHYUN_SLIDE_SEQUENCE;

  sequence.forEach((slideData, index) => {
    const slide = document.createElement("div");
    slide.className = "slide";

    if (index === 0) {
      slide.classList.add("slide-active");
    }

    if (slideData.type === "single") {
      slide.classList.add("slide-single");
      if (slideData.variant === "small") slide.classList.add("slide-small");
      if (slideData.variant === "closing") slide.classList.add("slide-closing");
      if (slideData.variant === "opening") slide.classList.add("slide-opening");
      if (slideData.variant === "lower-left") slide.classList.add("slide-lower-left");
      if (slideData.variant === "reduced") slide.classList.add("slide-reduced");
      if (slideData.variant === "reduced-forty") slide.classList.add("slide-reduced-forty");
      slide.appendChild(createSlideImage(slideData.files[0]));
    } else if (slideData.type === "contact-sheet") {
      slide.classList.add("slide-contact-sheet");
      slideData.files.forEach((file) => {
        slide.appendChild(createSlideImage(file));
      });
    } else if (slideData.type === "pair-spaced") {
      slide.classList.add("slide-pair-asymmetric");
      const spread = document.createElement("div");
      spread.className = "pair-spread";
      slideData.files.forEach((file, fileIndex) => {
        const img = createSlideImage(file);
        img.classList.add(fileIndex === 0 ? "pair-image-a" : "pair-image-b");
        spread.appendChild(img);
      });
      slide.appendChild(spread);
    }

    container.appendChild(slide);
  });
}
