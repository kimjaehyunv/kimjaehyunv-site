const MOBILE_MEDIA = window.matchMedia("(max-width: 768px)");

function isMobileView() {
  return MOBILE_MEDIA.matches;
}

function isMobileSpreadSlide(slide) {
  return (
    slide?.classList.contains("slide-work-spread") ||
    slide?.classList.contains("slide-work-spread-pair-vertical") ||
    slide?.classList.contains("slide-contact-sheet") ||
    slide?.classList.contains("slide-pair-asymmetric")
  );
}

function classifyMobileImageOrientation(img) {
  if (!isMobileView()) {
    img.classList.remove("mobile-landscape");
    return;
  }

  const slide = img.closest(".slide");
  if (!slide || isMobileSpreadSlide(slide)) return;

  const apply = () => {
    if (!img.naturalWidth || !img.naturalHeight) return;
    img.classList.toggle(
      "mobile-landscape",
      img.naturalWidth > img.naturalHeight,
    );
  };

  if (img.complete) {
    apply();
  } else {
    img.addEventListener("load", apply, { once: true });
  }
}

function classifyMobileSlideshowImages(container) {
  if (!container || !isMobileView()) return;

  container.querySelectorAll("img").forEach(classifyMobileImageOrientation);
}

function prepareMobileSlideImages(slide) {
  if (!slide) return Promise.resolve();

  const images = [...slide.querySelectorAll("img")];
  images.forEach((img) => {
    img.loading = "eager";
  });

  return Promise.all(
    images.map((img) => {
      if (img.complete) {
        classifyMobileImageOrientation(img);
        return img.decode?.().catch(() => undefined) ?? Promise.resolve();
      }

      return new Promise((resolve) => {
        img.addEventListener(
          "load",
          () => {
            classifyMobileImageOrientation(img);
            resolve();
          },
          { once: true },
        );
        img.addEventListener("error", () => resolve(), { once: true });
      });
    }),
  );
}

function createMobileViewer(sectionId, setNavReady) {
  const section = document.getElementById(sectionId);
  if (!section) return null;

  const prevZone = section.querySelector(".hero-zone-prev");
  const nextZone = section.querySelector(".hero-zone-next");
  let currentSlide = 0;

  function getSlides() {
    return section.querySelectorAll(".hero-slideshow .slide");
  }

  function preloadAdjacentSlides(index) {
    const slides = getSlides();
    if (!slides.length) return;

    const neighbors = [
      index,
      (index - 1 + slides.length) % slides.length,
      (index + 1) % slides.length,
    ];

    neighbors.forEach((slideIndex) => {
      prepareMobileSlideImages(slides[slideIndex]);
    });
  }

  function showSlide(index) {
    const slides = getSlides();
    if (!slides.length) return;

    slides.forEach((slide, i) => {
      slide.classList.toggle("slide-active", i === index);
    });
    currentSlide = index;

    preloadAdjacentSlides(index);

    if (sectionId === "work") {
      window.scheduleWorkSpreadSync?.();
    }
  }

  async function goPrev() {
    const slides = getSlides();
    if (!slides.length) return;

    const nextIndex = (currentSlide - 1 + slides.length) % slides.length;
    await prepareMobileSlideImages(slides[nextIndex]);
    showSlide(nextIndex);
  }

  async function goNext() {
    const slides = getSlides();
    if (!slides.length) return;

    const nextIndex = (currentSlide + 1) % slides.length;
    await prepareMobileSlideImages(slides[nextIndex]);
    showSlide(nextIndex);
  }

  prevZone.onclick = () => {
    goPrev();
  };

  nextZone.onclick = () => {
    goNext();
  };

  const slideCount = getSlides().length;
  setNavReady(sectionId, slideCount > 0);

  return {
    section,
    getSlides,
    showSlide,
    goNext,
    goPrev,
    preloadAdjacentSlides,
  };
}

function initMobileSlideshows(viewers, setNavReady) {
  const jaehyunContainer = document.querySelector("#jaehyun .hero-slideshow");
  if (jaehyunContainer) {
    buildHeroSlideshow(jaehyunContainer, { mobile: false, jaehyunMobile: true });
    classifyMobileSlideshowImages(jaehyunContainer);
    const jaehyunViewer = createMobileViewer("jaehyun", setNavReady);
    if (jaehyunViewer) viewers.set("jaehyun", jaehyunViewer);
  }

}

function initWorkMobileSlideshow(viewers, setNavReady) {
  const workContainer = document.querySelector("#work .hero-slideshow");
  if (!workContainer) return;

  buildWorkSlideshow(workContainer, { mobile: false, workMobile: true });
  classifyMobileSlideshowImages(workContainer);
  const workViewer = createMobileViewer("work", setNavReady);
  if (workViewer) viewers.set("work", workViewer);
}

function getMobileActiveImageSrc(sectionId) {
  const slide = document
    .getElementById(sectionId)
    ?.querySelector(".hero-slideshow .slide-active");
  return slide?.querySelector("img")?.getAttribute("src") ?? null;
}

function restoreMobileSlideBySrc(sectionId, src, viewers) {
  if (!src) return;

  const viewer = viewers.get(sectionId);
  if (!viewer) return;

  const slides = viewer.getSlides();
  const index = Array.from(slides).findIndex(
    (slide) => slide.querySelector("img")?.getAttribute("src") === src,
  );

  if (index >= 0) {
    viewer.showSlide(index);
  }
}
