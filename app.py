import streamlit as st

from research.research_chatbot import ResearchAssistant
from research.visualization import ConceptVisualizer

from chatbot.chatbot import ask_question
from chatbot.multimodal_chatbot import MultiModalAssistant
from chatbot.medical_chatbot import ask_medical_question


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="MultiModal AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ===================================================
# SESSION STATE
# ===================================================

if "assistant" not in st.session_state:
    st.session_state.assistant = MultiModalAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "PDF Chatbot"

if "research_assistant" not in st.session_state:
    st.session_state.research_assistant = ResearchAssistant()


assistant = st.session_state.assistant
research_assistant = st.session_state.research_assistant


# ===================================================
# TITLE
# ===================================================

st.title("🤖 MultiModal AI Assistant")

st.caption(
    "Task 1 • RAG Chatbot | "
    "Task 2 • Vision Language Model | "
    "Task 3 • Medical Q&A | "
    "Task 4 • AI Research Assistant | "
    "Task 5 • Sentiment-Aware Chatbot | "
    "Task 6 • Multilingual Chatbot"

)


# ===================================================
# SIDEBAR
# ===================================================

with st.sidebar:

    st.header("⚙️ Assistant")

    mode = st.radio(
        "Choose Mode",
        [
            "PDF Chatbot",
            "Image Assistant",
            "Medical Assistant",
            "Research Assistant"
        ]
    )

    st.session_state.mode = mode

    st.divider()

    if mode == "Image Assistant":

        uploaded_image = st.file_uploader(
            "Upload Image",
            type=[
                "jpg",
                "jpeg",
                "png",
                "webp"
            ]
        )

    else:

        uploaded_image = None

    st.divider()

    if st.button("🗑 Clear Conversation"):

        st.session_state.messages = []

        if mode == "Research Assistant":
            research_assistant.memory.clear()
        else:
            assistant.reset()

        st.rerun()


# ===================================================
# RESEARCH ASSISTANT UI
# ===================================================

if mode == "Research Assistant":

    st.header("🎓 AI Research Assistant")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔍 Search Papers",
            "💬 Research Chat",
            "🧠 Explain Concept",
            "📊 Visualization"
        ]
    )


    # ===================================================
    # TAB 1 — SEARCH PAPERS
    # ===================================================

    with tab1:

        st.subheader("🔍 Search arXiv Papers")

        search_query = st.text_input(
            "Enter a research topic",
            placeholder="e.g. Transformer, Computer Vision, Reinforcement Learning"
        )

        if st.button("Search Papers"):

            if search_query.strip():

                with st.spinner("Searching research database..."):

                    papers = research_assistant.search_papers(
                        search_query,
                        k=5
                    )

                if papers:

                    for index, paper in enumerate(papers):

                        st.markdown("---")

                        st.subheader(
                            f"{index + 1}. "
                            f"{paper.metadata.get('title', 'Unknown Title')}"
                        )

                        st.write(
                            f"**Authors:** "
                            f"{paper.metadata.get('authors', 'Unknown')}"
                        )

                        st.write(
                            f"**Categories:** "
                            f"{paper.metadata.get('categories', 'Unknown')}"
                        )

                        st.write(
                            f"**Published:** "
                            f"{paper.metadata.get('published', 'Unknown')}"
                        )

                        st.write(
                            f"**Paper ID:** "
                            f"{paper.metadata.get('paper_id', 'Unknown')}"
                        )

                        st.write(
                            paper.page_content[:800]
                        )

                        if st.button(
                            "📄 Summarize Paper",
                            key=f"summary_{index}"
                        ):

                            with st.spinner(
                                "Generating research summary..."
                            ):

                                summary = (
                                    research_assistant
                                    .summarize_paper(paper)
                                )

                            st.markdown("### 📝 Summary")

                            st.markdown(summary)

                else:

                    st.warning(
                        "No relevant papers were found."
                    )

            else:

                st.warning(
                    "Please enter a research topic."
                )


    # ===================================================
    # TAB 2 — RESEARCH CHAT
    # ===================================================

    with tab2:

        st.subheader("💬 Research Chat")

        st.write(
            "Ask complex questions about Computer Science research."
        )

        research_question = st.text_area(
            "Research Question",
            placeholder=(
                "Example: How does self-attention work "
                "in Transformer architectures?"
            )
        )

        if st.button("Ask Research Assistant"):

            if research_question.strip():

                with st.spinner(
                    "Searching research papers and generating answer..."
                ):

                    response = research_assistant.ask(
                        research_question
                    )

                st.markdown("### 🤖 Answer")

                st.markdown(response)

            else:

                st.warning(
                    "Please enter a research question."
                )


    # ===================================================
    # TAB 3 — CONCEPT EXPLAINER
    # ===================================================

    with tab3:

        st.subheader("🧠 Explain a Concept")

        concept = st.text_input(
            "Enter a Computer Science concept",
            placeholder="e.g. Transformer architecture"
        )

        if st.button("Explain Concept"):

            if concept.strip():

                with st.spinner(
                    "Generating explanation..."
                ):

                    explanation = (
                        research_assistant
                        .explain_concept(concept)
                    )

                st.markdown("### 📚 Explanation")

                st.markdown(explanation)

            else:

                st.warning(
                    "Please enter a concept."
                )


    # ===================================================
    # TAB 4 — VISUALIZATION
    # ===================================================

    with tab4:

        st.subheader("📊 Concept Visualization")

        graph_concept = st.text_input(
            "Concept to visualize",
            placeholder="e.g. Transformer"
        )

        if st.button("Generate Graph"):

            if graph_concept.strip():

                visualizer = ConceptVisualizer()

                figure = visualizer.create_graph(
                    graph_concept
                )

                st.pyplot(
                    figure,
                    clear_figure=True
                )

            else:

                st.warning(
                    "Please enter a concept."
                )


# ===================================================
# NORMAL CHAT MODES
# ===================================================

else:

    # ===================================================
    # DISPLAY OLD CHAT
    # ===================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    # ===================================================
    # CHAT INPUT
    # ===================================================

    prompt = st.chat_input(
        "Ask anything..."
    )


    if prompt:

        # -----------------------------
        # USER MESSAGE
        # -----------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)


        # -----------------------------
        # PDF CHATBOT
        # -----------------------------

        if mode == "PDF Chatbot":

            with st.spinner(
                "Searching knowledge base..."
            ):

                response = ask_question(
                    prompt
                )


        # -----------------------------
        # IMAGE ASSISTANT
        # -----------------------------

        elif mode == "Image Assistant":

            if uploaded_image is None:

                response = (
                    "Please upload an image first."
                )

            else:

                with st.spinner(
                    "Analyzing image..."
                ):

                    response = assistant.ask(
                        prompt,
                        uploaded_image
                    )


        # -----------------------------
        # MEDICAL ASSISTANT
        # -----------------------------

        else:

            with st.spinner(
                "Searching Medical Knowledge Base..."
            ):

                response = ask_medical_question(
                    prompt
                )


        # -----------------------------
        # ASSISTANT MESSAGE
        # -----------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                response
            )


# ===================================================
# IMAGE PREVIEW
# ===================================================

if (
    mode == "Image Assistant"
    and uploaded_image is not None
):

    st.divider()

    st.subheader(
        "🖼 Uploaded Image"
    )

    st.image(
        uploaded_image,
        use_container_width=True
    )


# ===================================================
# ASSISTANT STATUS
# ===================================================

st.sidebar.divider()

st.sidebar.subheader(
    "📊 Assistant Status"
)

if mode != "Research Assistant":

    status = assistant.get_status()

    st.sidebar.write(
        f"Image Loaded : "
        f"{'✅' if status['image_loaded'] else '❌'}"
    )

    st.sidebar.write(
        f"Conversation Length : "
        f"{status['conversation_length']}"
    )

else:

    history = research_assistant.history()

    st.sidebar.write(
        f"Research Messages : "
        f"{len(history)}"
    )


# ===================================================
# ABOUT
# ===================================================

st.sidebar.info(
    """
### 🚀 Features

✅ PDF RAG Chatbot

✅ Image Understanding

✅ Medical Q&A

✅ Research Paper Search

✅ Research Paper Summarization

✅ Concept Explanation

✅ Concept Visualization

✅ Multi-turn Research Conversation

✅ Multilingual Conversations

✅ Hindi • Spanish • French Support

✅ Language Switching

✅ Cross-lingual Context Retention

### Powered by

- LangChain
- Ollama
- ChromaDB
- HuggingFace Embeddings
- Streamlit
- NetworkX
"""
)


# ===================================================
# FOOTER
# ===================================================

st.divider()

st.caption(
    "Built with ❤️ using LangChain • Ollama • ChromaDB • Streamlit"
)