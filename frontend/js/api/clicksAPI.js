import { API_BASE_URL } from "../constants.js";

export async function registerClick(pid) {
    //  Registers a click on the "access full paper" button for the specified paper.

    try {
        await fetch(`${API_BASE_URL}/cards/${pid}/click`, {
            method: "POST",
            credentials: "include",
        });
    } catch (error) {
        console.error(error);
    }
}