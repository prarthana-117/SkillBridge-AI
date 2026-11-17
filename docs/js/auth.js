/* ==========================================================================
   SkillBridge AI - login & register forms
   ========================================================================== */
const form = document.getElementById("authForm");
const errorBox = document.getElementById("error");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.classList.add("hidden");
  const button = form.querySelector("button");
  button.disabled = true;

  const body = Object.fromEntries(new FormData(form));
  try {
    await api(`/api/${form.dataset.mode}`, body);
    location.href = "app.html";
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.classList.remove("hidden");
    button.disabled = false;
  }
});
