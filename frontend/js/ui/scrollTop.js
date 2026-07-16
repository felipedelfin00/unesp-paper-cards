const SCROLL_THRESHOLD = 400;

export function setupScrollToTop() {
    //  Configures the "scroll to top" button.

    const button = document.getElementById("scroll-top");
    if (!button) return;

    window.addEventListener("scroll", () => {
        button.classList.toggle("show", window.scrollY > SCROLL_THRESHOLD);
    });

    button.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}