from pathlib import Path

from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model
from medical.xml_parser import load_medquad_documents


# Directory where the Medical Chroma DB will be stored
MEDICAL_DB_DIRECTORY = Path("vector_db/medical_db")


def build_medical_database():
    """
    Builds the Medical Chroma Database from the MedQuAD dataset.
    """

    print("Loading MedQuAD dataset...")

    documents = load_medquad_documents()

    print(f"Loaded {len(documents)} medical documents.")

    print("Loading embedding model...")

    embedding_model = get_embedding_model()

    print("Creating Chroma database...")

    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(MEDICAL_DB_DIRECTORY)
    )

    print("Medical Vector Database created successfully!")

    return vector_db


def get_medical_database():
    """
    Loads the already created Medical Chroma Database.
    """

    embedding_model = get_embedding_model()

    vector_db = Chroma(
        persist_directory=str(MEDICAL_DB_DIRECTORY),
        embedding_function=embedding_model
    )

    return vector_db