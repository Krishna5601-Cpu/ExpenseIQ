const toggleCustomCategory = () => {
  const select = document.querySelector("#categorySelect");
  const custom = document.querySelector("#customCategory");

  if (select.value === "custom") {
    custom.classList.remove("hidden");
  } else {
    custom.classList.add("hidden");
  }
};
