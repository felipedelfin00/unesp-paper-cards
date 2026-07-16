import json
import os
import re


def loadJSON(response):
    #   Parses a JSON string. If parsing fails, it attemps to extract
    #   only the first segment enclosed in braces and parse that. If all
    #   attemps fail, it returns an empty dictionary.

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        match = re.search(r"\{.*?\}", response, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())

            except json.JSONDecodeError:
                return {}

        return {}


def loadJSONL(path):
    #   Reads a JSONL file (one JSON object per line) and returns a
    #   object list. Invalid lines are silently ignored.

    papers = []

    if not os.path.exists(path):
        return papers

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                papers.append(json.loads(line))

            except json.JSONDecodeError:
                continue

        return papers
