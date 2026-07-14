from src.database.init_db import initialize_database
from src.ingestion.generate_crm_data import generate_crm_data
from src.ingestion.load_crm import load_crm_entities
from src.standardization.entity_standardizer import standardize_entities
from src.entity_resolution.match_entities import match_entities
from src.data_quality.run_quality_checks import run_quality_checks
from src.golden_record.create_golden_records import create_golden_records
from src.reports.generate_reports import generate_reports


def run_pipeline() -> None:
    print("\n1. Initializing database")
    initialize_database()

    print("\n2. Generating CRM data")
    generate_crm_data()

    print("\n3. Loading CRM entities")
    load_crm_entities()

    print("\n4. Standardizing entities")
    standardize_entities()

    print("\n5. Matching entities")
    match_entities()

    print("\n6. Running data-quality checks")
    run_quality_checks()

    print("\n7. Creating golden records")
    create_golden_records()

    print("\n8. Generating reports")
    generate_reports()

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()