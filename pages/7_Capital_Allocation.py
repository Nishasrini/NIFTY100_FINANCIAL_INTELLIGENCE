import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
conn = sqlite3.connect("data/nifty100.db")
st.title("💰 Capital Allocation Analysis")
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
    companies["id"],
)
query = """
SELECT
    year,
    free_cash_flow_cr,
    capex_cr,
    cfo_quality_score,
    capex_intensity_pct,
    fcf_conversion_pct,
    capital_allocation_pattern
FROM financial_ratios
WHERE company_id = ?
ORDER BY year
"""

df = pd.read_sql(
    query,
    conn,
    params=(selected_company,),
)
st.subheader("Capital Allocation Metrics")

st.dataframe(df)
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(
    df["year"],
    df["free_cash_flow_cr"],
    marker="o",
    label="Free Cash Flow",
)

ax.set_xlabel("Year")
ax.set_ylabel("₹ Crores")
ax.set_title(f"{selected_company} Free Cash Flow Trend")

ax.legend()

st.pyplot(fig)
if not df.empty:
    st.metric(
        "Latest Capital Allocation Pattern",
        df.iloc[-1]["capital_allocation_pattern"],
    )
conn.close()