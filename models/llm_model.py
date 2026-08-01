from langchain_ollama import ChatOllama


def get_llm():
    """
    Returns the primary text LLM.

    This model is used for:
    - Task 1 RAG Chatbot
    - Task 2 Multi-modal Assistant
    - Future Tasks (Medical QA, Research Assistant, etc.)
    """

    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0.2
    )

    return llm