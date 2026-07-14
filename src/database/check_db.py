import sqlite3

from src.config import DATABASE_PATH


def check_database() -> None:
    conn = sqlite3.connect(DATABASE_PATH)

    try:
        print("\nSource systems:")

        source_systems = conn.execute(
            """
            SELECT
                source_system_id,
                source_system_name,
                source_type
            FROM source_systems
            """
        ).fetchall()

        for row in source_systems:
            print(row)

        print("\nRaw entities:")

        entities = conn.execute(
            """
            SELECT
                raw_entity_id,
                source_record_id,
                legal_name,
                country,
                registration_number,
                lei,
                risk_rating
            FROM raw_entities
            ORDER BY raw_entity_id
            """
        ).fetchall()

        for row in entities:
            print(row)

        print(f"\nTotal raw entities: {len(entities)}")

    finally:
        conn.close()


if __name__ == "__main__":
    check_database()