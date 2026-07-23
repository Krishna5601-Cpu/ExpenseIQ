"use strict";

document.addEventListener("DOMContentLoaded", () => {
  initializeTheme();
  initializeMobileMenu();
  initializeCategoryToggle();
  initializeAIInsights();
});

/* ==========================================
   DARK MODE
========================================== */

function initializeTheme() {
  const html = document.documentElement;

  const desktopBtn = document.getElementById("darkModeBtn");
  const mobileBtn = document.getElementById("darkModeBtnMobile");

  // Load saved theme
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "dark") {
    html.classList.add("dark");
  } else {
    html.classList.remove("dark");
  }

  function updateIcons() {
    const dark = html.classList.contains("dark");

    if (desktopBtn) {
      desktopBtn.innerHTML = dark ? "☀️" : "🌙";
    }

    if (mobileBtn) {
      mobileBtn.innerHTML = dark ? "☀️" : "🌙";
    }
  }

  function toggleTheme() {
    if (html.classList.contains("dark")) {
      html.classList.remove("dark");
      localStorage.setItem("theme", "light");
    } else {
      html.classList.add("dark");
      localStorage.setItem("theme", "dark");
    }

    updateIcons();
  }

  desktopBtn?.addEventListener("click", toggleTheme);
  mobileBtn?.addEventListener("click", toggleTheme);

  updateIcons();
}

/* ==========================================
   MOBILE MENU
========================================== */

function initializeMobileMenu() {
  const menuBtn = document.getElementById("menuBtn");
  const mobileMenu = document.getElementById("mobileMenu");

  if (!menuBtn || !mobileMenu) return;

  menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();

    mobileMenu.classList.toggle("hidden");
  });

  document.addEventListener("click", (e) => {
    if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
      mobileMenu.classList.add("hidden");
    }
  });
}

/* ==========================================
   CUSTOM CATEGORY
========================================== */

function initializeCategoryToggle() {
  const categorySelect = document.getElementById("categorySelect");
  const customCategory = document.getElementById("customCategory");

  if (!categorySelect || !customCategory) return;

  function updateCategory() {
    if (categorySelect.value === "custom") {
      customCategory.classList.remove("hidden");
      customCategory.required = true;
    } else {
      customCategory.classList.add("hidden");
      customCategory.required = false;
      customCategory.value = "";
    }
  }

  categorySelect.addEventListener("change", updateCategory);

  updateCategory();
}

/* ==========================================
   AI INSIGHTS
========================================== */

function initializeAIInsights() {
  const button = document.getElementById("generateAiBtn");
  const box = document.getElementById("aiInsightsBox");

  if (!button || !box) return;

  button.addEventListener("click", async () => {
    button.disabled = true;
    button.textContent = "Generating...";

    box.innerHTML = `
            <div class="text-center py-8 text-gray-500 dark:text-slate-400">
                🤖 Generating AI insights...
            </div>
        `;

    try {
      const response = await fetch("/ai-insights");

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();

      if (!data.insights || data.insights.length === 0) {
        box.innerHTML = `
                    <div class="text-center py-8 text-gray-500 dark:text-slate-400">
                        No insights available.
                    </div>
                `;
      } else {
        box.innerHTML = data.insights
          .map(
            (item) => `
                    <div class="bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-xl p-4 mb-4 shadow">
                        <div class="flex gap-3">
                            <span class="text-xl">💡</span>
                            <p>${item}</p>
                        </div>
                    </div>
                `,
          )
          .join("");
      }
    } catch (error) {
      console.error(error);

      box.innerHTML = `
                <div class="bg-red-100 text-red-700 rounded-xl p-4">
                    Failed to generate AI insights.
                </div>
            `;
    } finally {
      button.disabled = false;
      button.textContent = "Generate AI Insights";
    }
  });
}
