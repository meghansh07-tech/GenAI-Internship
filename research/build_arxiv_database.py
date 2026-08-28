from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model
from research.arxiv_loader import load_arxiv_documents


DB_DIRECTORY = Path("vector_db/arxiv_db")


def build_arxiv_database():

    print("Loading arXiv Papers...")

    documents = load_arxiv_documents(limit=5000)

    print(f"Loaded {len(documents)} papers.")

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    embedding_model = get_embedding_model()

    print("Creating Chroma Database...")

    Chroma.from_documents(

        documents=chunks,

        embedding=embedding_model,

        persist_directory=str(DB_DIRECTORY)
    )

    print("\nResearch Database Created Successfully!")
    print("Database stored at:", DB_DIRECTORY)


if __name__ == "__main__":

    build_arxiv_database()