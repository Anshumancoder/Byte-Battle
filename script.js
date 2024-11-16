const searchInput = document.getElementById("searchInput");

searchInput.addEventListener("input", filterLinks);

function filterLinks() {
    const input = searchInput.value.toLowerCase();
    const navLinks = document.querySelectorAll("#navbarLinks .nav-item");

    navLinks.forEach(link => {
        const linkText = link.textContent.toLowerCase();
        link.style.display = linkText.includes(input) ? "" : "none";
    });
}
