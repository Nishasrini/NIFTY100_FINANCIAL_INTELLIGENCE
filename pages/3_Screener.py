import streamlit as st
import sqlite3
import pandas as pd
conn = sqlite3.connect("data/nifty100.db")
st.title("🔍 Financial Screener")
query = """
SELECT *
FROM financial_ratios fr
WHERE CAST(SUBSTR(fr.year, -4) AS INTEGER) = (
    SELECT MAX(CAST(SUBSTR(fr2.year, -4) AS INTEGER))
    FROM financial_ratios fr2
    WHERE fr2.company_id = fr.company_id
)
"""

df = pd.read_sql(query, conn)
min_roe = st.slider(
    "Minimum ROE (%)",
    0,
    50,
    15
)

max_debt = st.slider(
    "Maximum Debt to Equity",
    0.0,
    5.0,
    1.0
)

min_roce = st.slider(
    "Minimum ROCE (%)",
    0,
    60,
    15
)
filtered = df[
    (df["return_on_equity_pct"] >= min_roe) &
    (df["debt_to_equity"] <= max_debt) &
    (df["return_on_capital_employed_pct"] >= min_roce)
]
st.subheader("Filtered Companies")

st.dataframe(filtered)
