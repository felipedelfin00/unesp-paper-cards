import os
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from groq import Groq

from config.log import getLogger
from database.connection import getConnection
from services.enrich.prompt import buildPrompt
from utils.json import loadJSON
from utils.normalize import normalizeText

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VERSION = 1
MODEL = "openai/gpt-oss-120b"

logger = getLogger(__name__, "pipeline.log")


def callAI(prompt):
    #   Sends the prompt to the AI Model, returning the response as text.

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )

            return response.choices[0].message.content

        except Exception as e:
            if (hasattr(e, "status_code")) and (e.status_code == 429):
                raise RuntimeError("AI_LIMIT")

            if attempt == 2:
                raise

            time.sleep(5)


def enrichPapers(limit):
    #   Enriches pending papers using AI and updates the database.
    #   Halts execution if the AI limit is reached.

    conn = getConnection()
    cursor = conn.cursor()

    #   Selects papers with pending enrichment.
    cursor.execute(
        "SELECT id, title, abstract FROM papers WHERE status = 'transformed' OR (status = 'enriched' AND version < ?) LIMIT ?",
        (VERSION, limit),
    )

    rows = cursor.fetchall()

    if not rows:
        logger.warning("There is no paper to enrich.")
        conn.close()
        return

    count = 0

    for pid, title, abstract in rows:
        now = datetime.now(timezone.utc).isoformat()

        paper = {"id": pid, "title": title, "abstract": abstract}
        prompt = buildPrompt(paper)

        try:
            logger.info(f"Enriching paper. [{count + 1} / {len(rows)}]")

            response = callAI(prompt)
            logger.debug(response)
            data = loadJSON(response)

            cursor.execute(
                """
                UPDATE papers
                SET summary = ?,
                    socialRelevance = ?,
                    knowledgeArea = ?,
                    knowledgeAreaNorm = ?,
                    version = ?,
                    updatedAt = ?,
                    status = 'enriched',
                    theme = ?
                WHERE id = ?
                """,
                (
                    data.get("summary", ""),
                    data.get("socialRelevance", ""),
                    data.get("knowledgeArea", ""),
                    normalizeText(data.get("knowledgeArea", "")),
                    VERSION,
                    now,
                    data.get("theme", ""),
                    pid,
                ),
            )

            #   Remove the old SDG from the paper before adding the new ones.
            cursor.execute("DELETE FROM sdg WHERE paperID = ?", (pid,))

            for sdg in data.get("sdg", []):
                number = sdg.get("number")
                reason = sdg.get("reason", "")

                if number is None:
                    continue

                cursor.execute(
                    """
                    INSERT INTO sdg (paperID, sdg, reason)
                    VALUES (?, ?, ?)
                    """,
                    (pid, int(number), reason),
                )

            count += 1

            time.sleep(5)  #   Avoid exceeding AI's rate limit.

        except Exception as e:
            if str(e) == "AI_LIMIT":
                logger.warning("AI Limit reached.", exc_info=False)
                break
            else:
                logger.error("Unable to enrich paper.", exc_info=True)
                conn.close()
                raise

    conn.commit()
    conn.close()

    logger.info(f"{count} papers enriched.")
