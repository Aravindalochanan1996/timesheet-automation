from datetime import datetime

def is_weekend(year, month, day):
    try:
        return datetime(year, month, day).weekday() >= 5
    except:
        return False


def calculate_metrics(entries, month_str):
    month_name, year = month_str.split("-")
    year = int(year)

    month_index = datetime.strptime(month_name, "%b").month

    working_days = 0
    unpaid_days = 0

    for day, entry in entries.items():
        d = int(day)

        if is_weekend(year, month_index, d):
            continue

        hours = entry.get("hours", "")
        remarks = str(entry.get("remarks", "")).lower()

        # Count unpaid
        if "unpaid" in remarks:
            unpaid_days += 1
            continue

        # Skip public holidays
        if "holiday" in remarks:
            continue

        # Count working days
        if hours not in ["", "--:--"]:
            working_days += 1

    return working_days, unpaid_days