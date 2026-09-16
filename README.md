# 🤖 MultiModal AI Assistant — GenAI Internship Project

A multimodal and intelligent AI assistant developed as part of the **Generative AI Internship**. The project builds on a single training project and progressively extends it with Retrieval-Augmented Generation (RAG), vision-language capabilities, medical question answering, research assistance, sentiment analysis, and multilingual conversations.

## 🚀 Project Overview

The application is built using open-source AI models and frameworks and provides multiple AI capabilities through a Streamlit interface.

The project was developed incrementally across six internship tasks while maintaining the same core application.

### Completed Tasks

| Task   | Feature                   | Description                                                                                                                     |
| ------ | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Task 1 | 📚 RAG Chatbot            | Retrieves information from a document knowledge base using ChromaDB and generates context-aware answers.                        |
| Task 2 | 👁️ Vision Language Model | Enables the assistant to analyze and understand uploaded images.                                                                |
| Task 3 | 🏥 Medical Q&A            | Provides question answering using a medical knowledge base.                                                                     |
| Task 4 | 🔬 AI Research Assistant  | Supports research-paper search, summarization, concept explanation, and visualization.                                          |
| Task 5 | 😊 Sentiment Analysis     | Detects positive, negative, and neutral sentiment and adapts responses accordingly.                                             |
| Task 6 | 🌐 Multilingual Chatbot   | Supports multilingual conversations, language detection, translation, language switching, and conversational context retention. |

---

# ✨ Features

## 📚 1. Retrieval-Augmented Generation

The chatbot uses a vector database to retrieve relevant information before generating an answer.

### Pipeline

```text
User Question
      ↓
Embedding Model
      ↓
ChromaDB Vector Search
      ↓
Relevant Documents
      ↓
Llama 3.2
      ↓
Generated Response
```

The knowledge base can be updated with new documents without rebuilding the complete application.

---

## 👁️ 2. Vision Language Model

The application supports image-based interactions.

Users can upload an image and ask questions about its contents.

Supported image formats include:

* JPG
* JPEG
* PNG
* WEBP

The vision-language component uses an open-source model through Ollama.

---

## 🏥 3. Medical Question Answering

A dedicated medical knowledge base is used for medical-related questions.

The medical assistant retrieves relevant information from the medical vector database before generating an answer.

> The medical assistant is intended for informational purposes and should not replace professional medical advice.

---

# 🔬 4. AI Research Assistant

The research assistant provides several research-oriented capabilities.

### 🔍 Research Paper Search

Searches an indexed research-paper database and returns relevant papers.

### 📝 Paper Summarization

Generates summaries of retrieved research papers.

### 🧠 Concept Explanation

Explains Computer Science and AI concepts using the research assistant.

### 📊 Concept Visualization

Generates visual representations of selected concepts.

### 💬 Research Conversation

Maintains multi-turn research conversations using conversation memory.

---

# 😊 5. Sentiment-Aware Chatbot

The chatbot analyzes the sentiment of user messages using a sentiment classification model.

Supported sentiment categories:

* Positive
* Neutral
* Negative

The detected sentiment is used to adapt the response.

Example:

```text
User:
"I'm really frustrated because this isn't working."

↓ Sentiment Analysis

Negative

↓ Response Generation

The assistant provides a more appropriate and supportive response.
```

---

# 🌐 6. Multilingual Chatbot

The final internship task extends the chatbot to support multilingual conversations.

The multilingual system provides:

* Automatic language detection
* Translation to an internal English representation
* Cross-language conversation handling
* Context retention across language switches
* Translation of responses back into the detected language

Currently demonstrated languages include:

* 🇬🇧 English
* 🇮🇳 Hindi
* 🇪🇸 Spanish
* 🇫🇷 French

### Multilingual Pipeline

```text
User Message
      ↓
Language Detection
      ↓
Translation
      ↓
Conversation Context
      ↓
RAG Retrieval
      ↓
Llama 3.2
      ↓
Sentiment Analysis
      ↓
Response Translation
      ↓
User
```

### Example

```text
User:
What is machine learning?

Assistant:
[English response]

User:
अब इसे आसान भाषा में समझाओ।

Assistant:
[Hindi response]

User:
¿Puedes darme un ejemplo?

Assistant:
[Spanish response]
```

The conversation memory allows the assistant to retain context while the user changes languages.

---

# 🧠 Technologies Used

### AI / LLM

* Ollama
* Llama 3.2
* Qwen2.5-VL
* Hugging Face Transformers

### GenAI Frameworks

* LangChain
* LangChain Ollama
* LangChain Chroma

### Vector Database

* ChromaDB

### Embeddings

* Hugging Face embeddings
* Nomic embedding model

### Application

* Streamlit
* Python

### Research

* arXiv research-paper data
* NetworkX
* Matplotlib

---

# 📁 Project Structure

```text
GenAI-Internship/
│
├── app.py
│
├── chatbot/
│   ├── chatbot.py
│   ├── multimodal_chatbot.py
│   └── medical_chatbot.py
│
├── embeddings/
│   └── embedding_model.py
│
├── vector_db/
│   ├── chroma_db/
│   ├── medical_db/
│   ├── arxiv_db/
│   └── medical_db_builder.py
│
├── sentiment/
│   ├── __init__.py
│   └── sentiment_analyzer.py
│
├── multilingual/
│   ├── __init__.py
│   └── multilingual_handler.py
│
├── memory/
│   └── conversation_memory.py
│
├── models/
│   ├── llm_model.py
│   └── vision_model.py
│
├── research/
│   ├── research_chatbot.py
│   └── visualization.py
│
├── utils/
│   ├── document_loader.py
│   ├── image_processor.py
│   ├── updater.py
│   ├── scheduler.py
│   └── logger.py
│
├── notebooks/
│
├── report/
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/meghansh07-tech/GenAI-Internship.git
cd GenAI-Internship
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🦙 Ollama Setup

Install Ollama and make sure the required models are available.

Example:

```bash
ollama pull llama3.2
```

For the vision-language functionality, the required vision model should also be available through Ollama.

Start the Ollama server:

```bash
ollama serve
```

Keep the Ollama server running while using the application.

---

# ▶️ Running the Application

Start Streamlit from the project root:

```bash
streamlit run app.py
```

The application will open in the browser.

Use the sidebar to select between:

```text
PDF Chatbot
Image Assistant
Medical Assistant
Research Assistant
```

---

# 🧪 Testing

The major components were tested individually during development.

### RAG

The chatbot retrieves documents from ChromaDB and uses the retrieved context to generate answers.

### Sentiment

Messages were tested for positive, negative, and neutral sentiment detection.

### Multilingual

The multilingual pipeline was tested with language switching between:

```text
English → Hindi → Spanish
```

The assistant successfully generated responses in the corresponding languages while retaining conversation context.

---

# 🔄 Overall Architecture

```text
                       ┌─────────────────────┐
                       │   Streamlit UI      │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
              User Question               Image Input
                    │                           │
                    ↓                           ↓
          Multilingual Handler          Vision Assistant
                    │
                    ↓
            Language Detection
                    │
                    ↓
             Translation Layer
                    │
                    ↓
            Sentiment Analysis
                    │
                    ↓
             ChromaDB Retrieval
                    │
                    ↓
              Llama 3.2 LLM
                    │
                    ↓
            Conversation Memory
                    │
                    ↓
             Response Translation
                    │
                    ↓
                  User
```

---

# 🎯 Internship Outcome

The project demonstrates the progressive development of a single Generative AI application through six practical tasks.

The final system combines:

* Retrieval-Augmented Generation
* Vector databases
* Large Language Models
* Vision-language models
* Medical knowledge retrieval
* Research assistance
* Sentiment analysis
* Multilingual processing
* Conversation memory
* Streamlit application development

The project uses open-source models and frameworks and demonstrates their integration into a unified AI assistant.

---

# 👨‍💻 Author

**Meghansh Singh**

B.Tech — Civil Engineering
National Institute of Technology, Warangal

GitHub: `meghansh07-tech`

---

# 📌 Note

This project was developed as part of a Generative AI internship and is intended to demonstrate practical implementation and integration of Generative AI technologies.
