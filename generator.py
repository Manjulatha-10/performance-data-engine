
import random
from pathlib import Path

import pandas as pd

SEED = 20261022

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_managers(count=3):
    random.seed(SEED)

    names = ["Ravi Kumar", "Priya Sharma", "Suresh Reddy"]

    managers = []

    for i in range(1, count + 1):
        managers.append({
            "manager_id": f"MGR-{i:06d}",
            "manager_name": names[i - 1],
            "department": ["Engineering", "Finance", "HR"][i - 1]
        })

    return managers


def generate_employees(managers, count=10):
    random.seed(SEED)

    first_names = [
        "Ananya", "Rahul", "Priya", "Arjun", "Sneha",
        "Kiran", "Divya", "Rohit", "Meera", "Vikram"
    ]

    departments = [
        "Engineering", "HR", "Finance", "Sales", "Marketing"
    ]

    employees = []

    for i in range(1, count + 1):
        manager = managers[(i - 1) % len(managers)]

        employees.append({
            "employee_id": f"EMP-{i:06d}",
            "employee_name": random.choice(first_names),
            "department": random.choice(departments),
            "manager_id": manager["manager_id"],
            "employment_status": "Active"
        })

    return employees


if __name__ == "__main__":
    managers = generate_managers()
    employees = generate_employees(managers)

    managers_df = pd.DataFrame(managers)
    employees_df = pd.DataFrame(employees)

    managers_df.to_csv(OUTPUT_DIR / "managers.csv", index=False)
    employees_df.to_csv(OUTPUT_DIR / "employees.csv", index=False)

    print(f"Managers generated: {len(managers_df)}")
    print(f"Employees generated: {len(employees_df)}")
    print("\nManagers:")
    print(managers_df)
    print("\nEmployees:")
    print(employees_df)
    print(f"\nCSV files saved in: {OUTPUT_DIR}")
