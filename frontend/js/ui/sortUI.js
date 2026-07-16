import { filters } from "../state.js";
import { loadCatalog } from "../catalogController.js";
 

export function setupSortDropdown() {
    //  Configures the sorting dropdown.

    const select = document.getElementById("select-sort");
    const options = document.getElementById("sort-options");
 
    select.addEventListener("click", (event) => {
        event.stopPropagation();
        options.classList.toggle("show");
    });
 
    document.addEventListener("click", () => {
        options.classList.remove("show");
    });
}

export function setupSortButtons() {
    //  Configure the sorting buttons. Each click updates the sorting filter,
    //  the shown label, and reloads.

    const options = [
        { id: "newest", label: "Mais recentes" },
        { id: "oldest", label: "Mais antigos" },
        { id: "visits", label: "Mais acessados" },
        { id: "random", label: "Aleatório" },
    ];
 
    options.forEach(({ id, label }) => {
        document.getElementById(id).addEventListener("click", () => changeSort(id, label));
    });
}
 
function changeSort(sort, label) {
    filters.sort = sort;
    document.getElementById("current-sort").textContent = label;
    loadCatalog();
}
