import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

total_companies = pd.read_sql(
    "SELECT COUNT(*) AS total FROM companies",
    conn
).iloc[0]["total"]

latest_year = pd.read_sql(
    "SELECT MAX(year) AS latest_year FROM financial_ratios",
    conn
).iloc[0]["latest_year"]

total_ratio_records = pd.read_sql(
    "SELECT COUNT(*) AS total FROM financial_ratios",
    conn
).iloc[0]["total"]

avg_roe = pd.read_sql(
    """
    SELECT ROUND(AVG(return_on_equity_pct),2) AS avg_roe
    FROM financial_ratios
    """,
    conn
).iloc[0]["avg_roe"]

st.title("📊 Nifty100 Financial Intelligence Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Companies", total_companies)
col2.metric("Latest Year", latest_year)
col3.metric("Financial Ratio Records", total_ratio_records)
col4.metric("Average ROE (%)", avg_roe)

conn.close()