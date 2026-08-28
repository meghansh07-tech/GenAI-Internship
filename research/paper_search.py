from pathlib import Path

from langchain_chroma import Chroma

from embeddings.embedding_model import get_embedding_model


DB_DIRECTORY = Path("vector_db/arxiv_db")


class PaperSearch:

    def __init__(self):

        self.embedding_model = get_embedding_model()

        self.db = Chroma(

            persist_directory=str(DB_DIRECTORY),

            embedding_function=self.embedding_model
        )

    def search(self, query, k=5):

        docs = self.db.similarity_search(query, k=k)

        return docs

    def search_with_scores(self, query, k=5):

        docs = self.db.similarity_search_with_score(query, k=k)

        return docs