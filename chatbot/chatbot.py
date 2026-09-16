"""
chatbot/chatbot.py
LangChain 1.x + Ollama + Chroma (Base Version)
"""

from langchain_ollama import ChatOllama

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from vector_db.chroma_manager import get_vector_database
from sentiment.sentiment_analyzer import SentimentAnalyzer



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
#-------------------------
# Sentiment Analyser


sentiment_analyzer = SentimentAnalyzer()

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
    print("========== SENTIMENT ==========")

    sentiment_result = sentiment_analyzer.analyze(question)

    sentiment = sentiment_result["sentiment"]
    confidence = sentiment_result["confidence"]

    print(f"Sentiment: {sentiment}")
    print(f"Confidence: {confidence}")


    print("========== STEP 1 ==========")

    docs = retriever.invoke(question)

    print("========== STEP 2 ==========")
    print(f"Retrieved {len(docs)} documents")

    context = format_docs(docs)

    print("========== STEP 3 ==========")

    prompt_text = prompt.invoke({
        "context": context,
        "question": question
    })

    print("========== STEP 4 ==========")

    response = llm.invoke(prompt_text)

    print("========== STEP 5 ==========")

    response_text = response.content
    prefix = sentiment_analyzer.get_response_prefix(sentiment)

    return prefix + response_text




