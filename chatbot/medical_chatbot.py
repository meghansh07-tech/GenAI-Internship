from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from medical.medical_retriever import retrieve_medical_documents
from medical.entity_extractor import extract_medical_entities


# ==================================================
# LLM
# ==================================================

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# ==================================================
# PROMPT
# ==================================================

prompt = ChatPromptTemplate.from_template(
    """
You are a careful Medical AI Assistant.

Answer the user's question using the retrieved medical
knowledge below.

STRICT RULES:

1. Use only information supported by the retrieved context.
2. Never diagnose the user.
3. Never assume that a symptom means the user has a disease.
4. Never prescribe medication or dosage.
5. Never invent medical facts.
6. If the context does not contain enough information, say:
   "I don't know based on the available medical knowledge."
7. If the user only reports a symptom such as:
   "I have fever"
   "I am suffering from fever"
   "I'm having a headache"

   answer about the symptom itself.

8. Do NOT list diseases merely because the symptom appears
   inside their descriptions.

9. If the user explicitly asks about a disease, answer about
   that disease using the retrieved context.

10. Keep the response concise and relevant.

11. Do not claim that the user has any disease.

12. Detected entities are only clues about the user's question.
    They are NOT diagnoses.

Detected Medical Entities:
{entities}

Retrieved Medical Context:
{context}

User Question:
{question}

Answer:
"""
)


# ==================================================
# DOCUMENT FORMATTER
# ==================================================

def format_docs(docs):

    if not docs:
        return "No relevant medical information was retrieved."

    return "\n\n".join(
        document.page_content
        for document in docs
    )


# ==================================================
# EXPLICIT DISEASE QUESTION DETECTION
# ==================================================

def is_explicit_disease_question(question: str):

    q = question.lower().strip()

    disease_question_patterns = [
        "what is ",
        "what are ",
        "what causes ",
        "how is ",
        "how are ",
        "symptoms of ",
        "treatment for ",
        "treatments for ",
        "diagnosis of ",
        "how to diagnose ",
        "causes of "
    ]

    return any(
        q.startswith(pattern)
        for pattern in disease_question_patterns
    )


# ==================================================
# GENERIC SYMPTOM QUESTION DETECTION
# ==================================================

def is_generic_symptom_question(question, entities):

    q = question.lower().strip()

    symptoms = entities.get("symptoms", [])

    if not symptoms:
        return False

    # Explicit disease-style questions should go to RAG.
    if is_explicit_disease_question(q):
        return False

    symptom_phrases = [
        "i have ",
        "i am having ",
        "i'm having ",
        "i am suffering from ",
        "i'm suffering from ",
        "i suffer from ",
        "i feel ",
        "i'm feeling ",
        "i am feeling ",
        "i've been having ",
        "i have been having ",
        "i am experiencing ",
        "i'm experiencing ",
        "experiencing ",
        "suffering from "
    ]

    return any(
        phrase in q
        for phrase in symptom_phrases
    )


# ==================================================
# GENERATE MEDICAL ANSWER
# ==================================================
def generate_medical_answer(question: str):

    entities = extract_medical_entities(question)

    # ------------------------------------------------
    # Retrieve relevant medical documents from ChromaDB
    # ------------------------------------------------

    documents = retrieve_medical_documents(
        question,
        k=6
    )

    # ------------------------------------------------
    # Format retrieved documents
    # ------------------------------------------------

    context = format_docs(documents)

    # ------------------------------------------------
    # Generate answer using retrieved context
    # ------------------------------------------------

    response = prompt.invoke(
        {
            "entities": entities,
            "context": context,
            "question": question
        }
    )

    # ------------------------------------------------
    # LLM response
    # ------------------------------------------------

    answer = llm.invoke(response)

    return StrOutputParser().invoke(answer)
# ==================================================
# PUBLIC FUNCTION
# ==================================================

def ask_medical_question(question: str):

    if not question or not question.strip():

        return "Please enter a medical question."

    return generate_medical_answer(
        question.strip()
    )