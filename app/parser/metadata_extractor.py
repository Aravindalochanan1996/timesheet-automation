import re

def extract_metadata(text):
    name = re.search(r"Employee Timesheet Report\s+(.*?)\s+\(", text, re.S)
    emp_id = re.search(r"\((\d+)\)", text)
    month = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}", text)

    return {
        "name": name.group(1).strip() if name else "",
        "emp_id": emp_id.group(1) if emp_id else "",
        "month": month.group(0) if month else ""
    }