# AI Prompt History — Performance  Data Engine

## 1. Purpose

AI assistance was used during the development of this project to understand the requirements, generate Python code, design data validation checks, create synthetic anomalies, build a SQLite database, and prepare project documentation.

The prompts below summarize the main AI-assisted development steps. They are reconstructed summaries of the prompts used during development, not a verbatim export of the entire chat history.

## 2. Prompt History

### Step 1: Project Setup and Planning

**Prompt summary:**

"Help me build the Performance Data Engine project step by step in VS Code. Explain each step in beginner-friendly language and help me implement the required features."

**AI assistance:**

- Broke the project into manageable development steps.
- Explained the project structure and Python file creation.
- Provided instructions for running scripts in the terminal.

**Developer contribution:** Created the project folder and Python files and followed the implementation instructions.

### Step 2: Employee and Manager Data Generation

**Prompt summary:**

"Help me generate synthetic employee and manager records in Python using deterministic IDs, a fixed random seed, and CSV output."

**AI assistance:**

- Provided sample Python code for generating managers and employees.
- Helped structure the generated records.
- Explained how to save the datasets using pandas.

**Developer contribution:** Added and executed the generation code and checked the output.

### Step 3: Full-Scale Dataset Generation

**Prompt summary:**

"Help me create a Python generator for performance management datasets, including review cycles, goals, key results, check-ins, competencies, reviews, feedback, and development plans. Support starter and full-scale configurations."

**AI assistance:**

- Helped combine dataset generation into `generate_all.py`.
- Added command-line options for starter and full-scale generation.
- Used a fixed seed for repeatability.
- Generated deterministic identifiers for the records.

**Developer contribution:** Integrated the code into the project and ran both starter and full-scale configurations.

### Step 4: Data Validation

**Prompt summary:**

"Create a Python validation script to check duplicate primary keys, missing foreign-key references, invalid progress percentages, key-result calculations, and check-in goal ownership."

**AI assistance:**

- Helped implement validation checks in `validate_all.py`.
- Added a text validation report.
- Explained how to run and interpret the validation results.

**Developer contribution:** Executed the validation script and confirmed that the current checks passed for the generated dataset.

### Step 5: Synthetic Anomaly Injection

**Prompt summary:**

"Help me create a separate anomaly dataset without modifying the clean CSV files. Include labelled examples for goal-owner mismatches, invalid progress, reviewer relationship mismatches, silent edits after cycle closure, and missing evidence references."

**AI assistance:**

- Helped implement `inject_anomalies.py`.
- Created separate copies of the datasets under `output/anomalies/`.
- Added `ground_truth.csv` to describe the five intentionally introduced anomalies.

**Developer contribution:** Ran the anomaly injection script and verified that five labelled anomaly examples were created.

### Step 6: SQLite Database Design

**Prompt summary:**

"Help me design a SQLite database for the generated performance management datasets with primary keys, foreign keys, data constraints, and parent-before-child insertion order."

**AI assistance:**

- Helped define tables and relationships in `database.py`.
- Added basic SQL constraints for selected fields.
- Added foreign-key integrity checks.

**Developer contribution:** Ran the database script and verified the printed table counts and foreign-key check result.

### Step 7: Project Documentation

**Prompt summary:**

"Help me write a README.md explaining the project purpose, technologies, dataset sizes, installation, execution commands, validation, anomaly generation, reproducibility, and limitations."

**AI assistance:**

- Drafted the README structure and content.
- Documented commands for running the generator and supporting scripts.
- Helped describe the current implementation and known limitations.

**Developer contribution:** Created and saved the README file in the project.

### Step 8: Reproducibility Testing

**Prompt summary:**

"Create a Python script that runs the full-scale generator twice and compares SHA-256 checksums of the generated CSV files to verify reproducibility."

**AI assistance:**

- Helped implement `reproducibility_test.py`.
- Added file hashing and comparison logic.
- Explained how to interpret matching and differing checksums.

**Developer contribution:** Ran the test and observed that all checked CSV files were reproducible.

## 3. Tools and Technologies

- Python 3
- pandas
- SQLite
- CSV
- SHA-256 checksums
- Visual Studio Code
- AI-assisted coding and documentation

## 4. Verification Performed

The following checks were executed during development:

1. Generated starter datasets.
2. Ran the validation script and observed `VALIDATION PASSED`.
3. Generated full-scale datasets with 3,000 employees, 500 managers, 10,000 goals, and 20,000 check-ins.
4. Ran the validation script again and observed `VALIDATION PASSED`.
5. Created five labelled synthetic anomalies in a separate folder.
6. Created the SQLite database and observed that its foreign-key checks passed.
7. Ran the reproducibility test and observed `All CSV files are reproducible`.

These results describe the checks performed by the current scripts. They do not establish that every assessment requirement or business rule has been implemented.

## 5. Limitations and Further Work

The current implementation is a working prototype that covers synthetic data generation, selected data-quality checks, labelled anomaly examples, SQLite loading, and reproducibility testing.

Further work is needed to implement and validate additional requirements such as manager-transfer history, complete lifecycle and effective-date rules, comprehensive evidence traceability, audit history, and broader anomaly coverage.

The developer remains responsible for reviewing the code, understanding the implementation, testing the outputs, and ensuring the final submission meets the assessment requirements.
