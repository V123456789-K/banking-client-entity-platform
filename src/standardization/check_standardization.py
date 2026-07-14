import sqlite3

from src.config import DATABASE_PATH


conn = sqlite3.connect(DATABASE_PATH)

rows = conn.execute(
    """
    SELECT
        raw_entity_id,
        standardized_legal_name
    FROM standardized_entities
    """
).fetchall()

for row in rows:
    print(row)

conn.close()