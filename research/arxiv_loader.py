import json
from pathlib import Path

from langchain_core.documents import Document


ARXIV_FILE = Path("data/arxiv/arxiv-metadata-oai-snapshot.json")


def load_arxiv_documents(limit=5000):
    """
    Loads Computer Science papers from the arXiv dataset.

    Only the first 'limit' Computer Science papers are loaded.
    """

    documents = []

    with open(ARXIV_FILE, "r", encoding="utf-8") as file:

        for line in file:

            paper = json.loads(line)

            categories = paper.get("categories", "")

            # Keep only Computer Science papers
            if not categories.startswith("cs."):
                continue

            title = paper.get("title", "").strip()

            abstract = paper.get("abstract", "").strip()

            authors = paper.get("authors", "").strip()

            paper_id = paper.get("id", "")

            published = paper.get("update_date", "")

            document = Document(

                page_content=f"""
Title:
{title}

Abstract:
{abstract}
""",

                metadata={

                    "title": title,

                    "authors": authors,

                    "paper_id": paper_id,

                    "categories": categories,

                    "published": published
                }
            )

            documents.append(document)

            if len(documents) >= limit:
                break

    return documents