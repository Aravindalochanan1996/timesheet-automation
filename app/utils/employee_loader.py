import pandas as pd


def generate_timesheet_enrolled_sheet(wb, records, employee_file):

    # =========================
    # Read employee master
    # =========================
    df = pd.read_excel(employee_file)

    employees = []

    for _, row in df.iterrows():

        employees.append({
            "name": str(row.get("Employee Name", "")).strip(),
            "old_id": str(row.get("Old Employee ID", "")).strip(),
            "new_id": str(row.get("New Employee ID", "")).strip()
        })
        print(employees[:2])