from services.enrich.enrich import enrichPapers


def run(limit):
    #   Enriching step: generates additional data for pending papers.
    
    enrichPapers(limit)
