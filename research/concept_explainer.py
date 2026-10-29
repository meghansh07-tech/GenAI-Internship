from models.llm_model import get_llm


class ConceptExplainer:

    def __init__(self):

        self.llm = get_llm()


    # ===================================================
    # NORMAL EXPLANATION
    # ===================================================

    def explain(self, concept):

        prompt = f"""
You are Syntheia AI, a concise Computer Science research assistant.

Explain the following concept clearly and accurately:

{concept}

Response requirements:

- Start with a short definition.
- Explain the core idea and working.
- Mention important advantages or limitations only when relevant.
- Give a practical/example use case when useful.
- Keep the response concise and interview-friendly.
- Avoid unnecessary long sections.
- Do not repeat the question.
"""

        response = self.llm.invoke(prompt)

        return response.content


    # ===================================================
    # STREAMING EXPLANATION
    # ===================================================

    def stream_explain(self, concept):

        prompt = f"""
You are Syntheia AI, a concise Computer Science research assistant.

Explain the following concept clearly and accurately:

{concept}

Response requirements:

- Start with a short definition.
- Explain the core idea and working.
- Mention important advantages or limitations only when relevant.
- Give a practical/example use case when useful.
- Keep the response concise and interview-friendly.
- Avoid unnecessary long sections.
- Do not repeat the question.
"""

        for chunk in self.llm.stream(prompt):

            if chunk.content:

                yield chunk.content