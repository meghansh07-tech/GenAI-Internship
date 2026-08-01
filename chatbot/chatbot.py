"""
chatbot/chatbot.py
LangChain 1.x + Ollama + Chroma (Base Version)
"""

from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from vector_db.chroma_manager import get_vector_database


# -------------------------
# Load Vector Database
# -------------------------

vector_db = get_vector_database()

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": 4
    }
)


# -------------------------
# LLM
# -------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# -------------------------
# Prompt
# -------------------------

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
reply:

"I don't know."

Context:
{context}

Question:
{question}
"""
)


# -------------------------
# Format Retrieved Docs
# -------------------------

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


# -------------------------
# LCEL RAG Pipeline
# -------------------------

rag_chain = (

    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }

    | prompt

    | llm

    | StrOutputParser()

)


# -------------------------
# Chat Function
# -------------------------

def ask_question(question: str):
    docs = retriever.invoke(question)

    print("=" * 50)

    for doc in docs:
        print(doc.page_content[:300])

    print("=" * 50)

    return rag_chain.invoke(question)