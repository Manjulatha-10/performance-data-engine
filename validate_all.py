
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

errors = []

def load_csv(name):
    path = OUTPUT_DIR / f"{name}.csv"
    if not path.exists():
        errors.append(f"Missing file: {name}.csv")
        return pd.DataFrame()
    return pd.read_csv(path, keep_default_na=False)

# Load generated datasets
managers = load_csv("managers")
employees = load_csv("employees")
goals = load_csv("goals")
key_results = load_csv("key_results")
checkins = load_csv("checkins")
reviews = load_csv("reviews")
feedback = load_csv("feedback")
development_plans = load_csv("development_plans")
review_cycles = load_csv("review_cycles")
competencies = load_csv("competencies")

# 1. Check unique primary keys
primary_keys = {
    "managers": (managers, "manager_id"),
    "employees": (employees, "employee_id"),
    "goals": (goals, "goal_id"),
    "key_results": (key_results, "key_result_id"),
    "checkins": (checkins, "checkin_id"),
    "reviews": (reviews, "review_id"),
    "feedback": (feedback, "feedback_id"),
    "development_plans": (development_plans, "plan_id"),
    "review_cycles": (review_cycles, "cycle_id"),
    "competencies": (competencies, "competency_id"),
}

for table_name, (df, key) in primary_keys.items():
    if not df.empty and key in df.columns:
        if df[key].eq("").any():
            errors.append(f"{table_name}: empty {key}")
        if df[key].duplicated().any():
            errors.append(f"{table_name}: duplicate {key}")

# 2. Check foreign-key references
def check_reference(child_df, child_column, parent_df, parent_column, label):
    if child_df.empty or parent_df.empty:
        return
    if child_column not in child_df.columns or parent_column not in parent_df.columns:
        errors.append(f"{label}: required column missing")
        return
    valid_ids = set(parent_df[parent_column])
    missing = child_df[~child_df[child_column].isin(valid_ids)]
    if not missing.empty:
        errors.append(f"{label}: {len(missing)} invalid reference(s)")

check_reference(employees, "manager_id", managers, "manager_id",
                "Employee -> Manager")
check_reference(goals, "employee_id", employees, "employee_id",
                "Goal -> Employee")
check_reference(key_results, "goal_id", goals, "goal_id",
                "Key Result -> Goal")
check_reference(checkins, "goal_id", goals, "goal_id",
                "Check-in -> Goal")
check_reference(checkins, "employee_id", employees, "employee_id",
                "Check-in -> Employee")
check_reference(reviews, "employee_id", employees, "employee_id",
                "Review -> Employee")
check_reference(reviews, "reviewer_manager_id", managers, "manager_id",
                "Review -> Manager")
check_reference(reviews, "cycle_id", review_cycles, "cycle_id",
                "Review -> Cycle")
check_reference(feedback, "employee_id", employees, "employee_id",
                "Feedback -> Employee")
check_reference(development_plans, "employee_id", employees, "employee_id",
                "Development Plan -> Employee")

# 3. Check numeric ranges
for name, df, column in [
    ("Key Results", key_results, "progress_percent"),
    ("Check-ins", checkins, "progress_percent")
]:
    if not df.empty and column in df.columns:
        values = pd.to_numeric(df[column], errors="coerce")
        if values.isna().any() or not values.between(0, 100).all():
            errors.append(f"{name}: invalid progress percentage")

if not key_results.empty:
    target = pd.to_numeric(key_results["target_value"], errors="coerce")
    actual = pd.to_numeric(key_results["actual_value"], errors="coerce")
    progress = pd.to_numeric(key_results["progress_percent"], errors="coerce")
    expected = (actual / target * 100).round(2)
    if target.isna().any() or (target <= 0).any():
        errors.append("Key Results: target must be greater than zero")
    elif not expected.equals(progress):
        errors.append("Key Results: progress does not match actual / target")

# 4. Check that check-in employee owns the referenced goal
if not checkins.empty and not goals.empty:
    goal_owners = goals.set_index("goal_id")["employee_id"].to_dict()
    for _, row in checkins.iterrows():
        if row["goal_id"] in goal_owners:
            if row["employee_id"] != goal_owners[row["goal_id"]]:
                errors.append(
                    f"Check-in {row['checkin_id']}: employee does not own goal"
                )
                break

# 5. Save and print report
report_path = OUTPUT_DIR / "validation_report.txt"

if errors:
    report = "VALIDATION FAILED\n" + "\n".join(
        f"- {error}" for error in errors
    )
    print(report)
else:
    report = "VALIDATION PASSED\nAll current checks passed."
    print(report)

report_path.write_text(report, encoding="utf-8")
print(f"\nReport saved to: {report_path}")
