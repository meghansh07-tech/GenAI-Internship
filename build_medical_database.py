from vector_db.medical_db_builder import build_medical_database


def main():

    print("=" * 60)
    print("Building Medical Vector Database")
    print("=" * 60)

    build_medical_database()

    print("\nMedical Database Ready!")


if __name__ == "__main__":
    main()