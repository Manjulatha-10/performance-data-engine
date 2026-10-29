# Data Dictionary — Performance Data Engine

## Overview
This project generates synthetic employee performance data using Python, CSV files, and SQLite.

## Dataset files

| File | Purpose |
|---|---|
| `managers.csv` | Manager identifiers and details |
| `employees.csv` | Employee details and assigned manager |
| `review_cycles.csv` | Performance review cycles and statuses |
| `goals.csv` | Employee goals and their statuses |
| `key_results.csv` | Goal targets, actual values, and progress |
| `checkins.csv` | Goal progress updates recorded by employees |
| `competencies.csv` | Competencies used for performance feedback |
| `reviews.csv` | Employee review records and review status |
| `feedback.csv` | Employee feedback and evidence references |
| `development_plans.csv` | Employee development objectives and status |

## Key relationships
- Employees reference managers through `manager_id`.
- Goals reference employees through `employee_id`.
- Key results reference goals through `goal_id`.
- Check-ins reference goals and employees.
- Reviews reference employees, managers, and review cycles.
- Feedback references employees and may include evidence references.
- Development plans reference employees.

## Data quality
The validation scripts check identifiers, foreign-key relationships, progress ranges, key-result progress calculations, and selected consistency rules.

## Reproducibility
The generator uses seed `20261022`. Run `python reproducibility_test.py` to compare generated CSV files across repeated runs.

## Anomaly data
Intentional anomalies are stored separately in `output/anomalies/`. The `ground_truth.csv` file labels injected anomalies and should be kept separate from model input features.

## Limitations
This is synthetic data. Manager-transfer history, complete lifecycle enforcement, and comprehensive evidence-traceability validation are not fully implemented.