from openpyxl.styles import PatternFill
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Light yellow highlight
REMARK_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

def highlight_remarks(ws):
    """
    Highlight only Remarks columns where value is present
    """

    header = [cell.value for cell in ws[1]]

    # Find all "Remarks" column indexes
    remark_cols = [i + 1 for i, col in enumerate(header) if "Remarks" in col]

    for row in ws.iter_rows(min_row=2):
        for col_idx in remark_cols:
            cell = row[col_idx - 1]

            if cell.value and str(cell.value).strip():
                cell.fill = REMARK_FILL


HEADER_FONT = Font(bold=True)
CENTER_ALIGN = Alignment(horizontal="center", vertical="center")
LEFT_ALIGN = Alignment(horizontal="left", vertical="center", wrap_text=True)

BORDER = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

HEADER_FILL = PatternFill(start_color="D9E1F2", fill_type="solid")
TOTAL_FILL = PatternFill(start_color="C6E0B4", fill_type="solid")


def format_sheet(ws):
    # Freeze top row
    ws.freeze_panes = "A2"

    # Identify columns
    header = [cell.value for cell in ws[1]]
    total_col_index = len(header)

    for col_idx, col_name in enumerate(header, start=1):
        column_letter = ws.cell(row=1, column=col_idx).column_letter

        # Set column width
        if "Remarks" in col_name:
            ws.column_dimensions[column_letter].width = 25
        elif "Hours" in col_name:
            ws.column_dimensions[column_letter].width = 12
        else:
            ws.column_dimensions[column_letter].width = 18

    # Apply styles
    for row in ws.iter_rows():
        for cell in row:
            # Header styling
            if cell.row == 1:
                cell.font = HEADER_FONT
                cell.fill = HEADER_FILL
                cell.alignment = CENTER_ALIGN
            else:
                if "Remarks" in str(ws.cell(row=1, column=cell.column).value):
                    cell.alignment = LEFT_ALIGN
                else:
                    cell.alignment = CENTER_ALIGN

            cell.border = BORDER

    # Highlight Total Hours column
    for row in ws.iter_rows(min_row=2):
        total_cell = row[total_col_index - 1]
        total_cell.fill = TOTAL_FILL