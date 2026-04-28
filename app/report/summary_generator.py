
from datetime import datetime

def convert_to_hours(time_str):
    if not time_str or time_str == "--:--":
        return 0

    try:
        h, m = time_str.split(":")
        return int(h) + int(m) / 60
    except:
        return 0


def calculate_total_hours(entries):
    total = 0

    for day in entries.values():
        total += convert_to_hours(day.get("hours"))

    return round(total, 2)


def generate_summary_sheet(wb, records):
    ws = wb.create_sheet(title="Summary")

    # Header
    ws.append(["Name", "Emp ID", "Month", "Total Hours"])

    # ✅ Sort records by Month (latest first)
    sorted_records = sorted(
        records,
        key=lambda r: datetime.strptime(r["month"], "%b-%Y"),
        reverse=True
    )

    for r in sorted_records:
        total_hours = calculate_total_hours(r["entries"])

        ws.append([
            r["name"].strip(),
            r["emp_id"],
            r["month"],
            total_hours
        ])

def parse_month(m):
    try:
        return datetime.strptime(m, "%b-%Y")
    except:
        return datetime.min  # fallback

    sorted_records = sorted(
    records,
    key=lambda r: (
        datetime.strptime(r["month"], "%b-%Y"),
        r["name"]
    ),
    reverse=True
)