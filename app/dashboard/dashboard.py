import streamlit as st
import pandas as pd
from charts import plot_leave_vs_holiday

st.set_page_config(layout="wide")
st.title("📊 Timesheet Dashboard")

uploaded_file = st.file_uploader("Upload Excel Report", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)

    valid_sheets = [s for s in xls.sheet_names if s != "Summary"]
    sheet = st.selectbox("📅 Select Month", valid_sheets)

    df = pd.read_excel(xls, sheet)
    df = df.fillna("")

    # -----------------------------
    # 🧠 Extract Month & Year
    # -----------------------------
    df["Month_Parsed"] = df["Month"].apply(lambda x: x.split("-")[0])
    df["Year_Parsed"] = df["Month"].apply(lambda x: x.split("-")[1])

    # -----------------------------
    # 🎯 FILTERS
    # -----------------------------
    st.sidebar.header("🔍 Filters")

    # Month filter
    months = sorted(df["Month_Parsed"].unique())
    selected_month = st.sidebar.selectbox("Month", months)

    # Year filter
    years = sorted(df["Year_Parsed"].unique())
    selected_year = st.sidebar.selectbox("Year", years)

    # Employee filter
    employees = sorted(df["Name"].unique())
    selected_employees = st.sidebar.multiselect("Employee", employees, default=employees)

    # -----------------------------
    # 🔎 SEARCH
    # -----------------------------
    search_text = st.sidebar.text_input("Search Employee")

    # -----------------------------
    # 🎯 APPLY FILTERS
    # -----------------------------
    filtered_df = df[
        (df["Month_Parsed"] == selected_month) &
        (df["Year_Parsed"] == selected_year) &
        (df["Name"].isin(selected_employees))
    ]

    if search_text:
        filtered_df = filtered_df[
            filtered_df["Name"].str.contains(search_text, case=False)
        ]

    # -----------------------------
    # 📋 DATA VIEW
    # -----------------------------
    st.subheader("📋 Filtered Data")
    st.dataframe(filtered_df)

    # -----------------------------
    # 📊 CHART
    # -----------------------------
    st.subheader("📊 Leave vs Holiday Analysis")
    fig = plot_leave_vs_holiday(filtered_df)
    st.pyplot(fig)

    # -----------------------------
    # 📌 INSIGHTS
    # -----------------------------
    st.subheader("📌 Insights")

    if "Total Hours" in filtered_df.columns and not filtered_df.empty:
        st.write("🏆 Top Performer:")
        st.write(filtered_df.loc[filtered_df["Total Hours"].idxmax()])

        st.write("⚠️ Least Hours:")
        st.write(filtered_df.loc[filtered_df["Total Hours"].idxmin()])