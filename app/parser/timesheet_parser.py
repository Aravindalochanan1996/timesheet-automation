import re

def extract_entries(text):
    entries = {}

    lines = text.split("\n")

    for line in lines:
        # Match full row
        match = re.match(
            r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+"
            r"(\d{2})-[A-Za-z]{3}-\d{4}\s+"
            r"(--:--|\d{1,2}:\d{2})\s*(.*)",
            line
        )

        if match:
            day = match.group(2)  # 01, 02, etc
            hours = match.group(3)
            remarks = match.group(4).strip()

            entries[day] = {
                "hours": hours,
                "remarks": remarks
            }

    return entries