const MOBILE_MEDIA = window.matchMedia("(max-width: 768px)");

function isMobileView() {
  return MOBILE_MEDIA.matches;
}
