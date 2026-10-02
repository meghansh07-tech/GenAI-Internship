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
# WARM MODERN UI STYLING
# ===================================================

st.markdown("""
<style>

    /* =========================
       MAIN APP BACKGROUND
       ========================= */

    .stApp {
        background:
            radial-gradient(circle at 85% 10%,
                rgba(255, 184, 77, 0.28),
                transparent 32%),
            radial-gradient(circle at 50% 80%,
                rgba(255, 218, 128, 0.22),
                transparent 35%),
            linear-gradient(
                135deg,
                #fff8e7 0%,
                #fff4dc 35%,
                #fff0df 65%,
                #ffe8d2 100%
            ) !important;

        color: #35220f !important;
    }


    /* =========================
       MAIN CONTENT
       ========================= */

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }


    /* =========================
       TEXT
       ========================= */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label {
        color: #3d2a16;
    }

    .stMarkdown p {
        color: #5a4024 !important;
    }


    /* =========================
       HEADINGS
       ========================= */

    h1 {
        font-size: 2.25rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.7px;

        color: #8a3f00 !important;

        margin-bottom: 0.25rem !important;
    }

    h2 {
        font-weight: 700 !important;
        color: #7a3b00 !important;
    }

    h3 {
        font-weight: 650 !important;
        color: #63330d !important;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #fff3cf 0%,
                #fff0d8 45%,
                #ffe6d2 100%
            ) !important;

        border-right: 1px solid #f2c27b;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] * {
        color: #542d0c !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #f1c98d !important;
    }


    /* =========================
       SIDEBAR RADIO OPTIONS
       ========================= */

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 8px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {

        background:
            rgba(255, 255, 255, 0.72) !important;

        border: 1px solid #f3d4a5;

        border-radius: 13px;

        padding: 10px 12px;

        color: #542d0c !important;

        transition: all 0.2s ease;

        box-shadow:
            0 3px 10px rgba(160, 91, 20, 0.05);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:hover {

        background: #fff7e8 !important;

        border-color: #f4a340;

        transform: translateX(2px);

        box-shadow:
            0 5px 15px rgba(230, 126, 34, 0.12);
    }


    /* =========================
       BUTTONS
       ========================= */

    .stButton > button {

        border-radius: 11px !important;

        border: 1px solid #f1c27d !important;

        background:
            linear-gradient(
                135deg,
                #fffdf7,
                #fff4df
            ) !important;

        color: #713900 !important;

        font-weight: 600 !important;

        min-height: 40px;

        transition: all 0.2s ease;
    }

    .stButton > button:hover {

        border-color: #e88921 !important;

        background:
            linear-gradient(
                135deg,
                #fff1cf,
                #ffe2b5
            ) !important;

        color: #a44800 !important;

        transform: translateY(-1px);

        box-shadow:
            0 5px 14px rgba(225, 126, 34, 0.16);
    }


    /* =========================
       INPUTS
       ========================= */

    div[data-baseweb="input"],
    div[data-baseweb="textarea"] {
        border-radius: 13px !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {

        border-radius: 13px !important;

        border: 1px solid #efc27e !important;

        background: rgba(255,255,255,0.92) !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {

        color: #3d2a16 !important;

        background: transparent !important;
    }

    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {

        color: #b38b62 !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {

        border-color: #ed922c !important;

        box-shadow:
            0 0 0 3px rgba(245, 158, 11, 0.13);
    }


    /* =========================
       CHAT MESSAGES
       ========================= */

    [data-testid="stChatMessage"] {

        border-radius: 16px !important;

        padding: 12px 15px;

        margin: 9px 0;

        border: 1px solid #f0d19f !important;

        background:
            rgba(255,255,255,0.88) !important;

        box-shadow:
            0 4px 15px rgba(135, 78, 18, 0.055);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {

        color: #3d2a16 !important;
    }


    /* =========================
       USER MESSAGE
       ========================= */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {

        background:
            linear-gradient(
                135deg,
                #fff0c9,
                #ffe3bd
            ) !important;

        border-color: #f4c56f !important;
    }


    /* =========================
       CHAT INPUT
       ========================= */

    [data-testid="stChatInput"] {
        margin-top: 15px;
    }

    [data-testid="stChatInput"] > div {

        border-radius: 16px !important;

        border: 1.5px solid #efa646 !important;

        background:
            rgba(255,255,255,0.95) !important;

        box-shadow:
            0 6px 24px rgba(190, 105, 20, 0.12);
    }

    [data-testid="stChatInput"] textarea {

        color: #3d2a16 !important;

        font-size: 14px;
    }

    [data-testid="stChatInput"] textarea::placeholder {

        color: #b99a76 !important;
    }


    /* =========================
       TABS
       ========================= */

    button[data-baseweb="tab"] {

        font-weight: 600 !important;

        color: #8a6949 !important;

        padding: 10px 18px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {

        color: #d96500 !important;
    }

    div[data-baseweb="tab-highlight"] {

        background: #f28c28 !important;

        height: 3px;
    }


    /* =========================
       FILE UPLOADER
       ========================= */

    [data-testid="stFileUploader"] {

        background:
            rgba(255, 247, 229, 0.85) !important;

        border: 1px dashed #e9a34d !important;

        border-radius: 13px;

        padding: 8px;
    }

    [data-testid="stFileUploader"] * {

        color: #68401d !important;
    }


    /* =========================
       ALERTS
       ========================= */

    div[data-testid="stAlert"] {

        border-radius: 12px !important;

        border-left: 4px solid #f28c28 !important;
    }


    /* =========================
       RESEARCH PAPER CARDS
       ========================= */

    .paper-result {

        background:
            rgba(255,255,255,0.9);

        border: 1px solid #f0c987;

        border-radius: 15px;

        padding: 18px;

        margin: 12px 0;

        box-shadow:
            0 4px 14px rgba(150, 85, 20, 0.055);

        transition: all 0.2s ease;
    }

    .paper-result:hover {

        border-color: #efa13b;

        box-shadow:
            0 8px 22px rgba(210, 112, 20, 0.12);

        transform: translateY(-2px);
    }

    .paper-title {

        font-size: 17px;

        font-weight: 700;

        color: #713600 !important;
    }

    .paper-meta {

        color: #947250 !important;

        font-size: 12px;

        margin-top: 5px;
    }


    /* =========================
       DIVIDERS
       ========================= */

    hr {
        border-color: #edc98e !important;
    }


    /* =========================
       IMAGE
       ========================= */

    [data-testid="stImage"] img {

        border-radius: 15px;

        border: 1px solid #efc786;

        box-shadow:
            0 6px 20px rgba(150, 80, 15, 0.08);
    }


    /* =========================
       STATUS
       ========================= */

    div[data-testid="stStatusWidget"] {

        border-radius: 12px !important;

        border: 1px solid #efc27e !important;

        background: rgba(255,250,238,0.9) !important;
    }


    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        h1 {
            font-size: 1.8rem !important;
        }
    }

</style>
""", unsafe_allow_html=True)



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