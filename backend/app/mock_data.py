# backend/mock_data.py
# Fictional mock records for local testing only

MOCK_WAEC_RESULTS = {
    "2022009876": {
        "PIN": "2022009876",
        "ExamYear": 2019,
        "CandidateNo": "WAEC20220001",
        "Name": "Bashir Mustapha",
        "CentreName": "Government Secondary School Kaduna",
        "subject_grades": [
            {"subject": "MATHEMATICS", "grade": "B3"},
            {"subject": "ENGLISH LANGUAGE", "grade": "C4"},
            {"subject": "BIOLOGY", "grade": "B2"},
            {"subject": "CHEMISTRY", "grade": "C5"},
            {"subject": "PHYSICS", "grade": "C6"},
            {"subject": "GEOGRAPHY", "grade": "B2"},
            {"subject": "ECONOMICS", "grade": "C4"},
            {"subject": "GOVERNMENT", "grade": "B3"},
            {"subject": "AGRICULTURAL SCIENCE", "grade": "C5"}
        ],
    }
}

MOCK_NECO_RESULTS = {
    "3022009876": {
        "PIN": "3022009876",
        "ExamYear": 2019,
        "CandidateNo": "NECO20220002",
        "Name": "Bashir Mustapha",
        "CentreName": "Kaduna Central NECO Centre",
        "subject_grades": [
            {"subject": "MATHEMATICS", "grade": "B3"},
            {"subject": "ENGLISH LANGUAGE", "grade": "C4"},
            {"subject": "BIOLOGY", "grade": "B2"},
            {"subject": "CHEMISTRY", "grade": "C5"},
            {"subject": "PHYSICS", "grade": "C6"},
            {"subject": "GEOGRAPHY", "grade": "B2"},
            {"subject": "ECONOMICS", "grade": "C4"},
            {"subject": "COMPUTER STUDIES", "grade": "B3"},
            {"subject": "CIVIC EDUCATION", "grade": "B2"}
        ],
    }
}

MOCK_NYSC_RESULTS = {
    "NYSC2024KAD001": {
        "callup_no": "NYSC2024KAD001",
        "certificate_no": "NYSC-CERT-2024-001",
        "dob": "2002-02-26",
        "Name": "Bashir Mustapha",
        "Batch": "Batch A",
        "Year": "2024",
        "StateCode": "NYSC/KAD/2024/0001",
    }
}
