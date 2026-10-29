
import random
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "performance.db"

SEED = 20261022


def generate_feedback():
    random.seed(SEED)

    with sqlite3.connect(DB_PATH) as connection:
        employees = pd.read_sql_query(
            "SELECT employee_id, manager_id FROM employees ORDER BY employee_id",
            connection
        )

    competencies = [
        "Communication",
        "Problem Solving",
        "Technical Skills",
        "Teamwork",
        "Leadership"
    ]

    comments = [
        "Demonstrates consistent progress.",
        "Communicates clearly with the team.",
        "Should improve planning and prioritization.",
        "Shows strong problem-solving skills.",
        "Could benefit from additional technical practice."
    ]

    feedback_records = []

    for index, employee in employees.iterrows():
        feedback_records.append({
            "feedback_id": f"FDB-{index + 1:06d}",
            "employee_id": employee["employee_id"],
            "reviewer_id": employee["manager_id"],
            "competency": random.choice(competencies),
            "rating": random.randint(1, 5),
            "comments": random.choice(comments),
            "evidence_reference": (
                f"CHK-{index + 1:06d}"
                if index % 2 == 0 else None
            )
        })

    df = pd.DataFrame(feedback_records)
    df.to_csv(OUTPUT_DIR / "feedback.csv", index=False)

    print(f"Feedback records generated: {len(df)}")
    print("Saved feedback.csv")


if __name__ == "__main__":
    generate_feedback()
