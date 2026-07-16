import { THEME_COLORS, LANGUAGES } from "../constants.js";
import { openCard } from "./cardModal.js";

export function renderCatalog(cards, container, append = false) {
    //  Renders the list of cards inside the specified container.
    //  If 'append' is true, it appends to the end.
    //  If 'append' is false, it replaces all current content.

    if (!append) {
        container.innerHTML = "";
    }

    if (cards.length === 0 && !append) {
        container.appendChild(createEmptyState());
        return;
    }

    cards.forEach(card => {
        container.appendChild(createCard(card));
    });
}

function createEmptyState() {
    const div = document.createElement("div");
    div.className = "empty-state";
    div.innerHTML = `
        <p class="medium-text bold">Nenhum trabalho encontrado</p>
        <p class="small-text dark-gray-text margin-smaller">Tente ajustar os filtros ou o termo de busca</p>
    `;

    return div;
}

function createCard(card) {
    //  Creates the DOM elemento for a single card.

    const color = THEME_COLORS[card.theme] ?? "gray";
    const lang = LANGUAGES[card.language] ?? "Indefinido";

    const div = document.createElement("div");
    div.className = `card ${color}-gradient`;
    div.dataset.id = card.id;
    div.innerHTML = `                               
        <div class="flex start">
            <div class="card__theme-icon ${color}-background">
                <img class="bigger-img" src="icons/themes/${card.theme}.svg">
            </div>
            <p class="text-medium bold">${card.title}</p>
        </div>
 
        <div class="margin-small">
            <p class="summary small-text dark-gray-text">${card.summary}</p>
        </div>
 
        <div class="card-info margin-medium">
            <p class="smaller-text semi-bold dark-gray-text">Área do conhecimento</p>
            <p class="small-text">${card.knowledgeArea}</p>
        </div>
 
        <div class="card-info margin-small">
            <p class="smaller-text semi-bold dark-gray-text">Tipo de trabalho</p>
            <p class="small-text">${card.paperType}</p>
        </div>
 
        <div class="margin-small flex" style="gap: 8px;">
            <div class="card-info" style="flex: 1;">
                <p class="smaller-text semi-bold dark-gray-text">Idioma</p>
                <p class="small-text">${lang}</p>
            </div>
            <div class="card-info" style="flex: 1;">
                <p class="smaller-text semi-bold dark-gray-text">Ano de emissão</p>
                <p class="small-text">${card.yearIssued}</p>
            </div>
        </div>
 
        <div class="card__button margin-medium flex">
            <p class="small-text semi-bold white-text">Ver detalhes</p>
            <img class="big-img" src="icons/arrow-right.svg">
        </div>
    `;

    div.querySelector(".card__button").addEventListener("click", () => openCard(card.id));

    return div;
}