import sqlite3

import pandas as pd

from src.config import DATABASE_PATH, OUTPUT_DIR


def generate_reports() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        golden_records = pd.read_sql_query(
            """
            SELECT
                golden_record_id,
                canonical_legal_name,
                canonical_lei,
                canonical_registration_number,
                canonical_address,
                country,
                industry,
                risk_rating,
                record_status,
                created_at,
                updated_at
            FROM golden_records
            ORDER BY golden_record_id
            """,
            conn,
        )

        duplicate_matches = pd.read_sql_query(
            """
            SELECT
                m.entity_match_id,
                m.entity_id_1,
                s1.standardized_legal_name AS entity_name_1,
                m.entity_id_2,
                s2.standardized_legal_name AS entity_name_2,
                m.name_similarity_score,
                m.registration_match,
                m.overall_match_score,
                m.match_classification,
                m.review_status
            FROM entity_matches m
            JOIN standardized_entities s1
                ON s1.standardized_entity_id = m.entity_id_1
            JOIN standardized_entities s2
                ON s2.standardized_entity_id = m.entity_id_2
            WHERE m.match_classification = 'DUPLICATE'
            ORDER BY m.overall_match_score DESC
            """,
            conn,
        )

        quality_summary = pd.read_sql_query(
            """
            SELECT
                q.rule_code,
                q.rule_name,
                q.severity,
                COUNT(*) AS checks_executed,
                SUM(
                    CASE
                        WHEN d.validation_status = 'PASS' THEN 1
                        ELSE 0
                    END
                ) AS passed_checks,
                SUM(
                    CASE
                        WHEN d.validation_status = 'FAIL' THEN 1
                        ELSE 0
                    END
                ) AS failed_checks,
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN d.validation_status = 'PASS' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS pass_rate_percentage
            FROM data_quality_results d
            JOIN data_quality_rules q
                ON q.rule_id = d.rule_id
            GROUP BY
                q.rule_code,
                q.rule_name,
                q.severity
            ORDER BY q.rule_code
            """,
            conn,
        )

        entity_quality_scores = pd.read_sql_query(
            """
            SELECT
                r.raw_entity_id,
                r.source_record_id,
                r.legal_name,
                COUNT(*) AS checks_executed,
                SUM(
                    CASE
                        WHEN d.validation_status = 'PASS' THEN 1
                        ELSE 0
                    END
                ) AS passed_checks,
                SUM(
                    CASE
                        WHEN d.validation_status = 'FAIL' THEN 1
                        ELSE 0
                    END
                ) AS failed_checks,
                ROUND(
                    100.0 * SUM(
                        CASE
                            WHEN d.validation_status = 'PASS' THEN 1
                            ELSE 0
                        END
                    ) / COUNT(*),
                    2
                ) AS entity_quality_score
            FROM data_quality_results d
            JOIN raw_entities r
                ON r.raw_entity_id = d.raw_entity_id
            GROUP BY
                r.raw_entity_id,
                r.source_record_id,
                r.legal_name
            ORDER BY entity_quality_score ASC
            """,
            conn,
        )

        golden_records.to_csv(
            OUTPUT_DIR / "golden_records.csv",
            index=False,
        )

        duplicate_matches.to_csv(
            OUTPUT_DIR / "duplicate_matches.csv",
            index=False,
        )

        quality_summary.to_csv(
            OUTPUT_DIR / "data_quality_summary.csv",
            index=False,
        )

        entity_quality_scores.to_csv(
            OUTPUT_DIR / "entity_quality_scores.csv",
            index=False,
        )

        print(f"Golden records exported: {len(golden_records)}")
        print(f"Duplicate matches exported: {len(duplicate_matches)}")
        print(f"Quality rules summarized: {len(quality_summary)}")
        print(f"Entity quality scores exported: {len(entity_quality_scores)}")
        print(f"Reports saved to: {OUTPUT_DIR}")

    finally:
        conn.close()


if __name__ == "__main__":
    generate_reports()