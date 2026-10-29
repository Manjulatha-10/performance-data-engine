
import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "performance.db"


def create_database():
    files = {
        "managers": "managers.csv",
        "employees": "employees.csv",
        "review_cycles": "review_cycles.csv",
        "goals": "goals.csv",
        "key_results": "key_results.csv",
        "checkins": "checkins.csv",
        "competencies": "competencies.csv",
        "reviews": "reviews.csv",
        "feedback": "feedback.csv",
        "development_plans": "development_plans.csv",
    }

    data = {}
    for table, filename in files.items():
        path = OUTPUT_DIR / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing required file: {path}")
        data[table] = pd.read_csv(path)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        # Drop child tables before parent tables.
        connection.executescript("""
            DROP TABLE IF EXISTS feedback;
            DROP TABLE IF EXISTS reviews;
            DROP TABLE IF EXISTS development_plans;
            DROP TABLE IF EXISTS checkins;
            DROP TABLE IF EXISTS key_results;
            DROP TABLE IF EXISTS goals;
            DROP TABLE IF EXISTS competencies;
            DROP TABLE IF EXISTS review_cycles;
            DROP TABLE IF EXISTS employees;
            DROP TABLE IF EXISTS managers;

            CREATE TABLE managers (
                manager_id TEXT PRIMARY KEY,
                manager_name TEXT NOT NULL,
                department TEXT NOT NULL
            );

            CREATE TABLE employees (
                employee_id TEXT PRIMARY KEY,
                employee_name TEXT NOT NULL,
                department TEXT NOT NULL,
                manager_id TEXT NOT NULL,
                employment_status TEXT NOT NULL
                    CHECK (employment_status IN ('Active', 'Inactive')),
                FOREIGN KEY (manager_id)
                    REFERENCES managers(manager_id)
            );

            CREATE TABLE review_cycles (
                cycle_id TEXT PRIMARY KEY,
                cycle_name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('Open', 'Closed')),
                CHECK (start_date <= end_date)
            );

            CREATE TABLE goals (
                goal_id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL,
                goal_title TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('Not Started', 'In Progress', 'Completed')),
                FOREIGN KEY (employee_id)
                    REFERENCES employees(employee_id)
            );

            CREATE TABLE key_results (
                key_result_id TEXT PRIMARY KEY,
                goal_id TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                target_value REAL NOT NULL CHECK (target_value > 0),
                actual_value REAL NOT NULL CHECK (actual_value >= 0),
                progress_percent REAL NOT NULL
                    CHECK (progress_percent BETWEEN 0 AND 100),
                FOREIGN KEY (goal_id) REFERENCES goals(goal_id)
            );

            CREATE TABLE checkins (
                checkin_id TEXT PRIMARY KEY,
                goal_id TEXT NOT NULL,
                employee_id TEXT NOT NULL,
                checkin_date TEXT NOT NULL,
                progress_percent REAL NOT NULL
                    CHECK (progress_percent BETWEEN 0 AND 100),
                status_update TEXT NOT NULL,
                FOREIGN KEY (goal_id) REFERENCES goals(goal_id),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            );

            CREATE TABLE competencies (
                competency_id TEXT PRIMARY KEY,
                competency_name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE reviews (
                review_id TEXT PRIMARY KEY,
                cycle_id TEXT NOT NULL,
                employee_id TEXT NOT NULL,
                reviewer_manager_id TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                review_status TEXT NOT NULL
                    CHECK (review_status IN ('Completed', 'Pending', 'Incomplete')),
                FOREIGN KEY (cycle_id) REFERENCES review_cycles(cycle_id),
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
                FOREIGN KEY (reviewer_manager_id) REFERENCES managers(manager_id)
            );

            CREATE TABLE feedback (
                feedback_id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL,
                reviewer_id TEXT NOT NULL,
                competency TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comments TEXT NOT NULL,
                evidence_reference TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
                FOREIGN KEY (reviewer_id) REFERENCES managers(manager_id),
                FOREIGN KEY (competency) REFERENCES competencies(competency_name)
            );

            CREATE TABLE development_plans (
                plan_id TEXT PRIMARY KEY,
                employee_id TEXT NOT NULL,
                development_area TEXT NOT NULL,
                planned_action TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('Not Started', 'In Progress', 'Completed')),
                target_date TEXT NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
            );
        """)

        # Load parent tables before dependent tables.
        load_order = [
            "managers",
            "employees",
            "review_cycles",
            "goals",
            "key_results",
            "checkins",
            "competencies",
            "reviews",
            "feedback",
            "development_plans",
        ]

        for table in load_order:
            data[table].to_sql(
                table, connection, if_exists="append", index=False
            )

        # Check database foreign-key integrity.
        fk_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        print("Database record counts:")
        for table in load_order:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            print(f"{table}: {count}")

        if fk_errors:
            print("\nFOREIGN KEY CHECK FAILED:")
            for error in fk_errors[:10]:
                print(error)
            raise ValueError("Database contains foreign-key errors.")

        print("\nDatabase created and foreign-key checks passed!")
        print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    create_database()
