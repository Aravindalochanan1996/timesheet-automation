from datetime import datetime

def extract_leave_metrics(entries, month_str):
    month_name, year = month_str.split("-")
    year = int(year)

    month_index = datetime.strptime(month_name, "%b").month

    public_holidays = []
    unpaid_dates = []

    for day, entry in entries.items():
        d = int(day)

        remarks = str(entry.get("remarks", "")).lower()

        if "holiday" in remarks:
            public_holidays.append(str(d).zfill(2))

        elif "unpaid" in remarks:
            unpaid_dates.append(str(d).zfill(2))

    return (
        ", ".join(public_holidays),
        len(unpaid_dates),
        ", ".join(unpaid_dates)
    )