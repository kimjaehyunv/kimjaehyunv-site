const sectionLinks = document.querySelectorAll("[data-section]");
const menuLinks = document.querySelectorAll(".menu-link");
const sections = document.querySelectorAll(".section");
const sidebar = document.querySelector(".sidebar");
const customCursor = document.querySelector(".custom-cursor");
const cursorArrowLeft = document.querySelector(".custom-cursor-arrow-left");
const cursorArrowRight = document.querySelector(".custom-cursor-arrow-right");

const viewers = new Map();

function setNavReady(sectionId, ready) {
  const nav = document.getElementById(sectionId)?.querySelector(".hero-nav");
  nav?.classList.toggle("hero-nav-ready", ready);
}

function showSection(sectionId) {
  sections.forEach((section) => {
    section.classList.toggle("section-active", section.id === sectionId);
  });

  menuLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.section === sectionId);
  });

  const viewer = viewers.get(sectionId);
  if (viewer) {
    const activeImg = viewer.section.querySelector(".slide-active img");
    if (activeImg) {
      activeImg.loading = "eager";
    }
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

  function showSlide(index) {
    const slides = getSlides();
    if (!slides.length) return;

    slides.forEach((slide, i) => {
      slide.classList.toggle("slide-active", i === index);
    });
    currentSlide = index;

    const activeImg = slides[index]?.querySelector("img");
    if (activeImg) {
      activeImg.loading = "eager";
    }
  }

  prevZone?.addEventListener("click", () => {
    const slides = getSlides();
    if (!slides.length) return;
    showSlide((currentSlide - 1 + slides.length) % slides.length);
  });

  nextZone?.addEventListener("click", () => {
    const slides = getSlides();
    if (!slides.length) return;
    showSlide((currentSlide + 1) % slides.length);
  });

  const slideCount = getSlides().length;
  setNavReady(sectionId, slideCount > 0);

  return {
    section,
    getSlides,
    showSlide,
  };
}

function initSlideshows() {
  const jaehyunContainer = document.querySelector("#jaehyun .hero-slideshow");
  if (jaehyunContainer) {
    buildHeroSlideshow(jaehyunContainer);
    const jaehyunViewer = createViewer("jaehyun");
    if (jaehyunViewer) viewers.set("jaehyun", jaehyunViewer);
  }

  const workContainer = document.querySelector("#work .hero-slideshow");
  if (workContainer) {
    buildWorkSlideshow(workContainer);
    const workViewer = createViewer("work");
    if (workViewer) viewers.set("work", workViewer);
  }
}

function isOverSidebar(x, y) {
  if (!sidebar) return false;
  const rect = sidebar.getBoundingClientRect();
  return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
}

function isInNavigationArea(x, y) {
  const activeViewer = Array.from(viewers.values()).find((viewer) => {
    return (
      viewer.section.classList.contains("section-active") &&
      viewer.getSlides().length > 0
    );
  });

  return Boolean(activeViewer) && !isOverSidebar(x, y);
}

function setCursorDirection(x) {
  const isLeft = x < window.innerWidth / 2;
  cursorArrowLeft?.classList.toggle("is-active", isLeft);
  cursorArrowRight?.classList.toggle("is-active", !isLeft);
}

document.addEventListener("mousemove", (event) => {
  const { clientX, clientY } = event;
  const shouldShow = isInNavigationArea(clientX, clientY);

  customCursor?.classList.toggle("is-visible", shouldShow);

  if (shouldShow) {
    customCursor.style.transform = `translate3d(${clientX}px, ${clientY}px, 0) translate(-50%, -50%)`;
    setCursorDirection(clientX);
  }
});

document.addEventListener("mouseleave", () => {
  customCursor?.classList.remove("is-visible");
});

initSlideshows();

const initialSection = window.location.hash.slice(1) || "jaehyun";
if (document.getElementById(initialSection)) {
  showSection(initialSection);
}
