import os
import re
from datetime import datetime
from app.parser.pdf_reader import read_pdf
from app.parser.metadata_extractor import extract_metadata
from app.parser.timesheet_parser import extract_entries
from app.processor.deduplicator import remove_duplicates

def extract_report_generated(text):
    match = re.search(
        r"Report\s*Generated.*?(\d{1,2}[-/][A-Za-z]{3}[-/]\d{4})",
        text,
        re.IGNORECASE | re.DOTALL
    )
    return match.group(1) if match else ""


def get_latest_report_date(records):
    dates = []

    for r in records:
        date_str = r.get("report_generated")

        if date_str:
            try:
                # ✅ Convert string → datetime
                dt = datetime.strptime(date_str.strip(), "%d-%b-%Y")
                dates.append(dt)
            except Exception as e:
                print("Date parse error:", date_str, e)

    if not dates:
        return ""

    # ✅ Get max date correctly
    latest_date = max(dates)
    # print("Parsed Dates:", dates)
    # print("Latest Date:", latest_date)
    return latest_date.strftime("%d-%b-%Y")

def process_pdfs(input_dir):
    records = []

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            path = os.path.join(input_dir, file)

            text = read_pdf(path)
            meta = extract_metadata(text)

            if not meta["name"]:
                continue

            report_generated = extract_report_generated(text)
            file_timestamp = os.path.getmtime(path)

            meta["entries"] = extract_entries(text)
            meta["report_generated"] = report_generated
            meta["file_timestamp"] = file_timestamp

            records.append(meta)

    # ✅ This alone will handle your logic
    records = remove_duplicates(records)

    return records
    