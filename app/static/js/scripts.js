"use strict";

//  ExpenseIQ Frontend

//  Theme Manager

const ThemeManager = (() => {
  const root = document.documentElement;
  const storageKey = "theme";

  function apply(theme) {
    root.classList.toggle("dark", theme === "dark");
    localStorage.setItem(storageKey, theme);
  }

  function toggle() {
    apply(root.classList.contains("dark") ? "light" : "dark");
  }

  function initialize() {
    apply(localStorage.getItem(storageKey) || "light");

    document
      .getElementById("darkModeBtn")
      ?.addEventListener("click", toggle);

    document
      .getElementById("darkModeBtnMobile")
      ?.addEventListener("click", toggle);
  }

  return { initialize };
})();

//  Mobile Navigation

const MobileMenu = (() => {
  const button = document.getElementById("menuBtn");
  const menu = document.getElementById("mobileMenu");

  function initialize() {
    if (!button || !menu) return;

    button.addEventListener("click", () => {
      menu.classList.toggle("hidden");
    });

    document.addEventListener("click", (event) => {
      if (
        !menu.classList.contains("hidden") &&
        !menu.contains(event.target) &&
        !button.contains(event.target)
      ) {
        menu.classList.add("hidden");
      }
    });

    window.addEventListener("resize", () => {
      if (window.innerWidth >= 768) {
        menu.classList.add("hidden");
      }
    });
  }

  return { initialize };
})();

//  Expense Form

const ExpenseForm = (() => {
  const categorySelect =
    document.getElementById("categorySelect");

  const customCategory =
    document.getElementById("customCategory");

  function toggleCategory() {
    if (!categorySelect || !customCategory) return;

    const isCustom =
      categorySelect.value === "custom";

    customCategory.classList.toggle(
      "hidden",
      !isCustom
    );

    customCategory.required = isCustom;

    if (!isCustom) {
      customCategory.value = "";
    }
  }

  function initialize() {
    if (!categorySelect) return;

    toggleCategory();

    categorySelect.addEventListener(
      "change",
      toggleCategory
    );
  }

  return { initialize };
})();

//  Card Animation

const AnimationManager = (() => {
  function initialize() {
    document
      .querySelectorAll(".animate-card")
      .forEach((card, index) => {
        card.classList.add(
          "opacity-0",
          "translate-y-4"
        );

        setTimeout(() => {
          card.classList.add(
            "transition-all",
            "duration-500"
          );

          card.classList.remove(
            "opacity-0",
            "translate-y-4"
          );
        }, index * 80);
      });
  }

  return { initialize };
})();

//  AI Insights

const AIInsights = (() => {
  const button =
    document.getElementById("generateAiBtn");

  const container =
    document.getElementById("aiInsightsBox");

  function loadingUI() {
    container.innerHTML = `
      <div class="space-y-3">
        ${Array.from({ length: 4 })
        .map(
          () => `
          <div
            class="h-12 rounded-2xl bg-slate-200 dark:bg-slate-700 animate-pulse">
          </div>
        `
        )
        .join("")}
      </div>
    `;
  }

  function render(insights) {
    container.innerHTML = insights
      .map(
        (item) => `
      <div
        class="rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 p-4 leading-relaxed">
        ${item}
      </div>
    `
      )
      .join("");
  }

  function renderError() {
    container.innerHTML = `
      <div
        class="rounded-2xl bg-red-100 p-4 text-red-700 dark:bg-red-900/30 dark:text-red-300">
        Failed to generate AI insights.
      </div>
    `;
  }

  async function generate() {
    if (!button || !container) return;

    button.disabled = true;
    button.textContent = "Generating...";

    loadingUI();

    try {
      const response = await fetch("/ai-insights");
      const data = await response.json();

      render(data.insights);
    } catch {
      renderError();
    }

    button.disabled = false;
    button.textContent = "Generate";
  }

  function initialize() {
    if (!button) return;

    button.addEventListener("click", generate);
  }

  return { initialize };
})();

//  Application Bootstrap

document.addEventListener("DOMContentLoaded", () => {
  ThemeManager.initialize();

  MobileMenu.initialize();

  ExpenseForm.initialize();

  AnimationManager.initialize();

  AIInsights.initialize();
});