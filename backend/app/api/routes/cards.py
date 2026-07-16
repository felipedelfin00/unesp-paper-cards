import uuid as uuid_lib
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from config.log import getLogger
from api.repositories import getCards, getCard, addClick, getFilters

logger = getLogger(__name__, "api.log")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cards")
def readCards(
    offset: int = 0,
    q: str = None,
    knowledgeArea: str = None,
    paperType: str = None,
    yearFrom: int = None,
    yearTo: int = None,
    language: str = None,
    advisor: str = None,
    author: str = None,
    campus: str = None,
    sdg: str = None,
    sort: str = "newest",
):
    #   Lists paper cards with support for text search, filter combinations and sorting.
    offset = max(0, offset)

    if sort not in ["visits", "newest", "oldest", "random"]:
        sort = "newest"

    return getCards.getCards(
        offset,
        q,
        knowledgeArea,
        paperType,
        yearFrom,
        yearTo,
        language,
        advisor,
        author,
        campus,
        sdg,
        sort,
    )


@app.get("/cards/{pid}")
def readCard(pid: str):
    #   Returns the details of a card based on the ID.

    return getCard.getCard(pid)


@app.post("/cards/{pid}/click")
def registerClick(pid: str, request: Request, response: Response):
    #   Records a click on a card. Uses a cookie to identify unique users and prevent duplicate counting.
    clientID = request.cookies.get("clientID")

    if not clientID:
        clientID = str(uuid_lib.uuid4())
        response.set_cookie(
            key="clientID",
            value=clientID,
            max_age=31536000,  #   1 year
            httponly=True,
            samesite="Lax",
            secure=False,
        )

    success = addClick.addClick(pid, clientID)

    if not success:
        logger.info("Click ignored.")
        return {"status": "ignored"}

    logger.info("Click added.")
    return {"status": "ok"}


@app.get("/filters")
def filters():
    #   Returns the available filter values to populate the interface.

    return getFilters.getFilters()
