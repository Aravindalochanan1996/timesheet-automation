def remove_duplicates(records):
    unique = {}
    for r in records:
        key = f"{r['emp_id']}_{r['month']}"
        unique[key] = r
    return list(unique.values())