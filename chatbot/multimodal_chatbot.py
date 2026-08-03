
from models.llm_model import get_llm

import ollama
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




    def analyze_image(self, user_prompt):
            """
            Analyze uploaded image using the official Ollama SDK.
            """
            print("===== USING OLLAMA SDK ANALYZE_IMAGE =====")

            if self.current_image is None:
                return "Please upload an image first."

            try:

                response = ollama.chat(
                    model="qwen2.5vl:3b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
        Analyze this image carefully.

        User Question:
        {user_prompt}

        Instructions:
        - Answer only using evidence visible in the image.
        - If uncertain, clearly say you are uncertain.
        - Never invent details.
        """,
                            "images": [str(self.current_image)]
                        }
                    ]
                )
                print(response)
                print(type(response))

                answer = response.message.content

                self.memory.add_user_message(user_prompt)
                self.memory.add_assistant_message(answer)

                return self.validate_response(answer)

            except Exception as e:
                import traceback

                traceback.print_exc()

                return str(e)



    def ask(self, user_prompt, uploaded_file=None):

        """
        Main entry point for the assistant.

        Parameters
        ----------
        user_prompt : str
            User's question.

        uploaded_file : UploadedFile, optional
            Streamlit uploaded image.

        Returns
        -------
        str
            Assistant response.
        """
        print(">>> INSIDE analyze_image() <<<")

        # Save newly uploaded image
        print("Before set_image")
        if uploaded_file is not None:
            self.set_image(uploaded_file)
            print("After set_image")
            print("Current image:", self.current_image)


        # If an image exists, use the Vision Model
        if self.current_image is not None:
            print("Calling analyze_image()")
            return self.analyze_image(user_prompt)

        # Otherwise use the normal LLM
        return self.chat(user_prompt)


    def validate_response(self, response):
        """
        Perform simple response validation.
        """

        if response is None:
            return "Unable to generate a response."

        if isinstance(response, str):

            response = response.strip()

            if len(response) == 0:
                return "The model returned an empty response."

        return response


    def get_status(self):
        """
        Return assistant status.
        """

        return {
            "image_loaded": self.current_image is not None,
            "conversation_length": len(
                self.memory.get_history()
            )
        }


    def reset(self):
        """
        Reset the assistant.
        """

        self.clear_image()
        self.clear_conversation()


