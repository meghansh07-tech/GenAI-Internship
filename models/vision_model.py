from langchain_ollama import ChatOllama


def get_vision_model():
    """
    Returns the Vision Language Model.
    Used for image understanding and reasoning.
    """

    vision_model = ChatOllama(
        model="qwen2.5vl:3b",
        temperature=0.2
    )

    return vision_model