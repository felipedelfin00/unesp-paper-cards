import argparse

from jobs import database, extract, transform, contacts, enrich

LIMIT_EXTRACT = 150
LIMIT_ENRICH = 100


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--database", action="store_true")
    parser.add_argument("--extract", action="store_true")
    parser.add_argument("--transform", action="store_true")
    parser.add_argument("--contacts", action="store_true")
    parser.add_argument("--enrich", action="store_true")
    parser.add_argument("--process", action="store_true")

    args = parser.parse_args()

    if args.database:
        database.run()

    if args.process:
        extract.run(LIMIT_EXTRACT)
        transform.run()
        contacts.run()
        enrich.run(LIMIT_ENRICH)
        return

    if args.extract:
        extract.run(LIMIT_EXTRACT)

    if args.transform:
        transform.run()

    if args.contacts:
        contacts.run()

    if args.enrich:
        enrich.run(LIMIT_ENRICH)


if __name__ == "__main__":
    main()
