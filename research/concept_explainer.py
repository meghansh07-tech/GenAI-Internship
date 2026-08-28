from models.llm_model import get_llm


class ConceptExplainer:

    def __init__(self):

        self.llm = get_llm()

    def explain(self, concept):

        prompt = f"""
You are an expert Computer Science professor.

Explain:

{concept}

Provide:

1. Definition
2. Working
3. Advantages
4. Limitations
5. Real-world Applications
6. Simple Explanation
"""

        response = self.llm.invoke(prompt)

        return response.content