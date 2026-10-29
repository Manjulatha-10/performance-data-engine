
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
DB_PATH = OUTPUT_DIR / "performance.db"

SEED = 20261022


def generate_checkins():
    random.seed(SEED)

    with sqlite3.connect(DB_PATH) as connection:
        goals = pd.read_sql_query(
            "SELECT goal_id, employee_id FROM goals ORDER BY goal_id",
            connection
        )

    updates = [
        "Progress is on track.",
        "Completed planned tasks this week.",
        "Some tasks need additional time.",
        "Blocked by a dependency; working on a solution.",
        "Made progress and identified next steps."
    ]

    checkins = []
    checkin_number = 1
    today = date(2026, 10, 29)

    for _, goal in goals.iterrows():
        for weeks_ago in [3, 2, 1, 0]:
            checkin_date = today - timedelta(weeks=weeks_ago)

            checkins.append({
                "checkin_id": f"CHK-{checkin_number:06d}",
                "goal_id": goal["goal_id"],
                "employee_id": goal["employee_id"],
                "checkin_date": checkin_date.isoformat(),
                "progress_percent": random.randint(0, 100),
                "status_update": random.choice(updates)
            })

            checkin_number += 1

    df = pd.DataFrame(checkins)
    df.to_csv(OUTPUT_DIR / "checkins.csv", index=False)

    print(f"Check-ins generated: {len(df)}")
    print(f"Saved to: {OUTPUT_DIR / 'checkins.csv'}")


if __name__ == "__main__":
    generate_checkins()
