const sectionLinks = document.querySelectorAll("[data-section]");
const menuLinks = document.querySelectorAll(".menu-link");
const sections = document.querySelectorAll(".section");

const viewers = new Map();
let viewportListenerAttached = false;

function setNavReady(sectionId, ready) {
  const nav = document.getElementById(sectionId)?.querySelector(".hero-nav");
  nav?.classList.toggle("hero-nav-ready", ready);
}

function getActiveImageSrc(sectionId) {
  const section = document.getElementById(sectionId);
  if (!section) return null;

  if (isMobileView()) {
    return getMobileActiveImageSrc(sectionId);
  }

  const slide = section.querySelector(".hero-slideshow .slide-active");
  return slide?.querySelector("img")?.getAttribute("src") ?? null;
}

function restoreSlideBySrc(sectionId, src) {
  if (!src) return;

  if (isMobileView()) {
    restoreMobileSlideBySrc(sectionId, src, viewers);
    return;
  }

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

function showSection(sectionId) {
  sections.forEach((section) => {
    section.classList.toggle("section-active", section.id === sectionId);
  });

  menuLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.section === sectionId);
  });

  if (isMobileView()) {
    const mobileViewer = viewers.get(sectionId);
    if (mobileViewer) {
      const activeImg = mobileViewer.section.querySelector(".slide-active img");
      if (activeImg) {
        activeImg.loading = "eager";
      }
    }
    if (sectionId === "work") {
      window.scheduleWorkSpreadSync?.();
    }
    return;
  }

  const viewer = viewers.get(sectionId);
  if (viewer) {
    const activeImg = viewer.section.querySelector(".slide-active img");
    if (activeImg) {
      activeImg.loading = "eager";
    }
  }

  if (sectionId === "work") {
    window.scheduleWorkSpreadSync?.();
  }
}

sectionLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showSection(link.dataset.section);
    if (link.hasAttribute("data-reset-slideshow")) {
      viewers.get("jaehyun")?.showSlide(0);
    }
    history.replaceState(null, "", `#${link.dataset.section}`);
  });
});

function createViewer(sectionId) {
  const section = document.getElementById(sectionId);
  if (!section) return null;

  const prevZone = section.querySelector(".hero-zone-prev");
  const nextZone = section.querySelector(".hero-zone-next");
  let currentSlide = 0;

  function getSlides() {
    return section.querySelectorAll(".hero-slideshow .slide");
  }

  function prepareSlideImages(slide) {
    if (!slide) return Promise.resolve();

    const images = [...slide.querySelectorAll("img")];
    images.forEach((img) => {
      img.loading = "eager";
    });

    return Promise.all(
      images.map((img) => {
        if (img.complete) {
          return img.decode?.().catch(() => undefined) ?? Promise.resolve();
        }

        return new Promise((resolve) => {
          img.addEventListener("load", () => resolve(), { once: true });
          img.addEventListener("error", () => resolve(), { once: true });
        });
      }),
    );
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
      prepareSlideImages(slides[slideIndex]);
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
    await prepareSlideImages(slides[nextIndex]);
    showSlide(nextIndex);
  }

  async function goNext() {
    const slides = getSlides();
    if (!slides.length) return;

    const nextIndex = (currentSlide + 1) % slides.length;
    await prepareSlideImages(slides[nextIndex]);
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
  preloadAdjacentSlides(0);

  return {
    section,
    getSlides,
    showSlide,
    goNext,
    goPrev,
  };
}

function initDesktopSlideshows() {
  const jaehyunContainer = document.querySelector("#jaehyun .hero-slideshow");
  if (jaehyunContainer) {
    buildHeroSlideshow(jaehyunContainer, { mobile: false });
    const jaehyunViewer = createViewer("jaehyun");
    if (jaehyunViewer) viewers.set("jaehyun", jaehyunViewer);
  }

  const workContainer = document.querySelector("#work .hero-slideshow");
  if (workContainer) {
    buildWorkSlideshow(workContainer, { mobile: false });
    const workViewer = createViewer("work");
    if (workViewer) viewers.set("work", workViewer);
  }
}

function initSlideshows() {
  if (isMobileView()) {
    initMobileSlideshows(viewers, setNavReady);
    return;
  }

  initDesktopSlideshows();
}

function rebuildSlideshows() {
  const activeSection =
    document.querySelector(".section-active")?.id ?? "jaehyun";
  const jaehyunSrc = getActiveImageSrc("jaehyun");
  const workSrc = getActiveImageSrc("work");
  document.querySelector("#jaehyun .hero-slideshow").innerHTML = "";
  document.querySelector("#work .hero-slideshow").innerHTML = "";
  viewers.clear();

  initSlideshows();
  restoreSlideBySrc("jaehyun", jaehyunSrc);
  restoreSlideBySrc("work", workSrc);

  showSection(activeSection);
}

function attachViewportListener() {
  if (viewportListenerAttached) return;
  viewportListenerAttached = true;

  MOBILE_MEDIA.addEventListener("change", rebuildSlideshows);
}

function boot() {
  attachViewportListener();
  rebuildSlideshows();

  const initialSection = window.location.hash.slice(1) || "jaehyun";
  if (document.getElementById(initialSection)) {
    showSection(initialSection);
  }
}

boot();
