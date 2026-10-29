import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st

from research.research_chatbot import ResearchAssistant
from research.visualization import ConceptVisualizer

from chatbot.chatbot import ask_question
from chatbot.multimodal_chatbot import MultiModalAssistant
from chatbot.medical_chatbot import ask_medical_question
from pathlib import Path


# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="Syntheia AI — Research Intelligence",
    page_icon=str(
        Path(__file__).resolve().parent / "syntheia_page_icon.png"
    ),
    layout="wide"
)

logo_path = Path(__file__).resolve().parent / "Syntheia.png"

st.image(
    str(logo_path),
    width=220
)

# ===================================================
# WARM MODERN UI STYLING
# ===================================================

st.markdown("""
<style>
:root {
    --pm-bg: #080b12;
    --pm-panel: #0f141d;
    --pm-panel-2: #121925;
    --pm-border: rgba(255,255,255,.09);
    --pm-text: #eef2f7;
    --pm-muted: #8e9aaa;
    --pm-accent: #8b5cf6;
    --pm-accent-2: #6366f1;
}
.stApp { background: radial-gradient(circle at 80% 0%, rgba(99,102,241,.13), transparent 30%), radial-gradient(circle at 10% 80%, rgba(139,92,246,.09), transparent 28%), var(--pm-bg) !important; color: var(--pm-text) !important; }
.block-container { max-width: 1380px; padding-top: 1.2rem; padding-bottom: 2rem; }
.stApp, .stApp p, .stApp span, .stApp label, .stApp div { color: var(--pm-text); }
.stMarkdown p { color: #c3cbd6 !important; }
h1,h2,h3 { color: #f7f8fb !important; letter-spacing: -.5px; }
h1 { font-size: 2.25rem !important; font-weight: 750 !important; }
h2 { font-weight: 700 !important; }
h3 { font-weight: 650 !important; }
section[data-testid="stSidebar"] { background: #0b0f16 !important; border-right: 1px solid var(--pm-border); }
section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }
section[data-testid="stSidebar"] * { color: #d8dee8 !important; }
section[data-testid="stSidebar"] hr, hr { border-color: var(--pm-border) !important; }
section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 7px; }
section[data-testid="stSidebar"] div[role="radiogroup"] label { background: rgba(255,255,255,.025) !important; border: 1px solid var(--pm-border); border-radius: 12px; padding: 9px 11px; transition: .2s; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(139,92,246,.10) !important; border-color: rgba(139,92,246,.35); }
.stButton > button { border-radius: 10px !important; border: 1px solid var(--pm-border) !important; background: #121925 !important; color: #e8ecf2 !important; font-weight: 600 !important; min-height: 40px; transition: .2s; }
.stButton > button:hover { border-color: rgba(139,92,246,.55) !important; background: #171f2e !important; transform: translateY(-1px); box-shadow: 0 7px 24px rgba(0,0,0,.25); }
div[data-baseweb="input"], div[data-baseweb="textarea"] { border-radius: 12px !important; }
div[data-baseweb="input"] > div, div[data-baseweb="textarea"] > div { border-radius: 12px !important; border: 1px solid var(--pm-border) !important; background: #0f141d !important; }
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea { color: #edf1f7 !important; background: transparent !important; }
div[data-baseweb="input"] input::placeholder, div[data-baseweb="textarea"] textarea::placeholder { color: #687587 !important; }
div[data-baseweb="input"] > div:focus-within, div[data-baseweb="textarea"] > div:focus-within { border-color: rgba(139,92,246,.75) !important; box-shadow: 0 0 0 3px rgba(139,92,246,.10); }
[data-testid="stChatMessage"] { border-radius: 15px !important; padding: 12px 15px; margin: 9px 0; border: 1px solid var(--pm-border) !important; background: #0f141d !important; box-shadow: 0 8px 25px rgba(0,0,0,.14); }
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span, [data-testid="stChatMessage"] div { color: #e4e9f0 !important; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background: linear-gradient(135deg,#151a27,#111724) !important; border-color: rgba(99,102,241,.25) !important; }
[data-testid="stChatInput"] { margin-top: 15px; }
[data-testid="stChatInput"] > div { border-radius: 16px !important; border: 1px solid rgba(139,92,246,.55) !important; background: #0f141d !important; box-shadow: 0 8px 30px rgba(0,0,0,.25); }
[data-testid="stChatInput"] textarea { color: #edf1f7 !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #687587 !important; }
button[data-baseweb="tab"] { font-weight: 600 !important; color: #7f8b9b !important; padding: 10px 18px; }
button[data-baseweb="tab"][aria-selected="true"] { color: #c4b5fd !important; }
div[data-baseweb="tab-highlight"] { background: #8b5cf6 !important; height: 3px; }
[data-testid="stFileUploader"] { background: #0f141d !important; border: 1px dashed rgba(139,92,246,.45) !important; border-radius: 13px; padding: 8px; }
[data-testid="stFileUploader"] * { color: #cdd5df !important; }
div[data-testid="stAlert"] { border-radius: 12px !important; border-left: 4px solid #8b5cf6 !important; background: #101722 !important; }
.paper-result { background: linear-gradient(145deg,#101620,#0d121a); border: 1px solid var(--pm-border); border-radius: 15px; padding: 18px; margin: 12px 0; box-shadow: 0 8px 28px rgba(0,0,0,.18); transition: .2s; }
.paper-result:hover { border-color: rgba(139,92,246,.42); box-shadow: 0 12px 32px rgba(0,0,0,.26); transform: translateY(-2px); }
.paper-title { font-size: 17px; font-weight: 700; color: #f2f4f8 !important; }
.paper-meta { color: #8995a5 !important; font-size: 12px; margin-top: 5px; }
[data-testid="stImage"] img { border-radius: 15px; border: 1px solid var(--pm-border); }
div[data-testid="stStatusWidget"] { border-radius: 12px !important; border: 1px solid var(--pm-border) !important; background: #0f141d !important; }
.pm-brand { padding: 8px 2px 18px; }
.pm-brand-title { font-size: 24px; font-weight: 800; letter-spacing: -.7px; color: #f5f3ff; }
.pm-brand-sub { color: #8e9aaa; font-size: 12px; margin-top: 2px; }
.pm-hero { padding: 28px 30px; border: 1px solid var(--pm-border); border-radius: 22px; background: linear-gradient(135deg,rgba(139,92,246,.12),rgba(15,20,29,.92) 48%,rgba(99,102,241,.07)); box-shadow: 0 18px 50px rgba(0,0,0,.25); margin-bottom: 22px; }
.pm-kicker { color: #a78bfa; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.4px; }
.pm-hero-title { font-size: 34px; font-weight: 800; color: #f8fafc; margin-top: 5px; }
.pm-hero-text { color: #9ba7b7; font-size: 14px; margin-top: 6px; }
.pm-status { display:inline-flex; align-items:center; gap:7px; padding:6px 10px; border-radius:999px; background:rgba(34,197,94,.08); border:1px solid rgba(34,197,94,.18); color:#86efac; font-size:11px; font-weight:700; }
.pm-dot { width:7px; height:7px; border-radius:50%; background:#4ade80; box-shadow:0 0 10px rgba(74,222,128,.8); }
.pm-card { padding:18px; border:1px solid var(--pm-border); border-radius:16px; background:#0f141d; min-height:110px; }
.pm-card-value { font-size:25px; font-weight:800; color:#f4f6f9; }
.pm-card-label { color:#7f8b9b; font-size:12px; margin-top:3px; }
.pm-section { color:#cbd5e1; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin:18px 0 8px; }

.pm-logo { display:flex; align-items:center; gap:10px; margin-bottom:4px; }
.pm-logo-mark { width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg,#a78bfa,#6366f1 55%,#22d3ee); display:flex; align-items:center; justify-content:center; color:white !important; font-weight:900; font-size:14px; box-shadow:0 8px 24px rgba(99,102,241,.28); }
.pm-logo-name { font-size:19px; font-weight:850; color:#f8fafc !important; letter-spacing:-.5px; }
.pm-logo-sub { color:#7f8b9b !important; font-size:10px; margin-top:1px; }
.pm-live { display:inline-flex; align-items:center; gap:7px; padding:5px 9px; border:1px solid rgba(34,211,238,.18); background:rgba(34,211,238,.06); border-radius:999px; color:#67e8f9 !important; font-size:10px; font-weight:700; }
.pm-live-dot { width:6px; height:6px; border-radius:50%; background:#22d3ee; box-shadow:0 0 10px rgba(34,211,238,.8); }
.pm-stream { margin:4px 0 12px; color:#7f8b9b !important; font-size:11px; }
.pm-cursor { display:inline-block; width:7px; height:16px; margin-left:2px; vertical-align:-3px; background:#a78bfa; border-radius:2px; animation:pmblink .85s infinite; }
@keyframes pmblink { 0%,45%{opacity:1} 46%,100%{opacity:.15} }
.pm-welcome { padding:26px 28px; border:1px solid var(--pm-border); border-radius:20px; background:linear-gradient(145deg,rgba(139,92,246,.08),rgba(15,20,29,.88)); margin-bottom:16px; }
.pm-welcome h2 { margin:0; font-size:25px; }
.pm-welcome p { color:#8e9aaa !important; max-width:760px; }
.pm-chip { display:inline-block; padding:6px 9px; margin:4px 5px 0 0; border:1px solid var(--pm-border); border-radius:999px; background:rgba(255,255,255,.025); color:#aeb8c6 !important; font-size:10px; }
.pm-source-note { color:#64748b !important; font-size:10px; margin-top:8px; }
@media (max-width: 768px) { .block-container { padding-left:1rem; padding-right:1rem; } h1 { font-size:1.8rem !important; } .pm-hero-title { font-size:27px; } }
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
    st.session_state.mode = "Research Intelligence"

if "research_assistant" not in st.session_state:
    st.session_state.research_assistant = ResearchAssistant()


assistant = st.session_state.assistant
research_assistant = st.session_state.research_assistant


# ===================================================
# TITLE
# ===================================================

st.markdown("""<div class="pm-hero"><div class="pm-kicker">Research Intelligence Platform</div><div class="pm-hero-title">Syntheia AI</div><div class="pm-hero-text">Discover papers, understand technical concepts and synthesize evidence from your scientific library.</div><div style="margin-top:14px"><span class="pm-live"><span class="pm-live-dot"></span> Knowledge base online</span></div></div>""", unsafe_allow_html=True)

st.caption("Semantic retrieval • grounded answers • research paper intelligence • multi-turn conversations")


# ===================================================
# SIDEBAR
# ===================================================

with st.sidebar:

    st.markdown("""<div class="pm-brand"><div class="pm-logo"><div class="pm-logo-mark">S</div><div><div class="pm-logo-name">Syntheia AI</div><div class="pm-logo-sub">Research Intelligence</div></div></div></div>""", unsafe_allow_html=True)

    mode = st.radio(
        "Choose Mode",
        [
            "Research Intelligence",
            "PDF Chatbot",
            "Image Assistant",
            "Medical Assistant"
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

        if mode == "Research Intelligence":
            research_assistant.memory.clear()
        else:
            assistant.reset()

        st.rerun()


# ===================================================
# RESEARCH ASSISTANT UI
# ===================================================

if mode == "Research Intelligence":

    st.markdown('<div class="pm-section">Research Workspace</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="pm-card"><div class="pm-card-value">5,000+</div><div class="pm-card-label">Scientific papers indexed</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="pm-card"><div class="pm-card-value">8,961</div><div class="pm-card-label">Retrieval chunks</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="pm-card"><div class="pm-card-value">RAG</div><div class="pm-card-label">Semantic research retrieval</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

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

        st.subheader("Search the research collection")

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

                        st.markdown('<div class="paper-result">', unsafe_allow_html=True)

                        st.markdown(
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

                        st.markdown("</div>", unsafe_allow_html=True)

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

    # ===================================================
    # TAB 2 — RESEARCH CHAT
    # ===================================================

    with tab2:

        if not st.session_state.messages:
            st.markdown(
                """
    <div class="pm-welcome">

    <h2>Research intelligence, without the noise.</h2>

    <p>
    Ask Syntheia AI about papers, methods, concepts,
    benchmarks and research findings. Answers are
    grounded in your indexed literature.
    </p>

    <span class="pm-chip">Semantic RAG</span>
    <span class="pm-chip">Paper Search</span>
    <span class="pm-chip">Evidence Grounding</span>
    <span class="pm-chip">Live AI Streaming</span>

    </div>
    """,
                unsafe_allow_html=True
            )

        research_question = st.chat_input(
            "Ask about a paper, concept, methodology or research topic..."
        )

        # ---------------------------------------------------
        # PREVIOUS MESSAGES
        # ---------------------------------------------------

        for message in st.session_state.messages:
            with st.chat_message(
                    message["role"]
            ):
                st.markdown(
                    message["content"]
                )

        # ---------------------------------------------------
        # NEW QUESTION
        # ---------------------------------------------------

        if research_question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": research_question
                }
            )

            with st.chat_message("user"):

                st.markdown(
                    research_question
                )

            # ------------------------------------------------
            # REAL STREAMING RESPONSE
            # ------------------------------------------------

            with st.chat_message("assistant"):

                status = st.empty()

                answer_box = st.empty()

                status.markdown(
                    '<div class="pm-stream">'
                    '⌁ Searching your research library…'
                    '</div>',
                    unsafe_allow_html=True
                )

                full_response = ""

                for chunk in research_assistant.stream_answer(
                        research_question
                ):
                    full_response += chunk

                    status.markdown(
                        '<div class="pm-stream">'
                        '⌁ Synthesizing evidence…'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    answer_box.markdown(
                        full_response +
                        '<span class="pm-cursor"></span>',
                        unsafe_allow_html=True
                    )

                status.markdown(
                    '<div class="pm-stream">'
                    '✓ Response generated live'
                    '</div>',
                    unsafe_allow_html=True
                )

                answer_box.markdown(
                    full_response
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response
                }
            )



    # TAB 3 — CONCEPT EXPLAINER
    # ===================================================

    with tab3:

        st.subheader("Concept Explorer")

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

        st.subheader("Concept Visualization")

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

if mode != "Research Intelligence":

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