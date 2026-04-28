import calendar

def get_month_index(month_name):
    # Convert short month → full month
    month_map = {
        "Jan": "January", "Feb": "February", "Mar": "March",
        "Apr": "April", "May": "May", "Jun": "June",
        "Jul": "July", "Aug": "August", "Sep": "September",
        "Oct": "October", "Nov": "November", "Dec": "December"
    }

    full_month = month_map.get(month_name)

    if not full_month:
        raise ValueError(f"Invalid month: {month_name}")

    return list(calendar.month_name).index(full_month)


def get_days_in_month(month_name, year):
    month_index = get_month_index(month_name)
    return calendar.monthrange(int(year), month_index)[1]