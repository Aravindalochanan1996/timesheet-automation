
from datetime import datetime
from app.report.leave_metrics import extract_leave_metrics

def parse_month_safe(month_str):
    try:
        return datetime.strptime(month_str, "%b-%Y")
    except:
        return datetime.min

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

    # ✅ Updated Header
    ws.append([
        "Name",
        "Emp ID",
        "Month",
        "Total Hours",
        "Public Holidays",
        "Unpaid Leave Count",
        "Unpaid Leave Dates",
        "Final Work Hours"
    ])

    # ✅ Safe sorting (latest month first)
    sorted_records = sorted(
        records,
        key=lambda r: parse_month_safe(r.get("month", "")),
        reverse=True
    )

    for r in sorted_records:
        total_hours = calculate_total_hours(r["entries"])

        # ✅ Reuse same logic
        public_holidays, unpaid_count, unpaid_dates = extract_leave_metrics(
            r["entries"], r["month"]
        )

        final_hours = round(total_hours - (unpaid_count * 8), 2)

        ws.append([
            str(r.get("name", "")).strip(),
            r.get("emp_id", ""),
            r.get("month", ""),
            total_hours,
            public_holidays,
            unpaid_count,
            unpaid_dates,
            final_hours
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