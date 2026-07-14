import re
import sqlite3

from src.config import DATABASE_PATH


REPLACEMENTS = {
    "PRIVATE LIMITED": "PVT LTD",
    "PRIVATE LTD": "PVT LTD",
    "LIMITED": "LTD",
    "CORPORATION": "CORP",
    "INCORPORATED": "INC",
}


def normalize_company_name(name: str) -> str:

    if not name:
        return ""

    name = name.upper().strip()

    name = re.sub(r"[^\w\s]", " ", name)

    name = re.sub(r"\s+", " ", name)

    for old, new in REPLACEMENTS.items():
        name = name.replace(old, new)

    return name.strip()


def standardize_entities():

    conn = sqlite3.connect(DATABASE_PATH)

    entities = conn.execute(
        """
        SELECT
            raw_entity_id,
            legal_name,
            registration_number,
            country
        FROM raw_entities
        """
    ).fetchall()

    inserted = 0

    for row in entities:

        raw_entity_id = row[0]
        legal_name = row[1]
        registration_number = row[2]
        country = row[3]

        standardized_name = normalize_company_name(
            legal_name
        )

        conn.execute(
            """
            INSERT OR REPLACE INTO
            standardized_entities
            (
                raw_entity_id,
                standardized_legal_name,
                standardized_country,
                normalized_registration_number,
                standardization_status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                raw_entity_id,
                standardized_name,
                country,
                registration_number,
                "STANDARDIZED"
            )
        )

        inserted += 1

    conn.commit()

    print(
        f"Standardized entities: {inserted}"
    )

    conn.close()


if __name__ == "__main__":
    standardize_entities()