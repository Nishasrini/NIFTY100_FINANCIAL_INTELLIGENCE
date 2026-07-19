import streamlit as st
import sqlite3
import pandas as pd
conn = sqlite3.connect("data/nifty100.db")
st.title("🏢 Company Profile")
companies = pd.read_sql(
    """
    SELECT id
    FROM companies
    ORDER BY id
    """,
    conn
)
selected_company = st.selectbox(
    "Select Company",
    companies["id"]
)
ratios = pd.read_sql(
    f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id = '{selected_company}'
    ORDER BY year
    """,
    conn
)
st.subheader("Financial Ratios")

st.dataframe(ratios)
st.dataframe(
    pd.read_sql(
        "SELECT DISTINCT year FROM financial_ratios ORDER BY year;",
        conn
    )
)
conn.close()