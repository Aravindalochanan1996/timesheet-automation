from app.processor.timesheet_service import process_pdfs
from app.report.excel_generator import generate_excel
from app.config.settings import INPUT_DIR, OUTPUT_FILE

def run():
    records = process_pdfs(INPUT_DIR)

    if not records:
        print("No valid data found!")
        return

    # print(records[0])
    generate_excel(records, OUTPUT_FILE)

    print("✅ Timesheet Excel generated successfully")

if __name__ == "__main__":
    run()