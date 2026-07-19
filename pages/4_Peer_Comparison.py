import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("data/nifty100.db")

st.title("📊 Peer Comparison")

# Load company list
companies = pd.read_sql(
    """
    SELECT id
    FROM companies
    ORDER BY id
    """,
    conn,
)

selected_company = st.selectbox(
    "Select Company",
    companies["id"]
)

# Load peer comparison data
query = """
SELECT *
FROM peer_percentiles
WHERE company_id = ?
"""

peer_df = pd.read_sql(
    query,
    conn,
    params=(selected_company,)
)

if peer_df.empty:
    st.warning(f"No peer comparison data available for {selected_company}.")
else:
    st.dataframe(peer_df)



conn.close()