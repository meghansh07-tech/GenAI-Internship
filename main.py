import chatbot.multimodal_chatbot
print(chatbot.multimodal_chatbot.__file__)
import subprocess
import sys


def run_streamlit():

    subprocess.run(
        [
            "streamlit",
            "run",
            "app.py"
        ]
    )


if __name__ == "__main__":

    run_streamlit()