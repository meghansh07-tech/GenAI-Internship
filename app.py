import streamlit as st

from chatbot.chatbot import ask_question
from chatbot.multimodal_chatbot import MultiModalAssistant


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


assistant = st.session_state.assistant


# ===================================================
# TITLE
# ===================================================

st.title("🤖 MultiModal AI Assistant")

st.caption(
    "Task 1 • RAG Chatbot | Task 2 • Vision Language Model"
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
            "Image Assistant"
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

        assistant.reset()

        st.session_state.messages = []

        st.rerun()


# ===================================================
# DISPLAY OLD CHAT
# ===================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ===================================================
# CHAT INPUT
# ===================================================

prompt = st.chat_input("Ask anything...")


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

        with st.spinner("Searching knowledge base..."):

            response = ask_question(prompt)

    # -----------------------------
    # IMAGE ASSISTANT
    # -----------------------------

    else:

        with st.spinner("Analyzing image..."):

            response = assistant.ask(
                prompt,
                uploaded_image
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

    with st.chat_message("assistant"):

        st.markdown(response)
# ===================================================
# IMAGE PREVIEW
# ===================================================

if mode == "Image Assistant" and uploaded_image is not None:

    st.divider()

    st.subheader("🖼 Uploaded Image")

    st.image(
        uploaded_image,
        use_container_width=True
    )


# ===================================================
# ASSISTANT STATUS
# ===================================================

st.sidebar.divider()

st.sidebar.subheader("📊 Assistant Status")

status = assistant.get_status()

st.sidebar.write(
    f"Image Loaded : {'✅' if status['image_loaded'] else '❌'}"
)

st.sidebar.write(
    f"Conversation Length : {status['conversation_length']}"
)


# ===================================================
# ABOUT
# ===================================================

st.sidebar.divider()

st.sidebar.info(
    """
### 🚀 Features

✅ PDF Question Answering (RAG)

✅ Image Understanding

✅ Multi-turn Conversation

✅ Context Retention

✅ Local Ollama Models

Built using:

- LangChain 1.x
- Ollama
- Streamlit
- ChromaDB
"""
)


# ===================================================
# FOOTER
# ===================================================

st.divider()

st.caption(
    "Built with ❤️ using LangChain • Ollama • Streamlit"
)