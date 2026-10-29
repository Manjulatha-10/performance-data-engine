
# Performance Data Engine

## Overview

A Python-based synthetic employee performance data generator for
testing goal management, employee reviews, check-ins, feedback,
competencies, and development planning workflows.

The project generates reproducible CSV datasets, loads clean datasets
into SQLite, validates key data-quality rules, and creates a separate
dataset containing labelled synthetic anomalies.

## Technology Stack

- Python 3
- pandas
- SQLite
- CSV

## Data Generated

The full-scale configuration generates:

| Dataset | Record count |
|---|---:|
| Managers | 500 |
| Employees | 3,000 |
| Review cycles | 2 |
| Goals | 10,000 |
| Key results | 10,000 |
| Check-ins | 20,000 |
| Competencies | 5 |
| Reviews | 3,000 |
| Feedback | 3,000 |
| Development plans | 3,000 |

## Project Structure

```text
performance-data-engine/
├── output/
│   ├── managers.csv
│   ├── employees.csv
│   ├── review_cycles.csv
│   ├── goals.csv
│   ├── key_results.csv
│   ├── checkins.csv
│   ├── competencies.csv
│   ├── reviews.csv
│   ├── feedback.csv
│   ├── development_plans.csv
│   ├── performance.db
│   ├── validation_report.txt
│   └── anomalies/
│       └── ground_truth.csv
├── generate_all.py
├── inject_anomalies.py
├── database.py
├── validate_all.py
└── README.md
```

## Requirements

Install Python 3 and the pandas package.

```bash
python -m pip install pandas
```

## How to Run

### 1. Generate starter data

```bash
python generate_all.py --scale starter
```

### 2. Generate full-scale data

```bash
python generate_all.py --scale full
```

Both configurations use the fixed seed `20261022`.

**Note:** Generating data overwrites CSV files with the same names
inside `output/`.

### 3. Validate generated data

```bash
python validate_all.py
```

The validation script checks primary-key uniqueness, selected
foreign-key references, progress ranges, key-result calculations,
and check-in ownership. It writes a report to
`output/validation_report.txt`.

### 4. Create the SQLite database

```bash
python database.py
```

This rebuilds `output/performance.db` from the clean CSV datasets
and checks database foreign-key integrity.

### 5. Generate labelled anomalies

```bash
python inject_anomalies.py
```

Anomaly datasets are stored separately in `output/anomalies/`.
The `ground_truth.csv` file identifies five intentional anomaly
examples and records their types and changed values.

Run this after generating the clean data.

## Reproducibility

The generator uses the fixed random seed `20261022` so that the
same configuration can be regenerated consistently. To verify
reproducibility, generate the same configuration twice and compare
the output CSV file checksums.

## Data Quality and Limitations

The generated data is synthetic and is not intended to represent
real employees.

The current implementation provides a working starter/full-scale
generator and initial validation. It does not yet implement every
possible lifecycle rule, manager-transfer history, review-cycle
transition, or evidence-traceability rule. The anomaly dataset
contains five deliberately created examples, not an exhaustive
anomaly catalogue.

## AI Assistance

AI assistance was used during development for coding guidance,
debugging support, validation design, and documentation drafting.
The developer is responsible for reviewing the generated code,
running the tests, and understanding the implementation.
