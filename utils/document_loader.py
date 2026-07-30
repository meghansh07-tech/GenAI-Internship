"""
document_loader.py

Loads PDF documents from the docs directory.
Supports:
1. Loading all PDFs (first-time indexing)
2. Loading only selected PDFs (dynamic updates)
"""

from pathlib import Path
from typing import List, Optional

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

from utils.logger import log_info, log_error


def load_documents(
    docs_path: Path,
    files: Optional[List[str]] = None
) -> List[Document]:
    """
    Load PDF documents.

    Parameters
    ----------
    docs_path : Path
        Path to the docs folder.

    files : list[str], optional
        List of PDF filenames to load.
        If None, loads every PDF inside docs_path.

    Returns
    -------
    List[Document]
        LangChain Document objects.
    """

    if not docs_path.exists():
        raise FileNotFoundError(f"Directory not found: {docs_path}")

    documents = []

    try:

        # -------- Load ALL PDFs --------
        if files is None:

            pdf_files = list(docs_path.glob("*.pdf"))

        # -------- Load ONLY specified PDFs --------
        else:

            pdf_files = [
                docs_path / file
                for file in files
            ]

        if not pdf_files:

            log_info("No PDF documents found.")

            return []

        for pdf in pdf_files:

            loader = PyPDFLoader(str(pdf))

            docs = loader.load()

            documents.extend(docs)

            log_info(f"Loaded: {pdf.name}")

        log_info(
            f"Successfully loaded {len(documents)} pages."
        )

        return documents

    except Exception as e:

        log_error(
            f"Document loading failed: {str(e)}"
        )

        raise