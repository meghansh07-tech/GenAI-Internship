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
from multilingual.multilingual_handler import MultilingualHandler
from memory.conversation_memory import ConversationMemory




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
# Multilingual Support
# -------------------------

multilingual_handler = MultilingualHandler()

conversation_memory = ConversationMemory(
    max_history=10
)
# -------------------------
# Prompt
# -------------------------

prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

Use the conversation history to understand
references such as "it", "that", "this", or
previous questions.

Maintain the user's intent even when the
conversation contains multiple languages.

If the answer is not available in the context,
reply:

"I don't know."

Conversation History:
{history}

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

    # -------------------------
    # MULTILINGUAL INPUT
    # -------------------------

    print("========== MULTILINGUAL INPUT ==========")

    multilingual_result = (
        multilingual_handler.process_conversation_turn(
            question,
            conversation_memory
        )
    )

    detected_language = multilingual_result[
        "language_code"
    ]

    english_question = multilingual_result[
        "english_message"
    ]

    english_history = multilingual_result[
        "conversation_history"
    ]

    print(
        f"Detected language: "
        f"{multilingual_result['language_name']}"
    )

    print(
        f"English question: "
        f"{english_question}"
    )

    # -------------------------
    # SENTIMENT ANALYSIS
    # -------------------------

    print("========== SENTIMENT ==========")

    sentiment_result = sentiment_analyzer.analyze(
        question
    )

    sentiment = sentiment_result["sentiment"]
    confidence = sentiment_result["confidence"]

    print(f"Sentiment: {sentiment}")
    print(f"Confidence: {confidence}")

    # -------------------------
    # RETRIEVE DOCUMENTS
    # -------------------------

    print("========== STEP 1 ==========")

    docs = retriever.invoke(
        english_question
    )

    print("========== STEP 2 ==========")
    print(
        f"Retrieved {len(docs)} documents"
    )

    context = format_docs(docs)

    # -------------------------
    # GENERATE RESPONSE
    # -------------------------

    print("========== STEP 3 ==========")

    prompt_text = prompt.invoke({
        "history": english_history,
        "context": context,
        "question": english_question
    })

    print("========== STEP 4 ==========")

    response = llm.invoke(prompt_text)

    print("========== STEP 5 ==========")

    response_text = response.content

    # -------------------------
    # SENTIMENT RESPONSE
    # -------------------------

    prefix = sentiment_analyzer.get_response_prefix(
        sentiment
    )

    response_text = prefix + response_text

    # -------------------------
    # TRANSLATE RESPONSE
    # -------------------------

    print("========== TRANSLATION ==========")

    final_response = (
        multilingual_handler.process_response(
            response_text,
            detected_language
        )
    )

    # -------------------------
    # UPDATE MEMORY
    # -------------------------

    conversation_memory.add_user_message(
        english_question
    )

    conversation_memory.add_assistant_message(
        response_text
    )

    return final_response





