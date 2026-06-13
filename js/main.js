const sectionLinks = document.querySelectorAll("[data-section]");
const menuLinks = document.querySelectorAll(".menu-link");
const sections = document.querySelectorAll(".section");

function showSection(sectionId) {
  sections.forEach((section) => {
    section.classList.toggle("section-active", section.id === sectionId);
  });

  menuLinks.forEach((link) => {
    link.classList.toggle("active", link.dataset.section === sectionId);
  });
}

sectionLinks.forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    showSection(link.dataset.section);
    if (link.hasAttribute("data-reset-slideshow")) {
      showSlide(0);
    }
    history.replaceState(null, "", `#${link.dataset.section}`);
  });
});

const slideshowContainer = document.querySelector(".hero-slideshow");
if (slideshowContainer) {
  buildHeroSlideshow(slideshowContainer);
}

const slides = document.querySelectorAll(".hero-slideshow .slide");
const jaehyunSection = document.getElementById("jaehyun");
const sidebar = document.querySelector(".sidebar");
const prevZone = document.querySelector(".hero-zone-prev");
const nextZone = document.querySelector(".hero-zone-next");
const customCursor = document.querySelector(".custom-cursor");
const cursorArrowLeft = document.querySelector(".custom-cursor-arrow-left");
const cursorArrowRight = document.querySelector(".custom-cursor-arrow-right");

let currentSlide = 0;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle("slide-active", i === index);
  });
  currentSlide = index;
}

const initialSection = window.location.hash.slice(1) || "jaehyun";
if (document.getElementById(initialSection)) {
  showSection(initialSection);
}

prevZone?.addEventListener("click", () => {
  showSlide((currentSlide - 1 + slides.length) % slides.length);
});

nextZone?.addEventListener("click", () => {
  showSlide((currentSlide + 1) % slides.length);
});

function isOverSidebar(x, y) {
  if (!sidebar) return false;
  const rect = sidebar.getBoundingClientRect();
  return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
}

function isInNavigationArea(x, y) {
  const isJaehyunActive = jaehyunSection?.classList.contains("section-active");
  return isJaehyunActive && !isOverSidebar(x, y);
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
