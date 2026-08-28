from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from medical.medical_retriever import get_medical_retriever
from medical.entity_extractor import extract_medical_entities


retriever = get_medical_retriever()

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)

prompt = ChatPromptTemplate.from_template(
"""
You are a Medical AI Assistant.

Use ONLY the retrieved medical context.

If the answer is unavailable, say:

"I don't know based on the available medical knowledge."

Medical Context:
{context}

Detected Medical Entities:
{entities}

User Question:
{question}
"""
)


def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


medical_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
        "entities": lambda question: extract_medical_entities(question),
    }

    | prompt

    | llm

    | StrOutputParser()
)


def ask_medical_question(question):
    return medical_chain.invoke(question)