from transformers import pipeline


class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )

    def analyze(self, text):
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "confidence": 0.0
            }

        result = self.classifier(text[:512])[0]

        label = result["label"].lower()
        confidence = round(result["score"], 4)

        if "positive" in label:
            sentiment = "positive"
        elif "negative" in label:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "confidence": confidence
        }

    def get_response_prefix(self, sentiment):
        if sentiment == "positive":
            return "I'm glad I could help! 😊 "

        elif sentiment == "negative":
            return (
                "I understand that this may be frustrating. "
                "Let me try to provide a clearer and more helpful answer. "
            )

        return ""
