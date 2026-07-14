import sqlite3

from src.config import DATABASE_PATH, SCHEMA_PATH


def initialize_database():
    conn = sqlite3.connect(DATABASE_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn.executescript(schema)

    conn.commit()
    conn.close()

    print(f"Database created: {DATABASE_PATH}")


if __name__ == "__main__":
    initialize_database()