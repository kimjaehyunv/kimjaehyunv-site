const MOBILE_MEDIA = window.matchMedia("(max-width: 768px)");

function isMobileView() {
  return MOBILE_MEDIA.matches;
}

function buildMobileScrollFeed(container, imageDir, files, alt) {
  container.innerHTML = "";
  container.className = "hero-slideshow mobile-scroll-feed";

  files.forEach((file, index) => {
    const img = document.createElement("img");
    img.src = `${imageDir}${file}`;
    img.alt = alt;
    if (index > 1) {
      img.loading = "lazy";
    }
    container.appendChild(img);
  });

  return files.length;
}
