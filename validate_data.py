
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "output" / "performance.db"


def validate_database():
    errors = []

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        # 1. Check duplicate employee IDs
        duplicates = connection.execute("""
            SELECT employee_id, COUNT(*)
            FROM employees
            GROUP BY employee_id
            HAVING COUNT(*) > 1
        """).fetchall()

        if duplicates:
            errors.append(f"Duplicate employee IDs: {duplicates}")

        # 2. Check duplicate manager IDs
        duplicates = connection.execute("""
            SELECT manager_id, COUNT(*)
            FROM managers
            GROUP BY manager_id
            HAVING COUNT(*) > 1
        """).fetchall()

        if duplicates:
            errors.append(f"Duplicate manager IDs: {duplicates}")

        # 3. Check employees without valid managers
        missing_managers = connection.execute("""
            SELECT e.employee_id, e.manager_id
            FROM employees e
            LEFT JOIN managers m
                ON e.manager_id = m.manager_id
            WHERE m.manager_id IS NULL
        """).fetchall()

        if missing_managers:
            errors.append(f"Employees with missing managers: {missing_managers}")

        # 4. Check database foreign key violations
        fk_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if fk_errors:
            errors.append(f"Foreign key violations: {fk_errors}")

        # Print row counts
        employee_count = connection.execute(
            "SELECT COUNT(*) FROM employees"
        ).fetchone()[0]

        manager_count = connection.execute(
            "SELECT COUNT(*) FROM managers"
        ).fetchone()[0]

    print("\n--- DATA VALIDATION REPORT ---")
    print(f"Employees checked: {employee_count}")
    print(f"Managers checked: {manager_count}")

    if errors:
        print(f"FAILED: {len(errors)} validation issue(s)")
        for error in errors:
            print("-", error)
    else:
        print("PASSED: All current validation checks passed!")


if __name__ == "__main__":
    validate_database()
