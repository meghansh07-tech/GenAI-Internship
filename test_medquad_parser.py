from medical.xml_parser import load_medquad_documents


def main():

    documents = load_medquad_documents()

    print("=" * 60)

    print(f"Total Documents : {len(documents)}")

    print("=" * 60)

    if len(documents) > 0:

        print(documents[0].page_content)

        print()

        print(documents[0].metadata)


if __name__ == "__main__":
    main()