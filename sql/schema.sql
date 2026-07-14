PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS source_systems (
    source_system_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system_name TEXT NOT NULL UNIQUE,
    source_type TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_entities (
    raw_entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_system_id INTEGER NOT NULL,
    source_record_id TEXT,
    legal_name TEXT,
    trading_name TEXT,
    lei TEXT,
    registration_number TEXT,
    tax_identifier TEXT,
    legal_form TEXT,
    industry TEXT,
    country TEXT,
    address_line_1 TEXT,
    address_line_2 TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    onboarding_status TEXT,
    risk_rating TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (source_system_id)
        REFERENCES source_systems(source_system_id)
);

CREATE TABLE IF NOT EXISTS standardized_entities (
    standardized_entity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_entity_id INTEGER NOT NULL UNIQUE,
    standardized_legal_name TEXT,
    standardized_address TEXT,
    standardized_country TEXT,
    normalized_lei TEXT,
    normalized_registration_number TEXT,
    standardization_status TEXT,
    processed_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_entity_id)
        REFERENCES raw_entities(raw_entity_id)
);

CREATE TABLE IF NOT EXISTS entity_matches (
    entity_match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id_1 INTEGER NOT NULL,
    entity_id_2 INTEGER NOT NULL,
    name_similarity_score REAL,
    address_similarity_score REAL,
    registration_match INTEGER,
    lei_match INTEGER,
    overall_match_score REAL,
    match_classification TEXT,
    review_status TEXT DEFAULT 'PENDING',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (entity_id_1)
        REFERENCES standardized_entities(standardized_entity_id),

    FOREIGN KEY (entity_id_2)
        REFERENCES standardized_entities(standardized_entity_id)
);

CREATE TABLE IF NOT EXISTS golden_records (
    golden_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_legal_name TEXT NOT NULL,
    canonical_lei TEXT,
    canonical_registration_number TEXT,
    canonical_address TEXT,
    country TEXT,
    industry TEXT,
    risk_rating TEXT,
    record_status TEXT DEFAULT 'ACTIVE',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS golden_record_members (
    golden_record_id INTEGER NOT NULL,
    standardized_entity_id INTEGER NOT NULL,
    survivorship_priority INTEGER,
    source_confidence_score REAL,

    PRIMARY KEY (
        golden_record_id,
        standardized_entity_id
    ),

    FOREIGN KEY (golden_record_id)
        REFERENCES golden_records(golden_record_id),

    FOREIGN KEY (standardized_entity_id)
        REFERENCES standardized_entities(standardized_entity_id)
);

CREATE TABLE IF NOT EXISTS data_quality_rules (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_code TEXT NOT NULL UNIQUE,
    rule_name TEXT NOT NULL,
    rule_description TEXT,
    severity TEXT NOT NULL,
    target_field TEXT,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS data_quality_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    raw_entity_id INTEGER,
    rule_id INTEGER NOT NULL,
    validation_status TEXT NOT NULL,
    failure_reason TEXT,
    validated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (raw_entity_id)
        REFERENCES raw_entities(raw_entity_id),

    FOREIGN KEY (rule_id)
        REFERENCES data_quality_rules(rule_id)
);

CREATE TABLE IF NOT EXISTS onboarding_cases (
    onboarding_case_id INTEGER PRIMARY KEY AUTOINCREMENT,
    golden_record_id INTEGER,
    application_date TEXT,
    completion_date TEXT,
    onboarding_status TEXT,
    kyc_status TEXT,
    assigned_team TEXT,
    manual_review_required INTEGER DEFAULT 0,

    FOREIGN KEY (golden_record_id)
        REFERENCES golden_records(golden_record_id)
);