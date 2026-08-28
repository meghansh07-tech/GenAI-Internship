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

        return self.summarizer.summarize(document)

    def explain_concept(self, concept):

        return self.explainer.explain(concept)

    def ask(self, question):

        docs = self.search_engine.search(question)

        if len(docs) == 0:

            return "No related research paper found."

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        answer = self.explainer.explain(
            f"""
Question:
{question}

Research Context:

{context}
"""
        )

        self.memory.add_user(question)

        self.memory.add_assistant(answer)

        return answer

    def history(self):

        return self.memory.get_history()