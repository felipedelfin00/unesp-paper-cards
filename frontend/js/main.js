import { paginationState } from "./state.js";
import { loadCatalog } from "./catalogController.js";
import { fetchFilterOptions } from "./api/filtersAPI.js";
import { setupSelect, setupSDGFilters, setupFilterActions, setupFilterModal } from "./ui/filtersUI.js";
import { setupSortButtons, setupSortDropdown } from "./ui/sortUI.js";
import { setupSearch } from "./ui/search.js";
import { setupScrollToTop } from "./ui/scrollTop.js";

const observer = new IntersectionObserver(async (entries) => {
    //  Infinite scroll observer. When the "sentinel" enters on the viewport,
    //  retriaves the next page of cards.

    if (!entries[0].isIntersecting) return;
    if (paginationState.loading || !paginationState.hasMore) return;

    paginationState.loading = true;
    await loadCatalog(false);
    paginationState.loading = false;
}, { rootMargin: "200px" });

async function init() {
    loadCatalog();

    setupSearch();
    setupSortButtons();
    setupSortDropdown();
    setupSDGFilters();
    setupFilterActions();
    setupFilterModal();
    setupScrollToTop();

    const filterData = await fetchFilterOptions();

    setupSelect(document.querySelector('[data-filter="paperType"]'), filterData.paperType, "paperType", "Selecione um tipo");
    setupSelect(document.querySelector('[data-filter="language"]'), filterData.language, "language", "Selecione um idioma");
    setupSelect(document.querySelector('[data-filter="campus"]'), filterData.campus, "campus", "Selecione um campus");
    setupSelect(document.querySelector('[data-filter="yearFrom"]'), filterData.yearIssued, "yearFrom", "Selecione um ano");
    setupSelect(document.querySelector('[data-filter="yearTo"]'), filterData.yearIssued, "yearTo", "Selecione um ano");

    observer.observe(document.getElementById("scroll-sentinel"));
}

document.addEventListener("DOMContentLoaded", init);