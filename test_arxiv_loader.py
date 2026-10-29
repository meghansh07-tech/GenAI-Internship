from research.arxiv_loader import load_arxiv_documents

docs = load_arxiv_documents(limit=3)

print("Loaded:", len(docs))

for doc in docs:
    print("=" * 50)
    print(doc.metadata)
    print(doc.page_content[:300])