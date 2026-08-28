from vector_db.medical_db_builder import get_medical_database


def get_medical_retriever(k: int = 4):
    """
    Returns a retriever for the Medical Chroma Database.
    """

    vector_db = get_medical_database()

    retriever = vector_db.as_retriever(
        search_kwargs={
            "k": k
        }
    )

    return retriever


def retrieve_medical_documents(question: str, k: int = 4):
    """
    Retrieve relevant medical documents for a question.
    """

    retriever = get_medical_retriever(k)

    documents = retriever.invoke(question)

    return documents