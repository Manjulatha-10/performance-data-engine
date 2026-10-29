
import random
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "performance.db"

SEED = 20261022


def generate_reviews():
    random.seed(SEED)

    # Read employees from the database
    with sqlite3.connect(DB_PATH) as connection:
        employees = pd.read_sql_query(
            "SELECT employee_id, manager_id FROM employees ORDER BY employee_id",
            connection
        )

    review_cycles = [
        {
            "cycle_id": "CYCLE-2026-H1",
            "cycle_name": "2026 First Half",
            "start_date": "2026-01-01",
            "end_date": "2026-06-30",
            "status": "Closed"
        },
        {
            "cycle_id": "CYCLE-2026-H2",
            "cycle_name": "2026 Second Half",
            "start_date": "2026-07-01",
            "end_date": "2026-12-31",
            "status": "Open"
        }
    ]

    review_records = []
    ratings = [1, 2, 3, 4, 5]

    for index, employee in employees.iterrows():
        # Create a review for the first-half cycle
        review_records.append({
            "review_id": f"REV-2026-{index + 1:06d}",
            "cycle_id": "CYCLE-2026-H1",
            "employee_id": employee["employee_id"],
            "reviewer_manager_id": employee["manager_id"],
            "rating": random.choice(ratings),
            "review_status": random.choice(
                ["Completed", "Pending", "Incomplete"]
            )
        })

    cycles_df = pd.DataFrame(review_cycles)
    reviews_df = pd.DataFrame(review_records)

    cycles_df.to_csv(OUTPUT_DIR / "review_cycles.csv", index=False)
    reviews_df.to_csv(OUTPUT_DIR / "reviews.csv", index=False)

    print(f"Review cycles generated: {len(cycles_df)}")
    print(f"Reviews generated: {len(reviews_df)}")
    print("Saved review_cycles.csv and reviews.csv")


if __name__ == "__main__":
    generate_reviews()
