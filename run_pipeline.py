import subprocess
import sys


PIPELINE_STEPS = [
    ("Initialize database", "src.database.init_db"),
    ("Generate CRM data", "src.ingestion.generate_crm_data"),
    ("Load CRM entities", "src.ingestion.load_crm"),
    ("Standardize entities", "src.standardization.entity_standardizer"),
    ("Match entities", "src.entity_resolution.match_entities"),
    ("Run data-quality checks", "src.data_quality.run_quality_checks"),
    ("Create golden records", "src.golden_record.create_golden_records"),
    ("Generate reports", "src.reports.generate_reports"),
]


def run_module(step_name: str, module_name: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"Running: {step_name}")
    print(f"Module: {module_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline stopped because '{step_name}' failed."
        )


def run_pipeline() -> None:
    for step_name, module_name in PIPELINE_STEPS:
        run_module(step_name, module_name)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()