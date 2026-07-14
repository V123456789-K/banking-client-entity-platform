import pandas as pd

records = [
    {
        "source_record_id": "CRM001",
        "legal_name": "ABC Technologies Pvt Ltd",
        "country": "India",
        "industry": "Technology",
        "registration_number": "U12345KA2020PTC001",
        "lei": None,
        "risk_rating": "LOW"
    },
    {
        "source_record_id": "CRM002",
        "legal_name": "ABC Technologies Private Limited",
        "country": "India",
        "industry": "Technology",
        "registration_number": "U12345KA2020PTC001",
        "lei": None,
        "risk_rating": "LOW"
    },
    {
        "source_record_id": "CRM003",
        "legal_name": "XYZ Manufacturing Ltd",
        "country": "India",
        "industry": "Manufacturing",
        "registration_number": "U99887MH2018PLC888",
        "lei": "123456789XYZ",
        "risk_rating": "MEDIUM"
    },
    {
        "source_record_id": "CRM004",
        "legal_name": "Global Finance Holdings",
        "country": "Singapore",
        "industry": "Financial Services",
        "registration_number": "SG20211234",
        "lei": None,
        "risk_rating": "HIGH"
    }
]

df = pd.DataFrame(records)

df.to_csv(
    "data/raw/crm_entities.csv",
    index=False
)

print(df.head())
print()
print("Saved: data/raw/crm_entities.csv")