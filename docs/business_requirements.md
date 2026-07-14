# Banking Client Entity Data Platform

## 1. Project Overview

The Banking Client Entity Data Platform is designed to collect, standardize, validate and consolidate legal entity information received from multiple banking and reference-data sources.

The platform will support client onboarding, KYC operations, entity data stewardship, duplicate detection and regulatory reporting.

## 2. Business Problem

Banks receive client and legal entity information from multiple systems such as CRM platforms, onboarding applications, legal entity reference-data providers and external company registries.

The same organization may be represented differently across systems.

Examples:

- ABC Technologies Pvt Ltd
- ABC Technologies Private Limited
- A.B.C. Technologies Pvt. Ltd.
- ABC Tech Private Limited

These inconsistencies can create duplicate client records, onboarding delays, incorrect risk classifications and regulatory-reporting issues.

## 3. Business Objective

Build a trusted client entity data platform that:

- Ingests entity information from multiple sources
- Standardizes company names and addresses
- Validates Legal Entity Identifiers
- Detects duplicate entities
- Creates trusted golden records
- Measures data quality
- Supports client onboarding and KYC reporting
- Provides executive dashboards

## 4. Key Stakeholders

- Client Onboarding Team
- KYC Operations Team
- Data Governance Team
- Client Data Stewards
- Risk and Compliance Team
- Regulatory Reporting Team
- Relationship Managers
- Data Engineering Team

## 5. Key Business Questions

- How many unique legal entities exist?
- How many duplicate records are present?
- Which entities are missing LEIs?
- Which records have incomplete registration or address details?
- Which source systems produce the most data-quality failures?
- What percentage of entity records meet onboarding requirements?
- Which entities require manual review?
- How long does client onboarding take?
- Which countries or industries have the highest-risk entities?

## 6. Core Deliverables

- Multi-source ingestion pipeline
- Standardized legal entity dataset
- Entity-resolution engine
- Duplicate-detection report
- Golden-record generation
- Automated data-quality rules
- Data-quality scorecard
- SQL analytics layer
- Power BI dashboard
- Streamlit entity-search application
- Technical documentation
- GitHub repository