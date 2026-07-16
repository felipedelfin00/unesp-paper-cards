import { filters } from "../state.js";
import { loadCatalog } from "../catalogController.js";


export function setupSelect(group, options, filterName, defaultLabel) {
    //  Configures a filter dropdown menu.
    //  Generates options dynamically based on API data.

    const button = group.querySelector(".filter__select");
    const menu = group.querySelector(".filter__select-options");
    const label = group.querySelector(".filter__select-label");
 
    label.dataset.default = defaultLabel;
    label.textContent = defaultLabel;
 
    menu.innerHTML = "";
 
    createOption("", "Todos");
    options.forEach(option => {
        if (typeof option === "object") {
            createOption(option.value, option.label);
        } else {
            createOption(option, option);
        }
    });
 
    button.addEventListener("click", (event) => {
        event.stopPropagation();
 
        //  Closes all currently open dropdowns before opening this one.
        document.querySelectorAll(".filter__select-options.show").forEach(select => {
            if (select !== menu) {
                select.classList.remove("show");
            }
        });
 
        menu.classList.toggle("show");
    });
 
    //  Closes this dropdown when clicking outside of it.
    document.addEventListener("click", () => {
        menu.classList.remove("show");
    });
 
    function createOption(value, text) {
        const div = document.createElement("div");
        div.className = "filter__select-option small-text";
        div.textContent = text;
 
        div.addEventListener("click", (event) => {
            event.stopPropagation();
            filters[filterName] = value;
            label.textContent = text;
            menu.classList.remove("show");
        });
 
        menu.appendChild(div);
    }
}

export function setupSDGFilters() {
    //  Configures the SDG filters. Each click toggles the selection.

    document.querySelectorAll(".filter__sdg-item").forEach(item => {
        item.addEventListener("click", () => {
            item.classList.toggle("selected");
            filters.sdg = Array.from(
                document.querySelectorAll(".filter__sdg-item.selected")
            ).map(el => el.dataset.sdg);
        });
    });
}

export function setupFilterActions() {
    //  Configures the button to apply and clean the filters.

    document.getElementById("apply-filter").addEventListener("click", applyFilters);
    document.getElementById("clear-filter").addEventListener("click", clearFilters);
}
 
export function setupFilterModal() {
    //  Configures the opening and closing of the filter modal.
    const overlay = document.getElementById("overlay");
 
    document.getElementById("button-filters").addEventListener("click", openFilters);
    document.getElementById("modal-close").addEventListener("click", closeFilters);
    overlay.addEventListener("click", (event) => {
        if (event.target === overlay) closeFilters();
    });
}
 
function openFilters() {
    document.body.style.overflow = "hidden";
    document.getElementById("overlay").style.display = "flex";
    document.getElementById("filter-modal").classList.remove("hidden");
    document.getElementById("overlay").scrollTop = 0;
}
 
function closeFilters() {
    document.body.style.overflow = "auto";
    document.getElementById("filter-modal").classList.add("hidden");
    document.getElementById("overlay").style.display = "none";
}

function applyFilters() {
    //  Reads the free-text field, applies the value to the filter state, and reloads.
    
    filters.knowledgeArea = document.getElementById("knowledgeArea").value.trim();
    filters.author = document.getElementById("author").value.trim();
    filters.advisor = document.getElementById("advisor").value.trim();
 
    loadCatalog();
    closeFilters();
}

function clearFilters() {
    //  Resets all filters to default and reloads.

    filters.knowledgeArea = "";
    filters.paperType = "";
    filters.language = "";
    filters.campus = "";
    filters.yearFrom = "";
    filters.yearTo = "";
    filters.author = "";
    filters.advisor = "";
    filters.sdg = [];
 
    document.querySelectorAll(".filter__select-label").forEach(label => {
        label.textContent = label.dataset.default;
    });
 
    document.querySelectorAll(".filter__sdg-item").forEach(item => {
        item.classList.remove("selected");
    });
 
    document.getElementById("knowledgeArea").value = "";
    document.getElementById("author").value = "";
    document.getElementById("advisor").value = "";
 
    loadCatalog();
    closeFilters();
}
