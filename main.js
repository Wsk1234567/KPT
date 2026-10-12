/* Night Dispatch — interactions */
(function () {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* Mobile drawer */
  const toggle = document.querySelector(".nav-toggle");
  const drawer = document.getElementById("mobile-drawer");
  if (toggle && drawer) {
    const setOpen = (open) => {
      drawer.classList.toggle("is-open", open);
      drawer.hidden = !open;
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.style.overflow = open ? "hidden" : "";
    };

    toggle.addEventListener("click", () => setOpen(drawer.hidden));
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setOpen(false);
    });
  }

  /* Reveal */
  const reveals = document.querySelectorAll(".reveal");
  if (reduceMotion) {
    reveals.forEach((el) => el.classList.add("is-in"));
  } else if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  /* Count-up */
  const formatVal = (v, decimals) =>
    decimals > 0 ? v.toFixed(decimals) : Math.round(v).toLocaleString("en-US");

  const animateCount = (el) => {
    const target = parseFloat(el.getAttribute("data-count") || "0");
    const decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
    if (reduceMotion) {
      el.textContent = formatVal(target, decimals);
      return;
    }
    const start = performance.now();
    const duration = 1500;
    const tick = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = formatVal(target * eased, decimals);
      if (t < 1) requestAnimationFrame(tick);
      else el.textContent = formatVal(target, decimals);
    };
    requestAnimationFrame(tick);
  };

  const counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    const cio = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateCount(entry.target);
            cio.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.35 }
    );
    counters.forEach((el) => cio.observe(el));
  } else {
    counters.forEach(animateCount);
  }
})();

// Rotate original wheel pixels about the measured axle, without moving their centers.
(() => {
  const image = document.querySelector('.ambulance-img');
  if (!image) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const wheels = [
    { canvas: document.querySelector('.driving-wheel--rear'), x: 338, y: 808 },
    { canvas: document.querySelector('.driving-wheel--front'), x: 1187, y: 808 }
  ].filter(wheel => wheel.canvas);
  let frame = 0;
  let visible = true;
  function paint(now) {
    const angle = motion.matches ? 0 : (now % 1150) / 1150 * Math.PI * 2;
    for (const wheel of wheels) {
      const ctx = wheel.canvas.getContext('2d');
      ctx.clearRect(0, 0, 460, 460);
      ctx.save();
      ctx.translate(230, 230);
      ctx.beginPath();
      // Rotate only the rim; the outer crop includes pale wheel-arch pixels.
      ctx.arc(0, 0, 142, 0, Math.PI * 2);
      ctx.clip();
      ctx.rotate(angle);
      ctx.drawImage(image, wheel.x - 115, wheel.y - 115, 230, 230, -230, -230, 460, 460);
      ctx.restore();
    }
    frame = !motion.matches && visible && !document.hidden ? requestAnimationFrame(paint) : 0;
  }
  function restart() {
    cancelAnimationFrame(frame);
    if (image.complete && image.naturalWidth) paint(performance.now());
  }
  image.addEventListener('load', restart);
  motion.addEventListener('change', restart);
  document.addEventListener('visibilitychange', restart);
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    restart();
  }).observe(image);
  restart();
})();
