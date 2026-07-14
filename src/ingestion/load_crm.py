import sqlite3

import pandas as pd

from src.config import DATABASE_PATH, RAW_DATA_DIR


CRM_FILE = RAW_DATA_DIR / "crm_entities.csv"


def get_or_create_source_system(conn: sqlite3.Connection) -> int:
    conn.execute(
        """
        INSERT OR IGNORE INTO source_systems (
            source_system_name,
            source_type
        )
        VALUES (?, ?)
        """,
        (
            "CRM",
            "Internal Client Relationship Management",
        ),
    )

    result = conn.execute(
        """
        SELECT source_system_id
        FROM source_systems
        WHERE source_system_name = ?
        """,
        ("CRM",),
    ).fetchone()

    if result is None:
        raise RuntimeError("CRM source system could not be created.")

    return int(result[0])


def load_crm_entities() -> None:
    if not CRM_FILE.exists():
        raise FileNotFoundError(
            f"CRM source file does not exist: {CRM_FILE}"
        )

    dataframe = pd.read_csv(CRM_FILE)

    required_columns = {
        "source_record_id",
        "legal_name",
        "country",
        "industry",
        "registration_number",
        "lei",
        "risk_rating",
    }

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing CRM columns: {sorted(missing_columns)}"
        )

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        conn.execute("PRAGMA foreign_keys = ON")

        source_system_id = get_or_create_source_system(conn)

        inserted_count = 0
        skipped_count = 0

        for _, row in dataframe.iterrows():
            source_record_id = str(row["source_record_id"]).strip()

            existing_record = conn.execute(
                """
                SELECT raw_entity_id
                FROM raw_entities
                WHERE source_system_id = ?
                  AND source_record_id = ?
                """,
                (
                    source_system_id,
                    source_record_id,
                ),
            ).fetchone()

            if existing_record is not None:
                skipped_count += 1
                continue

            lei = (
                None
                if pd.isna(row["lei"])
                else str(row["lei"]).strip()
            )

            conn.execute(
                """
                INSERT INTO raw_entities (
                    source_system_id,
                    source_record_id,
                    legal_name,
                    lei,
                    registration_number,
                    industry,
                    country,
                    risk_rating
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source_system_id,
                    source_record_id,
                    str(row["legal_name"]).strip(),
                    lei,
                    str(row["registration_number"]).strip(),
                    str(row["industry"]).strip(),
                    str(row["country"]).strip(),
                    str(row["risk_rating"]).strip().upper(),
                ),
            )

            inserted_count += 1

        conn.commit()

        print(f"CRM records inserted: {inserted_count}")
        print(f"CRM records skipped: {skipped_count}")

    finally:
        conn.close()


if __name__ == "__main__":
    load_crm_entities()