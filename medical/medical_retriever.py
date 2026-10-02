from vector_db.medical_db_builder import get_medical_database
from medical.entity_extractor import extract_medical_entities


def get_medical_retriever(k: int = 6):
    vector_db = get_medical_database()

    return vector_db.as_retriever(
        search_kwargs={"k": k}
    )


def build_medical_search_queries(question: str):
    """
    Creates retrieval queries based on the medical entities detected
    in the user's natural-language question.
    """

    entities = extract_medical_entities(question)

    symptoms = entities.get("symptoms", [])
    diseases = entities.get("diseases", [])
    treatments = entities.get("treatments", [])

    queries = []

    # Specific disease mentioned
    if diseases:
        for disease in diseases:
            queries.append(f"What is {disease}?")
            queries.append(f"What are the symptoms of {disease}?")

    # Treatment mentioned
    if treatments:
        for treatment in treatments:
            queries.append(f"What is {treatment}?")

    # Generic symptom mentioned
    if symptoms:
        for symptom in symptoms:
            queries.append(f"What is {symptom}?")
            queries.append(f"What are the symptoms of {symptom}?")

    # Always keep the original question as a fallback
    queries.append(question)

    # Remove duplicates while preserving order
    unique_queries = []

    for query in queries:
        if query not in unique_queries:
            unique_queries.append(query)

    return unique_queries


def retrieve_medical_documents(question: str, k: int = 6):
    """
    Retrieves medical documents using normalized medical queries.
    """

    vector_db = get_medical_database()

    queries = build_medical_search_queries(question)

    all_documents = []

    for query in queries:

        documents = vector_db.similarity_search(
            query,
            k=k
        )

        all_documents.extend(documents)

    # Remove duplicate documents
    unique_documents = []
    seen = set()

    for document in all_documents:

        content = document.page_content.strip()

        if content not in seen:
            seen.add(content)
            unique_documents.append(document)

    return unique_documents[:k]