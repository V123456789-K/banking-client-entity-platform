import sqlite3

from rapidfuzz import fuzz

from src.config import DATABASE_PATH


MATCH_THRESHOLD = 85


def match_entities():

    conn = sqlite3.connect(DATABASE_PATH)

    entities = conn.execute(
        """
        SELECT
            standardized_entity_id,
            standardized_legal_name,
            normalized_registration_number
        FROM standardized_entities
        """
    ).fetchall()

    total_matches = 0

    for i in range(len(entities)):

        entity_a = entities[i]

        for j in range(i + 1, len(entities)):

            entity_b = entities[j]

            score = fuzz.token_sort_ratio(
                entity_a[1],
                entity_b[1]
            )

            registration_match = int(
                entity_a[2] == entity_b[2]
            )

            overall_score = score

            if registration_match:
                overall_score += 20

            if overall_score > 100:
                overall_score = 100

            classification = (
                "DUPLICATE"
                if overall_score >= MATCH_THRESHOLD
                else "UNIQUE"
            )

            conn.execute(
                """
                INSERT INTO entity_matches
                (
                    entity_id_1,
                    entity_id_2,
                    name_similarity_score,
                    registration_match,
                    overall_match_score,
                    match_classification
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    entity_a[0],
                    entity_b[0],
                    score,
                    registration_match,
                    overall_score,
                    classification
                )
            )

            total_matches += 1

    conn.commit()

    print(
        f"Entity comparisons created: {total_matches}"
    )

    conn.close()


if __name__ == "__main__":
    match_entities()