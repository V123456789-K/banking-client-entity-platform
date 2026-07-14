import pandas as pd

from src.config import RAW_DATA_DIR


def generate_crm_data() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    records = [
        {
            "source_record_id": "CRM001",
            "legal_name": "ABC Technologies Pvt Ltd",
            "country": "India",
            "industry": "Technology",
            "registration_number": "U12345KA2020PTC001",
            "lei": None,
            "risk_rating": "LOW",
        },
        {
            "source_record_id": "CRM002",
            "legal_name": "ABC Technologies Private Limited",
            "country": "India",
            "industry": "Technology",
            "registration_number": "U12345KA2020PTC001",
            "lei": None,
            "risk_rating": "LOW",
        },
        {
            "source_record_id": "CRM003",
            "legal_name": "XYZ Manufacturing Ltd",
            "country": "India",
            "industry": "Manufacturing",
            "registration_number": "U99887MH2018PLC888",
            "lei": "123456789XYZ",
            "risk_rating": "MEDIUM",
        },
        {
            "source_record_id": "CRM004",
            "legal_name": "Global Finance Holdings",
            "country": "Singapore",
            "industry": "Financial Services",
            "registration_number": "SG20211234",
            "lei": None,
            "risk_rating": "HIGH",
        },
    ]

    dataframe = pd.DataFrame(records)

    output_path = RAW_DATA_DIR / "crm_entities.csv"
    dataframe.to_csv(output_path, index=False)

    print(f"CRM records generated: {len(dataframe)}")
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    generate_crm_data()