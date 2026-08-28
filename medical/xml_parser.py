import xml.etree.ElementTree as ET
from pathlib import Path

from langchain_core.documents import Document


MEDQUAD_DIRECTORY = Path("data/medquad")


def load_medquad_documents():
    """
    Loads every XML file from the MedQuAD dataset
    and converts it into LangChain Documents.
    """

    documents = []

    xml_files = list(MEDQUAD_DIRECTORY.rglob("*.xml"))

    print(f"Found {len(xml_files)} XML files.")

    for xml_file in xml_files:

        try:

            tree = ET.parse(xml_file)

            root = tree.getroot()

        except Exception:

            continue

        # Every XML contains many QA pairs
        for qa in root.findall(".//QAPair"):

            question = qa.findtext("Question")

            answer = qa.findtext("Answer")

            if question is None or answer is None:
                continue

            document = Document(

                page_content=f"""
Question:
{question}

Answer:
{answer}
""",

                metadata={
                    "source": str(xml_file)
                }

            )

            documents.append(document)

    print(f"Loaded {len(documents)} Question Answer pairs.")

    return documents