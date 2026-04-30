const root = document.documentElement;

function applyTheme(theme) {
  if (theme === "dark") {
    root.classList.add("dark");
  } else {
    root.classList.remove("dark");
  }

  localStorage.setItem("theme", theme);
}

function toggleDarkMode() {
  if (root.classList.contains("dark")) {
    applyTheme("light");
  } else {
    applyTheme("dark");
  }
}

const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {
  applyTheme("dark");
} else {
  applyTheme("light");
}

document
  .getElementById("darkModeBtn")
  ?.addEventListener("click", toggleDarkMode);

document
  .getElementById("darkModeBtnMobile")
  ?.addEventListener("click", toggleDarkMode);

const menuBtn = document.getElementById("menuBtn");
const mobileMenu = document.getElementById("mobileMenu");

if (menuBtn && mobileMenu) {
  menuBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("hidden");
  });
}

document.addEventListener("click", (e) => {
  if (!menuBtn || !mobileMenu) return;

  if (
    !mobileMenu.classList.contains("hidden") &&
    !mobileMenu.contains(e.target) &&
    !menuBtn.contains(e.target)
  ) {
    mobileMenu.classList.add("hidden");
  }
});

window.addEventListener("resize", () => {
  if (window.innerWidth >= 768 && mobileMenu) {
    mobileMenu.classList.add("hidden");
  }
});

const toggleCustomCategory = () => {
  const select = document.getElementById("categorySelect");
  const custom = document.getElementById("customCategory");

  if (!select || !custom) return;

  if (select.value === "custom") {
    custom.classList.remove("hidden");
    custom.required = true;
  } else {
    custom.classList.add("hidden");
    custom.required = false;
    custom.value = "";
  }
};

document.addEventListener("DOMContentLoaded", () => {
  toggleCustomCategory();

  const cards = document.querySelectorAll(".animate-card");

  cards.forEach((card, index) => {
    card.classList.add("opacity-0", "translate-y-4");

    setTimeout(() => {
      card.classList.add("transition-all", "duration-500");

      card.classList.remove("opacity-0", "translate-y-4");
    }, index * 80);
  });
});
