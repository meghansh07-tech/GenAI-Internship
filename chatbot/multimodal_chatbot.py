from models.llm_model import get_llm
from models.vision_model import get_vision_model

from memory.conversation_memory import ConversationMemory

from utils.image_processor import save_uploaded_image


class MultiModalAssistant:
    """
    Multi-modal AI Assistant

    Capabilities
    ------------
    • Image Understanding
    • Text Understanding
    • Multi-turn Conversation
    • Context Retention
    """

    def __init__(self):

        # Text LLM
        self.llm = get_llm()

        # Vision LLM
        self.vision_model = get_vision_model()

        # Conversation Memory
        self.memory = ConversationMemory()

        # Last uploaded image
        self.current_image = None


    def set_image(self, uploaded_file):
        """
        Save uploaded image
        """

        self.current_image = save_uploaded_image(uploaded_file)

        return self.current_image


    def clear_image(self):
        """
        Remove current image.
        """

        self.current_image = None


    def clear_conversation(self):
        """
        Clear conversation history.
        """

        self.memory.clear_memory()


    def get_conversation(self):
        """
        Return formatted conversation.
        """

        return self.memory.get_formatted_history()


