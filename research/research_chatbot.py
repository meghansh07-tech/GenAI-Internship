from research.paper_search import PaperSearch
from research.paper_summarizer import PaperSummarizer
from research.concept_explainer import ConceptExplainer

from research.conversation_memory import ResearchMemory


class ResearchAssistant:

    def __init__(self):

        self.search_engine = PaperSearch()

        self.summarizer = PaperSummarizer()

        self.explainer = ConceptExplainer()

        self.memory = ResearchMemory()


    def search_papers(self, query, k=5):

        return self.search_engine.search(
            query,
            k=k
        )


    def summarize_paper(self, document):

        return self.summarizer.summarize(
            document
        )


    def explain_concept(self, concept):

        return self.explainer.explain(
            concept
        )


    # ===================================================
    # NORMAL RESEARCH ANSWER
    # ===================================================

    def ask(self, question):

        docs = self.search_engine.search(
            question
        )

        if len(docs) == 0:

            return "No related research paper found."


        context = "\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )


        prompt = f"""
You are Syntheia AI, a concise research intelligence assistant.

Answer the user's question using the research context below.

Question:
{question}

Research Context:
{context}

Response style:
- Be concise and direct.
- Give the answer first.
- Focus only on information relevant to the question.
- Use short paragraphs or bullets when useful.
- Avoid unnecessary background information.
- Do not repeat the question.
- Do not invent information outside the provided context.
- Aim for a brief but technically useful answer.
"""


        answer = self.explainer.explain(
            prompt
        )


        self.memory.add_user(
            question
        )

        self.memory.add_assistant(
            answer
        )


        return answer


    # ===================================================
    # REAL STREAMING RESEARCH ANSWER
    # ===================================================

    def stream_answer(self, question):

        docs = self.search_engine.search(
            question
        )

        if len(docs) == 0:

            yield "No related research paper found."

            return


        context = "\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )


        prompt = f"""
You are Syntheia AI, a concise research intelligence assistant.

Answer the user's question using the research context below.

Question:
{question}

Research Context:
{context}

Response style:
- Be concise and direct.
- Give the answer first.
- Focus only on information relevant to the question.
- Use short paragraphs or bullets when useful.
- Avoid unnecessary background information.
- Do not repeat the question.
- Do not invent information outside the provided context.
- Aim for a brief but technically useful answer.
"""


        full_answer = ""


        for chunk in self.explainer.stream_explain(
            prompt
        ):

            full_answer += chunk

            yield chunk


        self.memory.add_user(
            question
        )

        self.memory.add_assistant(
            full_answer
        )


    def history(self):

        return self.memory.get_history()