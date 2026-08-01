from collections import deque


class ConversationMemory:
    """
    Stores the recent conversation history.

    This memory is shared by the multimodal chatbot
    so it can remember previous images, questions,
    and responses.
    """

    def __init__(self, max_history=10):

        self.history = deque(maxlen=max_history)


    def add_user_message(self, message):

        self.history.append(
            {
                "role": "user",
                "content": message
            }
        )


    def add_assistant_message(self, message):

        self.history.append(
            {
                "role": "assistant",
                "content": message
            }
        )


    def get_history(self):

        return list(self.history)


    def clear_memory(self):

        self.history.clear()


    def get_formatted_history(self):
        """
        Returns conversation history
        in readable format for the LLM.
        """

        formatted_history = ""

        for message in self.history:

            formatted_history += (
                f"{message['role'].capitalize()}: "
                f"{message['content']}\n"
            )

        return formatted_history