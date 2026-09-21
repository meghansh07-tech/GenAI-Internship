from pathlib import Path

from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model


DB_DIRECTORY = Path("vector_db/chroma_db")


def get_vector_database():
    """
    Returns the Chroma vector database.
    """

    embedding_model = get_embedding_model()

    vector_db = Chroma(
        persist_directory=str(DB_DIRECTORY),
        embedding_function=embedding_model
    )

    return vector_db


def get_retriever(k: int = 4):
    """
    Returns a retriever object.
    """

    vector_db = get_vector_database()

    retriever = vector_db.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever