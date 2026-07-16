import { API_BASE_URL } from "../constants.js";


export async function fetchFilterOptions() {
    //  Searches for all available options to populate the interface.

    const response = await fetch(`${API_BASE_URL}/filters`);
    return response.json();
}