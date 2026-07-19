import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
conn = sqlite3.connect("data/nifty100.db")
st.title("📊 Sector Analysis")
peer_groups = pd.read_sql(
    """
    SELECT DISTINCT peer_group_name
    FROM peer_groups
    ORDER BY peer_group_name
    """,
    conn,
)
selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups["peer_group_name"],
)
query = """
SELECT
    pg.company_id,
    fr.year,
    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct
FROM peer_groups pg
JOIN financial_ratios fr
ON pg.company_id = fr.company_id
WHERE pg.peer_group_name = ?
"""

df = pd.read_sql(
    query,
    conn,
    params=(selected_group,),
)
st.subheader("Companies")

st.dataframe(df)
avg_roe = (
    df.groupby("company_id")["return_on_equity_pct"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(avg_roe.index, avg_roe.values)

ax.set_ylabel("Average ROE (%)")
ax.set_xlabel("Company")
ax.set_title(f"{selected_group} - Average ROE")

plt.xticks(rotation=90)

st.pyplot(fig)
conn.close()