// Save accessibility settings
function saveSettings() {
    const theme = document.getElementById("theme-toggle").value;
    const fontSize = document.getElementById("font-size-toggle").value;

    localStorage.setItem("theme", theme);
    localStorage.setItem("fontSize", fontSize);

    alert("Settings saved!");
    applySettings();
}

// Apply settings on page load
function applySettings() {
    const theme = localStorage.getItem("theme") || "light";
    const fontSize = localStorage.getItem("fontSize") || "medium";

    // Apply theme
    document.body.classList.remove("accessible-light", "accessible-dark", "accessible-high-contrast");
    document.body.classList.add(`accessible-${theme}`);

    // Apply font size
    document.body.classList.remove("font-small", "font-medium", "font-large", "font-xlarge");
    document.body.classList.add(`font-${fontSize}`);
}

// Reset to default settings
function resetSettings() {
    localStorage.removeItem("theme");
    localStorage.removeItem("fontSize");
    applySettings();
    alert("Settings reset to default!");
}

// Run on page load
document.addEventListener("DOMContentLoaded", applySettings);
