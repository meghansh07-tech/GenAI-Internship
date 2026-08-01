import streamlit as st

from chatbot.chatbot import ask_question

st.title("Dynamic Knowledge Base Chatbot")

question = st.text_input("Ask Question")

if st.button("Submit"):

    answer = ask_question(question)

    st.write(answer)