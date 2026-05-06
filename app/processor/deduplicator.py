from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%d-%b-%Y")
    except:
        return datetime.min
    
def remove_duplicates(records):
    unique = {}

    for r in records:
        key = f"{r['emp_id']}_{r['month']}"

        if key not in unique:
            unique[key] = r
        else:
            existing = unique[key]

            d1 = parse_date(r.get("report_generated", ""))
            d2 = parse_date(existing.get("report_generated", ""))

            if d1 > d2:
                unique[key] = r

            elif d1 == d2:
                if r.get("file_timestamp", 0) > existing.get("file_timestamp", 0):
                    unique[key] = r
            
    return list(unique.values())