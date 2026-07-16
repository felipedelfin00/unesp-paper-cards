import { PAGE_SIZE } from "./constants.js";
import { filters, paginationState, resetPagination } from "./state.js";
import { fetchCards } from "./api/cardsAPI.js";
import { renderCatalog } from "./ui/cardRenderer.js";


export async function loadCatalog(reset = true) {
    //  Loads the card catalog based on the current filters / state.

    try {
        if (reset) {
            window.scrollTo({ top: 0, behavior: "instant" });
            resetPagination();
        }

        const data = await fetchCards(filters, paginationState.offset);
        const container = document.getElementById("cards");

        document.getElementById("paper-count").innerHTML = data.total;
        renderCatalog(data.items, container, !reset);

        paginationState.offset += data.items.length;
        paginationState.hasMore = data.items.length === PAGE_SIZE;
    } catch (error) {
        console.error(error);
    }
}