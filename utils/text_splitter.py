"""
text_splitter.py

Splits LangChain Documents into smaller chunks
before creating embeddings.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.logger import log_info, log_error


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """
    Split documents into smaller chunks.

    Parameters
    ----------
    documents : List[Document]
        Documents loaded from PDFs.

    chunk_size : int
        Maximum characters in one chunk.

    chunk_overlap : int
        Overlap between two chunks.

    Returns
    -------
    List[Document]
        Chunked LangChain Documents.
    """

    try:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        chunks = splitter.split_documents(documents)

        log_info(f"Created {len(chunks)} chunks.")

        return chunks

    except Exception as e:

        log_error(f"Text splitting failed : {str(e)}")

        raise