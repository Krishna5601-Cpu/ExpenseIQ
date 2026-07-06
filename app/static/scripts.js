"use strict";

/* ==========================================================
   ExpenseIQ Frontend
========================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initializeDarkMode();
  initializeMobileMenu();
  initializeCategoryToggle();
  initializeAIInsights();
});

/* ==========================================================
   Dark Mode
========================================================== */

function initializeDarkMode() {
  const html = document.documentElement;

  const desktopBtn = document.getElementById("darkModeBtn");
  const mobileBtn = document.getElementById("darkModeBtnMobile");

  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "dark") {
    html.classList.add("dark");
  }

  function toggleTheme() {
    html.classList.toggle("dark");

    localStorage.setItem(
      "theme",
      html.classList.contains("dark")
        ? "dark"
        : "light"
    );
  }

  desktopBtn?.addEventListener("click", toggleTheme);
  mobileBtn?.addEventListener("click", toggleTheme);
}

/* ==========================================================
   Mobile Navigation
========================================================== */

function initializeMobileMenu() {

  const button = document.getElementById("menuBtn");
  const menu = document.getElementById("mobileMenu");

  if (!button || !menu) return;

  button.addEventListener("click", () => {
    menu.classList.toggle("hidden");
  });

  document.addEventListener("click", (event) => {

    if (
      !menu.contains(event.target) &&
      !button.contains(event.target)
    ) {
      menu.classList.add("hidden");
    }

  });

}

/* ==========================================================
   Category Toggle
========================================================== */

function initializeCategoryToggle() {

  const category = document.getElementById("categorySelect");
  const custom = document.getElementById("customCategory");

  if (!category || !custom) return;

  function update() {

    if (category.value === "custom") {

      custom.classList.remove("hidden");
      custom.required = true;

    } else {

      custom.classList.add("hidden");
      custom.required = false;
      custom.value = "";

    }

  }

  update();

  category.addEventListener("change", update);

}

/* ==========================================================
   AI Insights
========================================================== */

function initializeAIInsights() {

  const button = document.getElementById("generateAiBtn");
  const container = document.getElementById("aiInsightsBox");

  if (!button || !container) return;

  button.addEventListener("click", async () => {

    button.disabled = true;
    button.innerText = "Generating...";

    container.innerHTML = `
            <div class="text-center py-10 text-gray-500">
                🤖 Thinking...
            </div>
        `;

    try {

      const response = await fetch("/ai-insights");

      if (!response.ok) {
        throw new Error("Request failed");
      }

      const data = await response.json();

      if (!data.insights || data.insights.length === 0) {

        container.innerHTML = `
                    <div class="text-center py-8 text-gray-500">
                        No insights generated.
                    </div>
                `;

      } else {

        container.innerHTML = data.insights.map(insight => `
                    <div
                        class="border rounded-2xl p-4 mb-4 bg-slate-50"
                    >
                        <div class="flex gap-3">

                            <div class="text-2xl">
                                💡
                            </div>

                            <div>
                                ${insight}
                            </div>

                        </div>
                    </div>
                `).join("");

      }

    }

    catch (error) {

      console.error(error);

      container.innerHTML = `
                <div
                    class="rounded-xl bg-red-100 text-red-700 p-4"
                >
                    Failed to generate AI insights.
                </div>
            `;

    }

    finally {

      button.disabled = false;
      button.innerText = "Generate";

    }

  });

}