import re
import requests
import time
from bs4 import BeautifulSoup

from config.log import getLogger
from database.connection import getConnection

logger = getLogger(__name__, "pipeline.log")


def searchPortal(name):
    #   Searches for a name on the UNESP faculty portal and returns the results HTML.
    if not name:
        return ""

    nameClean = re.sub(r"[.\-]", " ", name)
    nameClean = re.sub(r"[^\w\s]", "", nameClean)
    nameClean = re.sub(r"\s+", " ", nameClean).strip()

    url = "https://unesp.br/portaldocentes/docentes"

    r = requests.get(url, params={"termoBusca": nameClean}, timeout=15)
    r.raise_for_status()

    return r.text


def extractProfiles(html):
    #   Extracts profile links from the portal's search results.

    soup = BeautifulSoup(html, "html.parser")

    links = []
    for div in soup.find_all("div", class_="col-sm-7"):
        a = div.find("a")
        if (a) and (a.get("href")):
            links.append(a["href"])

    return list(set(links))


def fetchProfile(link):
    #   Retrieves the HTML page of the faculty member's profile.

    if not link.startswith("http"):
        link = "https://unesp.br" + link

    r = requests.get(link, timeout=15)
    r.raise_for_status()

    return r.text


def extractEmail(profileHTML):
    #   Extracts the institutional e-mail from the profile page.

    soup = BeautifulSoup(profileHTML, "html.parser")
    a = soup.find("a", id="email-docente")

    if (a) and (a.text):
        email = a.text.strip()

        if "unesp" in email:
            return email

    return None


def findContact(name):
    #   Finds a person's contact e-mail based on their name, searching the
    #   UNESP faculty portal and checking the first profile found.

    try:
        html = searchPortal(name)
        links = extractProfiles(html)

        for link in links:
            profileHTML = fetchProfile(link)
            email = extractEmail(profileHTML)

            if email:
                return email

    except Exception:
        logger.error(f'Unable to find "{name}"\'s contact.', exc_info=True)

    return ""


def findContactsForTable(table, nameColumn, sleepSeconds):
    #   Searchs for and updates the contact e-mail for each unverified name in a table.
    #   Reuses the contact information if the same name has already been verified.

    conn = getConnection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT DISTINCT {nameColumn} FROM {table} WHERE verified = 'no'")
    names = [row[0] for row in cursor.fetchall()]

    for count, name in enumerate(names, 1):
        cursor.execute(
            f"SELECT contact FROM {table} WHERE {nameColumn} = ? AND verified = 'yes'",
            (name,),
        )

        existingContact = cursor.fetchone()

        contact = existingContact[0] if existingContact else findContact(name)

        cursor.execute(
            f"UPDATE {table} SET contact = ?, verified = 'yes' WHERE {nameColumn} = ?",
            (contact, name),
        )

        logger.info(f"New {nameColumn} contact added. [{count} / {len(names)}]")

        time.sleep(sleepSeconds)

    conn.commit()
    conn.close()


def findContactsMulti():
    #   Searches for and updates pending contacts for advisors and authors.

    findContactsForTable("advisors", "advisor", 0.5)
    findContactsForTable("authors", "author", 0.25)
