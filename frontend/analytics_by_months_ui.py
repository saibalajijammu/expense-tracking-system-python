import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_months_tab():
    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    
    # Handle both single-dict and list responses
    if isinstance(monthly_summary, dict):
        monthly_summary = [monthly_summary]

    # Handle empty response
    if not monthly_summary:
        st.warning("No data found.")
        return

    df = pd.DataFrame(monthly_summary)

    # Adjust column names based on your backend keys
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)

    if "Month Number" not in df.columns:
        st.error(f"Unexpected columns: {list(df.columns)}")
        return

    df_sorted = df.sort_values(by="Month Number", ascending=False)
    df_sorted.set_index("Month Number", inplace=True)

    st.title("Expense Breakdown By Months")

    st.bar_chart(data=df_sorted.set_index("Month Name")['Total'], use_container_width=True)

    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

    st.table(df_sorted.sort_index())
