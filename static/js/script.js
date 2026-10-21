// Small enhancements only. The profile card itself is rendered by Flask.
const bio = document.getElementById("bio");
const counter = document.getElementById("counter");
if (bio && counter) {
  const update = () => { counter.textContent = bio.value.length + " / 250"; };
  bio.addEventListener("input", update);
  update();
}

// Reset must clear fields even though Flask pre-filled them after an error.
const resetBtn = document.getElementById("resetBtn");
if (resetBtn) {
  resetBtn.addEventListener("click", () => {
    document.querySelectorAll("#profileForm input, #profileForm textarea")
      .forEach((el) => { el.value = ""; });
    if (bio) bio.dispatchEvent(new Event("input"));
  });
}

// Show the default avatar if the image URL fails to load.
const avatar = document.getElementById("avatar");
if (avatar) {
  avatar.addEventListener("error", () => {
    avatar.src = avatar.dataset.fallback;
  }, { once: true });
}
