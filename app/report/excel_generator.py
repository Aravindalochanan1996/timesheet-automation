from email import header
from datetime import datetime
from openpyxl import Workbook
from datetime import datetime
from app.report.formatter import format_sheet, highlight_remarks
from app.report.summary_generator import generate_summary_sheet, calculate_total_hours
from app.report.working_days_calculator import calculate_metrics
# from app.report.pivot_chart import add_unpaid_leave_chart
# from app.report.summary_chart import add_summary_pivot_chart
import calendar

    
def generate_excel(records, output_file):
    wb = Workbook()

    grouped = {}

    for r in records:
        grouped.setdefault(r["month"], []).append(r)
    

    sorted_months = sorted(
        grouped.keys(),
        key=lambda m: datetime.strptime(m, "%b-%Y"),
        reverse=True   # latest first
    )

    for month in sorted_months:
        recs = grouped[month]
        month_name, year = month.split("-")

        ws = wb.create_sheet(title=f"{month_name} {year}")

        # days = calendar.monthrange(
        #     int(year),
        #     list(calendar.month_name).index(month_name)
        # )[1]        

        month_index = datetime.strptime(month_name, "%b").month
        days = calendar.monthrange(int(year), month_index)[1]

        header = ["Name", "Emp ID", "Month"]

        for d in range(1, days + 1):
            header += [f"Day {d} Hours", f"Day {d} Remarks"]
        header.append("Total Hours")
        header.append("Total Working Days")
        header.append("Total Unpaid Leaves")
        ws.append(header)

        for r in recs:
            row = [r["name"], r["emp_id"], r["month"]]

            for d in range(1, days + 1):
                key = str(d).zfill(2)
                entry = r["entries"].get(key, {})

                row.append(entry.get("hours", ""))
                row.append(entry.get("remarks", ""))
            total_hours = calculate_total_hours(r["entries"])

            working_days, unpaid_days = calculate_metrics(r["entries"], r["month"])

            row.append(total_hours)
            row.append(working_days)
            row.append(unpaid_days)
            ws.append(row)

    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]
                   
    # ✅ Add Summary Sheet
    generate_summary_sheet(wb, records)
    
    wb._sheets.sort(
        key=lambda ws: (
            0 if ws.title == "Summary" else 1,
            -datetime.strptime(ws.title, "%b %Y").timestamp() if ws.title != "Summary" else 0
        )
    )


    summary_ws = wb["Summary"]
    # add_summary_pivot_chart(summary_ws, records)

    # Apply formatting safely
    for sheet in wb.worksheets:
        if sheet.title != "Summary":
            highlight_remarks(sheet)
        format_sheet(sheet)

    wb.save(output_file)