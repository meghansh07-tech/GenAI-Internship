import re


# ----------------------------------------
# Medical Entity Lists
# ----------------------------------------

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
    "anemia"
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


# ----------------------------------------
# Entity Extraction
# ----------------------------------------

def extract_medical_entities(text: str):

    text = text.lower()

    tokens = re.findall(r"[a-zA-Z0-9\- ]+", text)

    symptoms = []
    diseases = []
    treatments = []

    for token in tokens:

        token = token.strip()

        if token in SYMPTOMS:
            symptoms.append(token)

        if token in DISEASES:
            diseases.append(token)

        if token in TREATMENTS:
            treatments.append(token)

    return {

        "symptoms": sorted(set(symptoms)),

        "diseases": sorted(set(diseases)),

        "treatments": sorted(set(treatments))
    }