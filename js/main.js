document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("nav--open");
    });
  }

  var slider = document.getElementById("hero-slider");
  if (slider) {
    var slides = slider.querySelectorAll(".hero-slider__slide");
    var dots = slider.querySelectorAll(".hero-slider__dot");
    var current = 0;

    function show(index) {
      slides.forEach(function (s, i) { s.classList.toggle("hero-slider__slide--active", i === index); });
      dots.forEach(function (d, i) { d.classList.toggle("hero-slider__dot--active", i === index); });
      current = index;
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () { show(i); });
    });

    setInterval(function () {
      show((current + 1) % slides.length);
    }, 5000);
  }

  var plainThumbs = document.querySelectorAll(".work-grid__item--plain img");
  if (plainThumbs.length) {
    var lightbox = document.createElement("div");
    lightbox.className = "lightbox";
    lightbox.innerHTML = '<button class="lightbox__close" aria-label="Close">&times;</button><img alt="">';
    document.body.appendChild(lightbox);
    var lightboxImg = lightbox.querySelector("img");

    function openLightbox(src, alt) {
      lightboxImg.src = src;
      lightboxImg.alt = alt;
      lightbox.classList.add("lightbox--open");
    }

    function closeLightbox() {
      lightbox.classList.remove("lightbox--open");
    }

    plainThumbs.forEach(function (img) {
      img.addEventListener("click", function () {
        openLightbox(img.src, img.alt);
      });
    });

    lightbox.addEventListener("click", closeLightbox);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeLightbox();
    });
  }
});
