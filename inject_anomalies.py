
from pathlib import Path
import shutil
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
ANOMALY_DIR = OUTPUT_DIR / "anomalies"
ANOMALY_DIR.mkdir(parents=True, exist_ok=True)

# Copy original CSV datasets so clean data stays unchanged.
for source in OUTPUT_DIR.glob("*.csv"):
    shutil.copy2(source, ANOMALY_DIR / source.name)

employees = pd.read_csv(ANOMALY_DIR / "employees.csv", dtype=str)
goals = pd.read_csv(ANOMALY_DIR / "goals.csv", dtype=str)
checkins = pd.read_csv(ANOMALY_DIR / "checkins.csv", dtype=str)
reviews = pd.read_csv(ANOMALY_DIR / "reviews.csv", dtype=str)
cycles = pd.read_csv(ANOMALY_DIR / "review_cycles.csv", dtype=str)
feedback = pd.read_csv(ANOMALY_DIR / "feedback.csv", dtype=str)

ground_truth = []

def label(anomaly_id, dataset, record_id, anomaly_type,
          field, original, changed, description):
    ground_truth.append({
        "anomaly_id": anomaly_id,
        "dataset": dataset,
        "record_id": record_id,
        "anomaly_type": anomaly_type,
        "field_changed": field,
        "original_value": original,
        "anomalous_value": changed,
        "description": description
    })

# 1. Goal owner mismatch: check-in employee does not own the goal.
goal_id = goals.iloc[0]["goal_id"]
owner_id = goals.iloc[0]["employee_id"]
other_employee = employees.loc[
    employees["employee_id"] != owner_id, "employee_id"
].iloc[0]

idx = checkins.index[checkins["goal_id"] == goal_id][0]
old_value = checkins.at[idx, "employee_id"]
checkins.at[idx, "employee_id"] = other_employee

label(
    "ANOM-001", "checkins", checkins.at[idx, "checkin_id"],
    "goal_owner_mismatch", "employee_id", old_value, other_employee,
    "Check-in employee differs from the goal owner."
)

# 2. Progress outside the 0-100 scale, with no explanation.
idx = 1
old_value = checkins.at[idx, "progress_percent"]
checkins.at[idx, "progress_percent"] = "150"
checkins.at[idx, "status_update"] = "Progress is on track."

label(
    "ANOM-002", "checkins", checkins.at[idx, "checkin_id"],
    "progress_out_of_range", "progress_percent", old_value, "150",
    "Progress exceeds 100 and the update gives no explanation."
)

# 3. Reviewer is a valid manager, but not the employee's assigned manager.
idx = 0
employee_id = reviews.at[idx, "employee_id"]
assigned_manager = employees.loc[
    employees["employee_id"] == employee_id, "manager_id"
].iloc[0]
other_manager = employees.loc[
    employees["manager_id"] != assigned_manager, "manager_id"
].iloc[0]

old_value = reviews.at[idx, "reviewer_manager_id"]
reviews.at[idx, "reviewer_manager_id"] = other_manager

label(
    "ANOM-003", "reviews", reviews.at[idx, "review_id"],
    "reviewer_relationship_mismatch", "reviewer_manager_id",
    old_value, other_manager,
    "Reviewer exists but is not the employee's assigned manager."
)

# 4. Simulate a silent edit after a review cycle is closed.
closed_cycle = cycles.loc[cycles["status"] == "Closed"].iloc[0]
event = pd.DataFrame([{
    "event_id": "EVT-ANOM-001",
    "goal_id": goals.iloc[0]["goal_id"],
    "cycle_id": closed_cycle["cycle_id"],
    "cycle_end_date": closed_cycle["end_date"],
    "edit_date": "2026-07-15",
    "edit_field": "goal_title",
    "old_value": goals.iloc[0]["goal_title"],
    "new_value": "Edited after cycle closure",
    "edit_rationale": ""
}])
event.to_csv(ANOMALY_DIR / "goal_change_events.csv", index=False)

label(
    "ANOM-004", "goal_change_events", "EVT-ANOM-001",
    "silent_edit_after_cycle_close", "edit_rationale",
    "Not applicable", "",
    "A goal edit occurs after cycle closure without a rationale."
)

# 5. Feedback points to evidence that does not exist.
idx = 0
old_value = feedback.at[idx, "evidence_reference"]
feedback.at[idx, "evidence_reference"] = "CHK-999999"

label(
    "ANOM-005", "feedback", feedback.at[idx, "feedback_id"],
    "untraceable_feedback_evidence", "evidence_reference",
    old_value, "CHK-999999",
    "Feedback references a check-in ID that does not exist."
)

# Save anomaly datasets separately from clean datasets.
checkins.to_csv(ANOMALY_DIR / "checkins.csv", index=False)
reviews.to_csv(ANOMALY_DIR / "reviews.csv", index=False)
feedback.to_csv(ANOMALY_DIR / "feedback.csv", index=False)

truth_path = ANOMALY_DIR / "ground_truth.csv"
pd.DataFrame(ground_truth).to_csv(truth_path, index=False)

print("Anomaly dataset created successfully.")
print(f"Anomalies labelled: {len(ground_truth)}")
print(f"Anomaly files saved in: {ANOMALY_DIR}")
print(f"Ground truth saved in: {truth_path}")
