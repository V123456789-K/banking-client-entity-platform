from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REFERENCE_DATA_DIR = DATA_DIR / "reference"

OUTPUT_DIR = PROJECT_ROOT / "output"
SQL_DIR = PROJECT_ROOT / "sql"

DATABASE_PATH = PROJECT_ROOT / "banking_client_entities.db"
SCHEMA_PATH = SQL_DIR / "schema.sql"