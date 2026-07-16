import { filters } from "../state.js";
import { loadCatalog } from "../catalogController.js";

let searchTimeout;

export function setupSearch() {
    //  Configure the text search. It uses a 300ms debounce to search only
    //  when the user stops typing.

    document.getElementById("search").addEventListener("input", handleSearch);
}

function handleSearch(event) {
    clearTimeout(searchTimeout);

    searchTimeout = setTimeout(() => {
        filters.q = event.target.value;
        loadCatalog();
    }, 300);
}