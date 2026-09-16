from langdetect import detect, DetectorFactory

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


DetectorFactory.seed = 0


class MultilingualHandler:
    """
    Handles multilingual conversations.

    Supported languages:
        English
        Hindi
        Spanish
        French
    """

    LANGUAGE_CODES = {
        "en": "eng_Latn",
        "hi": "hin_Deva",
        "es": "spa_Latn",
        "fr": "fra_Latn",
    }

    LANGUAGE_NAMES = {
        "en": "English",
        "hi": "Hindi",
        "es": "Spanish",
        "fr": "French",
    }

    MODEL_NAME = "facebook/nllb-200-distilled-600M"

    def __init__(self):

        print("Loading multilingual model...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.MODEL_NAME
        )

        print("Multilingual model loaded.")

    # -------------------------
    # LANGUAGE DETECTION
    # -------------------------

    def detect_language(self, text: str):

        if not text or not text.strip():
            return "en"

        try:
            language = detect(text)

            if language in self.LANGUAGE_CODES:
                return language

            return "en"

        except Exception:
            return "en"

    # -------------------------
    # LANGUAGE NAME
    # -------------------------

    def get_language_name(self, language_code: str):

        return self.LANGUAGE_NAMES.get(
            language_code,
            "English"
        )

    # -------------------------
    # TRANSLATION
    # -------------------------

    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str
    ):

        if not text or not text.strip():
            return text

        if source_language == target_language:
            return text

        source_code = self.LANGUAGE_CODES.get(
            source_language
        )

        target_code = self.LANGUAGE_CODES.get(
            target_language
        )

        if source_code is None or target_code is None:
            return text

        self.tokenizer.src_lang = source_code

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        forced_bos_token_id = (
            self.tokenizer.convert_tokens_to_ids(
                target_code
            )
        )

        translated_tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=512
        )

        result = self.tokenizer.batch_decode(
            translated_tokens,
            skip_special_tokens=True
        )

        return result[0]

    # -------------------------
    # TRANSLATE TO ENGLISH
    # -------------------------

    def translate_to_english(
        self,
        text: str,
        source_language: str
    ):

        return self.translate(
            text,
            source_language,
            "en"
        )

    # -------------------------
    # TRANSLATE FROM ENGLISH
    # -------------------------

    def translate_from_english(
        self,
        text: str,
        target_language: str
    ):

        return self.translate(
            text,
            "en",
            target_language
        )

    # -------------------------
    # INPUT PROCESSING
    # -------------------------

    def process_input(self, text: str):

        language = self.detect_language(text)

        english_text = self.translate_to_english(
            text,
            language
        )

        return {
            "original_text": text,
            "language_code": language,
            "language_name": self.get_language_name(language),
            "english_text": english_text
        }

    # -------------------------
    # RESPONSE PROCESSING
    # -------------------------

    def process_response(
        self,
        response: str,
        target_language: str
    ):

        return self.translate_from_english(
            response,
            target_language
        )

    # -------------------------
    # CONVERSATION TURN
    # -------------------------

    def process_conversation_turn(
        self,
        user_message: str,
        conversation_memory
    ):

        # Detect the current language
        language = self.detect_language(
            user_message
        )

        # Translate current message into English
        english_message = self.translate_to_english(
            user_message,
            language
        )

        # Get previous conversation


        # Translate previous non-English messages
        # individually so the LLM receives a consistent
        # English conversation context.

        english_history = ""

        for message in conversation_memory.get_history():

            role = message["role"]
            content = message["content"]

            message_language = self.detect_language(
                content
            )

            if message_language != "en":

                content = self.translate_to_english(
                    content,
                    message_language
                )

            english_history += (
                f"{role.capitalize()}: "
                f"{content}\n"
            )

        return {
            "language_code": language,
            "language_name": self.get_language_name(language),
            "original_message": user_message,
            "english_message": english_message,
            "conversation_history": english_history
        }