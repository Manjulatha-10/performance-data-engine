
import random
import argparse
from pathlib import Path
from datetime import date, timedelta

import pandas as pd

SEED = 20261022
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_data(employee_count=10, manager_count=3,
                  goal_count=20, checkin_count=80):
    random.seed(SEED)

    first_names = [
        "Ananya", "Rahul", "Priya", "Arjun", "Sneha",
        "Kiran", "Divya", "Rohit", "Meera", "Vikram"
    ]
    departments = [
        "Engineering", "HR", "Finance", "Sales", "Marketing"
    ]

    # 1. Managers
    managers = []
    for i in range(1, manager_count + 1):
        managers.append({
            "manager_id": f"MGR-{i:06d}",
            "manager_name": f"Manager {i}",
            "department": departments[(i - 1) % len(departments)]
        })

    # 2. Employees
    employees = []
    for i in range(1, employee_count + 1):
        manager = managers[(i - 1) % manager_count]
        employees.append({
            "employee_id": f"EMP-{i:06d}",
            "employee_name": random.choice(first_names),
            "department": departments[(i - 1) % len(departments)],
            "manager_id": manager["manager_id"],
            "employment_status": "Active"
        })

    # 3. Review cycles
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

    # 4. Goals and key results
    titles = [
        "Improve application performance",
        "Deliver project milestones",
        "Improve customer satisfaction",
        "Reduce production defects",
        "Complete technical training",
        "Improve automated test coverage"
    ]

    goals = []
    key_results = []
    employee_goal_counts = {}
    goal_owner = {}

    for i in range(1, goal_count + 1):
        employee = employees[(i - 1) % employee_count]
        emp_id = employee["employee_id"]
        employee_goal_counts[emp_id] = employee_goal_counts.get(emp_id, 0) + 1

        goal_id = f"GOAL-{emp_id}-{employee_goal_counts[emp_id]:03d}"
        target = random.choice([10, 20, 50, 100])
        actual = random.randint(0, target)

        goals.append({
            "goal_id": goal_id,
            "employee_id": emp_id,
            "goal_title": random.choice(titles),
            "status": random.choice(["Not Started", "In Progress", "Completed"])
        })

        key_results.append({
            "key_result_id": f"KR-{goal_id}-01",
            "goal_id": goal_id,
            "metric_name": "Tasks completed",
            "target_value": target,
            "actual_value": actual,
            "progress_percent": round(actual / target * 100, 2)
        })
        goal_owner[goal_id] = emp_id

    # 5. Check-ins: each check-in belongs to the goal owner
    updates = [
        "Progress is on track.",
        "Completed planned tasks this week.",
        "Some tasks need additional time.",
        "Blocked by a dependency; working on a solution.",
        "Made progress and identified next steps."
    ]

    checkins = []
    goal_ids = [g["goal_id"] for g in goals]
    today = date(2026, 10, 29)

    for i in range(1, checkin_count + 1):
        goal_id = goal_ids[(i - 1) % len(goal_ids)]
        progress = key_results[goal_ids.index(goal_id)]["progress_percent"]
        checkins.append({
            "checkin_id": f"CHK-{i:06d}",
            "goal_id": goal_id,
            "employee_id": goal_owner[goal_id],
            "checkin_date": (today - timedelta(weeks=(i - 1) % 8)).isoformat(),
            "progress_percent": progress,
            "status_update": random.choice(updates)
        })

    # 6. Competencies
    competencies = [
        {"competency_id": "COMP-001", "competency_name": "Communication"},
        {"competency_id": "COMP-002", "competency_name": "Problem Solving"},
        {"competency_id": "COMP-003", "competency_name": "Technical Skills"},
        {"competency_id": "COMP-004", "competency_name": "Teamwork"},
        {"competency_id": "COMP-005", "competency_name": "Leadership"}
    ]

    # 7. Reviews: include some incomplete reviews
    reviews = []
    for i, employee in enumerate(employees, start=1):
        reviews.append({
            "review_id": f"REV-2026-{i:06d}",
            "cycle_id": "CYCLE-2026-H1",
            "employee_id": employee["employee_id"],
            "reviewer_manager_id": employee["manager_id"],
            "rating": random.randint(1, 5),
            "review_status": random.choice(["Completed", "Pending", "Incomplete"])
        })

    # 8. Feedback: some records intentionally lack evidence references
    feedback = []
    for i, employee in enumerate(employees, start=1):
        feedback.append({
            "feedback_id": f"FDB-{i:06d}",
            "employee_id": employee["employee_id"],
            "reviewer_id": employee["manager_id"],
            "competency": random.choice(competencies)["competency_name"],
            "rating": random.randint(1, 5),
            "comments": random.choice(updates),
            "evidence_reference": f"CHK-{i:06d}" if i % 2 else ""
        })

    # 9. Development plans
    areas = [
        "Technical Skills", "Communication", "Leadership",
        "Problem Solving", "Time Management"
    ]
    actions = [
        "Complete an online course", "Attend a training session",
        "Work with a mentor", "Complete a practical project",
        "Participate in team presentations"
    ]

    development_plans = []
    for i, employee in enumerate(employees, start=1):
        development_plans.append({
            "plan_id": f"DEV-{i:06d}",
            "employee_id": employee["employee_id"],
            "development_area": random.choice(areas),
            "planned_action": random.choice(actions),
            "status": random.choice(["Not Started", "In Progress", "Completed"]),
            "target_date": "2026-12-31"
        })

    # Save each dataset
    datasets = {
        "managers": managers,
        "employees": employees,
        "review_cycles": review_cycles,
        "goals": goals,
        "key_results": key_results,
        "checkins": checkins,
        "competencies": competencies,
        "reviews": reviews,
        "feedback": feedback,
        "development_plans": development_plans
    }

    for name, records in datasets.items():
        pd.DataFrame(records).to_csv(
            OUTPUT_DIR / f"{name}.csv", index=False
        )
        print(f"{name}.csv: {len(records)} records")

    print(f"\nAll CSV files saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", choices=["starter", "full"],
                        default="starter")
    args = parser.parse_args()

    if args.scale == "starter":
        generate_data(10, 3, 20, 80)
    else:
        generate_data(3000, 500, 10000, 20000)
