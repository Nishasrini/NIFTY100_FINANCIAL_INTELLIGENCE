import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("data/nifty100.db")

# Page title
st.title("📄 Annual Reports")

st.markdown(
    """
    Browse annual reports for NIFTY100 companies.
    """
)

# Load companies
companies = pd.read_sql(
    """
    SELECT id
    FROM companies
    ORDER BY id
    """,
    conn,
)

# Company selection
selected_company = st.selectbox(
    "Select Company",
    companies["id"]
)

st.subheader(f"{selected_company} Annual Reports")

st.info(
    """
    Annual report documents are not available in the current database.

    This page is reserved for integrating company annual reports in future.
    """
)

st.markdown("### Planned Features")

st.markdown("""
- 📄 View annual reports
- ⬇ Download PDF reports
- 📅 Select financial year
- 🔍 Search within reports
- 📊 Compare annual reports across years
""")

conn.close()