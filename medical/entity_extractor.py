import re


# --------------------------------------------------
# Medical Entity Lists
# --------------------------------------------------

SYMPTOMS = {
    "fever",
    "cough",
    "headache",
    "pain",
    "fatigue",
    "vomiting",
    "nausea",
    "diarrhea",
    "dizziness",
    "chills",
    "rash",
    "sore throat",
    "shortness of breath",
    "chest pain"
}


DISEASES = {
    "diabetes",
    "cancer",
    "covid",
    "covid-19",
    "malaria",
    "tuberculosis",
    "hypertension",
    "asthma",
    "arthritis",
    "anemia",

    # Multi-word diseases
    "familial mediterranean fever",
    "familial cold autoinflammatory syndrome",
    "rheumatic fever",
    "periodic fever aphthous stomatitis pharyngitis and adenitis",
    "tumor necrosis factor receptor-associated periodic syndrome",
    "q fever",
    "necrotizing fasciitis"
}


TREATMENTS = {
    "insulin",
    "paracetamol",
    "ibuprofen",
    "chemotherapy",
    "radiotherapy",
    "antibiotics",
    "surgery",
    "vaccination"
}


# --------------------------------------------------
# Entity Extraction
# --------------------------------------------------

def extract_medical_entities(text: str):

    text = text.lower()

    symptoms = []
    diseases = []
    treatments = []

    # --------------------------------------------------
    # Detect diseases FIRST
    # --------------------------------------------------

    for disease in DISEASES:

        if re.search(
            r"\b" + re.escape(disease) + r"\b",
            text
        ):
            diseases.append(disease)

    # --------------------------------------------------
    # Detect symptoms
    # --------------------------------------------------

    for symptom in SYMPTOMS:

        if re.search(
            r"\b" + re.escape(symptom) + r"\b",
            text
        ):
            symptoms.append(symptom)

    # --------------------------------------------------
    # Detect treatments
    # --------------------------------------------------

    for treatment in TREATMENTS:

        if re.search(
            r"\b" + re.escape(treatment) + r"\b",
            text
        ):
            treatments.append(treatment)

    return {
        "symptoms": sorted(set(symptoms)),
        "diseases": sorted(set(diseases)),
        "treatments": sorted(set(treatments))
    }
