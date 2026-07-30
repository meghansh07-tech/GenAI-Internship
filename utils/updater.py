import os
import json
from utils.text_splitter import split_documents
from datetime import datetime

from logger import log_info, log_error

from document_loader import load_documents
from vector_db.chroma_manager import get_vector_database


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DOCS_PATH = BASE_DIR / "docs"
PROCESSED_FILE = BASE_DIR / "data" / "processed_files.json"


def load_processed_files():

    if not os.path.exists(PROCESSED_FILE):
        return []

    with open(PROCESSED_FILE, "r") as file:
        return json.load(file)



def save_processed_files(files):

    with open(PROCESSED_FILE, "w") as file:
        json.dump(files, file, indent=4)



def get_new_documents():

    processed_files = load_processed_files()

    all_files = [
        file for file in os.listdir(str(DOCS_PATH))
        if file.endswith(".pdf")
    ]

    new_files = [
        file for file in all_files
        if file not in processed_files
    ]

    return new_files



def update_knowledge_base():

    new_files = get_new_documents()


    if not new_files:

        log_info(
            "No new documents found. Knowledge base is already updated."
        )

        return


    log_info("New documents detected:")

    for file in new_files:

        log_info(f"New document: {file}")


    try:

        # Load documents from docs folder
        documents = load_documents(
            DOCS_PATH,
            files=new_files
        )

        documents = split_documents(documents)


        # Get Chroma vector database
        vector_db = get_vector_database()


        # Add documents into Chroma
        vector_db.add_documents(
            documents
        )


        # Save processed files
        processed_files = load_processed_files()

        processed_files.extend(new_files)

        save_processed_files(processed_files)


        log_info(
            f"Knowledge base updated successfully at {datetime.now()}"
        )


    except Exception as e:

        log_error(
            f"Knowledge base update failed: {str(e)}"
        )



if __name__ == "__main__":

    update_knowledge_base()