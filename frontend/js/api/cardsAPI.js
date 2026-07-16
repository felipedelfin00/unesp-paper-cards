import { API_BASE_URL } from "../constants.js";


export async function fetchCards(filters, offset) {
    //  Retriaves a page of cards in the API, applying the specified filters.
    
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
        if (Array.isArray(value)) {
            if (value.length > 0) {
                params.set(key, value.join("||"));
            }
        } else if (value !== "") {
            params.append(key, value);
        }
    });

    params.set("offset", offset);

    const response = await fetch(`${API_BASE_URL}/cards?${params}`);
    return response.json();
}