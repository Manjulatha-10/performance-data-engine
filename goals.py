
import random
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "performance.db"

SEED = 20261022


def generate_goals():
    random.seed(SEED)

    # Read existing employees from the database
    with sqlite3.connect(DB_PATH) as connection:
        employees = pd.read_sql_query(
            "SELECT employee_id FROM employees ORDER BY employee_id",
            connection
        )

    goal_titles = [
        "Improve application performance",
        "Deliver project milestones",
        "Improve customer satisfaction",
        "Reduce production defects",
        "Complete technical training",
        "Improve automated test coverage"
    ]

    goals = []
    key_results = []

    goal_number = 1

    for _, employee in employees.iterrows():
        # Each employee receives two goals
        for _ in range(2):
            goal_id = f"GOAL-{employee['employee_id']}-{goal_number:03d}"
            title = random.choice(goal_titles)

            target = random.choice([10, 20, 50, 100])
            actual = random.randint(0, target)

            goals.append({
                "goal_id": goal_id,
                "employee_id": employee["employee_id"],
                "goal_title": title,
                "status": "In Progress"
            })

            key_results.append({
                "key_result_id": f"KR-{goal_id}-01",
                "goal_id": goal_id,
                "metric_name": "Tasks completed",
                "target_value": target,
                "actual_value": actual,
                "progress_percent": round(actual / target * 100, 2)
            })

            goal_number += 1

    goals_df = pd.DataFrame(goals)
    key_results_df = pd.DataFrame(key_results)

    goals_df.to_csv(OUTPUT_DIR / "goals.csv", index=False)
    key_results_df.to_csv(
        OUTPUT_DIR / "key_results.csv", index=False
    )

    print(f"Goals generated: {len(goals_df)}")
    print(f"Key results generated: {len(key_results_df)}")
    print("Saved goals.csv and key_results.csv")


if __name__ == "__main__":
    generate_goals()
