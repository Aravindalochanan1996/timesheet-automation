import os
from app.parser.pdf_reader import read_pdf
from app.parser.metadata_extractor import extract_metadata
from app.parser.timesheet_parser import extract_entries
from app.processor.deduplicator import remove_duplicates

def process_pdfs(input_dir):
    records = []

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            path = os.path.join(input_dir, file)

            text = read_pdf(path)
            meta = extract_metadata(text)

            if not meta["name"]:
                continue

            meta["entries"] = extract_entries(text)
            records.append(meta)

    return remove_duplicates(records)