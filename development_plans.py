
import random
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "performance.db"

SEED = 20261022


def generate_development_plans():
    random.seed(SEED)

    with sqlite3.connect(DB_PATH) as connection:
        employees = pd.read_sql_query(
            "SELECT employee_id FROM employees ORDER BY employee_id",
            connection
        )

    development_areas = [
        "Technical Skills",
        "Communication",
        "Leadership",
        "Problem Solving",
        "Time Management"
    ]

    actions = [
        "Complete an online course",
        "Attend a training session",
        "Work with a mentor",
        "Complete a practical project",
        "Participate in team presentations"
    ]

    plans = []

    for index, employee in employees.iterrows():
        plans.append({
            "plan_id": f"DEV-{index + 1:06d}",
            "employee_id": employee["employee_id"],
            "development_area": random.choice(development_areas),
            "planned_action": random.choice(actions),
            "status": random.choice(
                ["Not Started", "In Progress", "Completed"]
            ),
            "target_date": "2026-12-31"
        })

    df = pd.DataFrame(plans)
    df.to_csv(OUTPUT_DIR / "development_plans.csv", index=False)

    print(f"Development plans generated: {len(df)}")
    print("Saved development_plans.csv")


if __name__ == "__main__":
    generate_development_plans()
