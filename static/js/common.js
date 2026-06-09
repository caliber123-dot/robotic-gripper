// let isDirty = false;
window.isDirty = window.isDirty || false;
// let allowUnload = false;
window.allowUnload = false;

function updateDirtyState() {
  let files = JSON.parse(localStorage.getItem("generatedFiles")) || [];
  isDirty = files.length > 0;
  console.log("==> isDirty", isDirty);
}

updateDirtyState();

// Internal navigation
document.addEventListener("click", function (e) {
  const link = e.target.closest("a");

  if (link) {
    const url = new URL(link.href);

    if (
      url.pathname === "/home" ||
      url.pathname === "/input" ||
      url.pathname === "/graph" ||
      url.pathname === "/comparison"
    ) {
      allowUnload = true;
    }
  }
});

// Refresh keys
window.addEventListener("keydown", function (e) {
  if (e.key === "F5" || (e.ctrlKey && e.key.toLowerCase() === "r")) {
    allowUnload = true;
  }
});

// Show warning
window.addEventListener("beforeunload", function (e) {
  if (allowUnload) {
    return;
  }

  if (isDirty) {
    e.preventDefault();
    e.returnValue = "";
  }
});
