export const filters = {
    q: "",
    knowledgeArea: "",
    paperType: "",
    yearFrom: "",
    yearTo: "",
    language: "",
    advisor: "",
    author: "",
    campus: "",
    sdg: [],
    sort: "newest",
};

export const paginationState = {
    offset: 0,
    loading: false,
    hasMore: true,
};

export function resetPagination() {
    paginationState.offset = 0;
    paginationState.hasMore = true;
}