import sqlite3

from src.config import DATABASE_PATH


conn = sqlite3.connect(DATABASE_PATH)

rows = conn.execute(
    """
    SELECT
        entity_id_1,
        entity_id_2,
        overall_match_score,
        match_classification
    FROM entity_matches
    ORDER BY overall_match_score DESC
    """
).fetchall()

for row in rows:
    print(row)

conn.close()