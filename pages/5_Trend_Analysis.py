import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
conn = sqlite3.connect("data/nifty100.db")
st.title("📈 Trend Analysis")
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
query = """
SELECT
    year,
    return_on_equity_pct,
    return_on_capital_employed_pct,
    net_profit_margin_pct
FROM financial_ratios
WHERE company_id = ?
"""

df = pd.read_sql(
    query,
    conn,
    params=(selected_company,)
)
st.dataframe(df)
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(
    df["year"],
    df["return_on_equity_pct"],
    marker="o",
    label="ROE",
)

ax.plot(
    df["year"],
    df["return_on_capital_employed_pct"],
    marker="o",
    label="ROCE",
)

ax.set_xlabel("Year")
ax.set_ylabel("Percentage")
ax.set_title(f"{selected_company} Financial Trend")

ax.legend()

st.pyplot(fig)
conn.close()