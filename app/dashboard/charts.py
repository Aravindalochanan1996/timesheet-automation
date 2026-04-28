import matplotlib.pyplot as plt

def convert_to_hours(time_str):
    try:
        if not time_str or time_str == "--:--":
            return 0
        h, m = time_str.split(":")
        return int(h) + int(m)/60
    except:
        return 0


def plot_leave_vs_holiday(df):
    unpaid = {}
    holiday = {}

    for _, row in df.iterrows():
        name = str(row["Name"]).strip()   # ✅ FIX

        if name not in unpaid:
            unpaid[name] = 0
            holiday[name] = 0

        for col in df.columns:
            if "Hours" in col and "Total" not in col:
                remarks_col = col.replace("Hours", "Remarks")

                hours = convert_to_hours(row[col])
                remarks = str(row.get(remarks_col, "")).lower()

                if "unpaid" in remarks:
                    unpaid[name] += hours

                elif any(k in remarks for k in ["holiday"]):   # ✅ FIX
                    holiday[name] += hours

    # Prepare data
    names = list(unpaid.keys())
    unpaid_vals = [unpaid[n] for n in names]
    holiday_vals = [holiday[n] for n in names]

    x = range(len(names))

    # ✅ FIX: use fig
    fig, ax = plt.subplots()

    ax.bar(x, unpaid_vals, label="Unpaid Leave")
    ax.bar(x, holiday_vals, bottom=unpaid_vals, label="Public Holiday")

    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=45)
    ax.set_ylabel("Hours")
    ax.set_title("Unpaid Leave vs Public Holiday (Per Employee)")

    # ✅ Legend at top-right
    ax.legend(loc="upper right")

    return fig