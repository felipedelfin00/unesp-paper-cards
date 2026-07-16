import { API_BASE_URL, THEME_COLORS, LANGUAGES, SDG_LABELS } from "../constants.js";
import { registerClick } from "../api/clicksAPI.js";

export async function openCard(id) {
    //  Opens the card modal: retriaves the full paper data from the API
    //  and builds the entire content.

    const response = await fetch(`${API_BASE_URL}/cards/${id}`);
    const card = await response.json();
    const modal = document.getElementById("card-modal");

    const color = THEME_COLORS[card.theme] ?? "gray";
    const lang = LANGUAGES[card.language] ?? "Indefinido";

    modal.innerHTML = `
        <div class="flex end">
            <div class="modal__close">
                <img class="bigger-img" src="icons/x.svg">
            </div>
        </div>
 
        <div class="content">
            <div class="flex start">
                <div class="card-modal__icon ${color}-background">
                    <img class="way-bigger-img" src="icons/themes/${card.theme}.svg">
                </div>
                <p class="big-text bold">${card.title}</p>
            </div>
 
            <div class="margin-big">
                <p class="small-text bold">Resumo</p>
                <p class="small-text dark-gray-text margin-smaller">${card.summary}</p>
            </div>
 
            <div class="margin-medium">
                <p class="small-text bold">Relevância para a sociedade</p>
                <p class="small-text dark-gray-text margin-smaller">${card.socialRelevance}</p>
            </div>
 
            <div class="margin-medium" id="card-modal__sdg">
            </div>

            ${card.keywords.length > 0 ? 
                `<div class="margin-medium">
                    <p class="small-text bold">Palavras-chave</p>
                    <div class="card-modal__keywords margin-smaller flex start" id="card-modal__keywords">
                    </div>
                </div>`
            : ""}
            
            <div class="margin-medium">
                <p class="small-text bold">Informações acadêmicas</p>
 
                <div class="margin-smaller flex" style="gap: 8px;">
                    <div class="card-modal__block">
                        <p class="smaller-text dark-gray-text semi-bold">Área do conhecimento</p>
                        <p class="small-text">${card.knowledgeArea}</p>
                    </div>
                    <div class="card-modal__block">
                        <p class="smaller-text dark-gray-text semi-bold">Idioma</p>
                        <p class="small-text">${lang}</p>
                    </div>
                </div>
 
                <div class="margin-small flex" style="gap: 8px;">
                    <div class="card-modal__block">
                        <p class="smaller-text dark-gray-text semi-bold">Tipo de trabalho</p>
                        <p class="small-text">${card.paperType}</p>
                    </div>
                    <div class="card-modal__block">
                        <p class="smaller-text dark-gray-text" semi-bold>Ano de emissão</p>
                        <p class="small-text">${card.yearIssued}</p>
                    </div>
                </div>
            </div>
 
            <div class="card-modal__block margin-small" id="card-modal__campuses">
            </div>
 
            <div class="card-modal__block margin-small" id="card-modal__authors">
            </div>
 
            ${card.advisors.length > 0 ?
                `<div class="card-modal__block margin-small" id="card-modal__advisors">
                </div>`
            : ""}
 
            <div class="card-modal__button margin-big flex ">
                <p class="small-text white-text semi-bold">Acessar trabalho completo</p>
                <img class="big-img" src="icons/external-link.svg">
            </div>
        </div>
    `;

    //  SDG
    const sdg = document.getElementById("card-modal__sdg");
    sdg.innerHTML = `<p class="small-text bold">Objetivos de Desenvolvimento Sustentável</p>`;
    card.sdg.forEach(item => {
        const sdgName = SDG_LABELS[item.number];

        const div = document.createElement("div");
        div.className = `card-modal__sdg margin-small light-background-sdg-${item.number} flex `;
        div.innerHTML = `
            <div class="flex start" style="flex: 1;">
                <img class="card__sdg-icon" src="icons/sdg/sdg${item.number}.png">
                <div>
                    <p class="medium-text semi-bold text-sdg-${item.number}">ODS ${item.number}</p>
                    <p class="small-text">${sdgName}</p>
                </div>
            </div>
 
            <div style="flex: 2;">
                <p class="small-text">${item.reason}</p>
            </div>
        `;
 
        sdg.appendChild(div);
    });

    //  Keywords
    if (card.keywords.length > 0) {
        const keywords = document.getElementById("card-modal__keywords");
        keywords.innerHTML = "";
    
        const maxKeywords = 5;
        card.keywords.slice(0, maxKeywords).forEach(keyword => {
            const tag = document.createElement("div");
            tag.className = "card-modal__keyword smaller-text semi-bold";
            tag.textContent = keyword;
            keywords.appendChild(tag);
        });
    
        const remainingKeywords = card.keywords.length - maxKeywords;
        if (remainingKeywords > 0) {
            const tag = document.createElement("div");
            tag.className = "card-modal__keyword smaller-text semi-bold";
            tag.textContent = `+${remainingKeywords}`;
            keywords.appendChild(tag);
        }
    }

    //  Campuses
    const campuses = document.getElementById("card-modal__campuses");
    campuses.innerHTML = `<p class="smaller-text dark-gray-text semi-bold">Camp${card.campuses.length === 1 ? "us" : "i"}</p>`;
 
    card.campuses.forEach(campus => {
        const tag = document.createElement("p");
        tag.className = "small-text";
        tag.textContent = campus;
        campuses.appendChild(tag);
    });

    //  Authors and advisors
    fillPeople(document.getElementById("card-modal__authors"), "Autor", card.authors, "author");

    if (card.advisors.length > 0) {
        fillPeople(document.getElementById("card-modal__advisors"), "Orientador", card.advisors, "advisor");
    }

    //  Link
    document.querySelector(".card-modal__button").addEventListener("click", () => {
        registerClick(card.id);
        openPaper(card.link);
    });

    //  Close modal
    document.querySelector(".modal__close").addEventListener("click", closeCard);
    document.querySelector(".overlay").addEventListener("click", (event) => {
        if (event.target === document.querySelector(".overlay")) closeCard();
    });
 
    document.body.style.overflow = "hidden";
    document.getElementById("overlay").style.display = "flex";
    document.getElementById("card-modal").classList.remove("hidden");
    document.getElementById("overlay").scrollTop = 0;
}

function fillPeople(container, title, people, field) {
    //  Fill a section with people in the modal.

    container.innerHTML = `<p class="smaller-text dark-gray-text semi-bold">${title}${people.length === 1 ? "" : "es"}</p>`;
 
    const maxPeople = 10;
 
    people.slice(0, maxPeople).forEach(person => {
        const div = document.createElement("div");
        div.className = "flex";
 
        div.innerHTML = `
            <p class="small-text">${person[field]}</p>
 
            ${
                person.contact
                ? ` <a href="mailto:${person.contact}" title="Enviar e-mail">
                        <img class="less-bigger-img" src="icons/mail-plus.svg" alt="Enviar e-mail">
                    </a>
                `
                : ""
            }
        `;
 
        container.appendChild(div);
    });
 
    const peopleRemaining = people.length - maxPeople;
 
    if (peopleRemaining > 0) {
        const p = document.createElement("p");
        p.className = "small-text gray-text";
        p.textContent = `+${peopleRemaining} ${title}${peopleRemaining === 1 ? "" : "es"}`;
        container.appendChild(p);
    }
}

function openPaper(link) {
    //  Opens the external link to the full paper in a new tab.

    if (!link) return;
    window.open(link, "_blank", "noopener,noreferrer");
}

function closeCard() {
    //  Closes the card modal.

    document.body.style.overflow = "auto";
    document.getElementById("overlay").style.display = "none";
    document.getElementById("card-modal").classList.add("hidden");
}