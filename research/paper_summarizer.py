from models.llm_model import get_llm


class PaperSummarizer:

    def __init__(self):

        self.llm = get_llm()

    def summarize(self, document):

        prompt = f"""
You are an AI Research Assistant.

Analyze this research paper and provide:

1. Title
2. Main Problem
3. Proposed Method
4. Key Findings
5. Applications
6. Limitations
7. Simple Explanation

Paper:

{document.page_content}
"""

        response = self.llm.invoke(prompt)

        return response.content