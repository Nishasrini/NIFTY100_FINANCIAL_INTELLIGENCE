import sqlite3
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
DB_PATH = "data/nifty100.db"
METRICS = [
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "sales_3yr_cagr",
    "sales_5yr_cagr",
    "sales_10yr_cagr",
    "net_profit_3yr_cagr",
    "net_profit_5yr_cagr",
    "net_profit_10yr_cagr",
    "eps_3yr_cagr",
    "eps_5yr_cagr",
    "eps_10yr_cagr",
    "free_cash_flow_cr",
    "capex_cr",
    "cfo_quality_score",
    "capex_intensity_pct",
    "fcf_conversion_pct",
]
RADAR_METRICS = [
    "return_on_equity_pct_percentile",
    "return_on_capital_employed_pct_percentile",
    "net_profit_margin_pct_percentile",
    "debt_to_equity_percentile",
    "free_cash_flow_cr_percentile",
    "net_profit_5yr_cagr_percentile",
    "sales_5yr_cagr_percentile",
    "eps_5yr_cagr_percentile",
]
def create_output_folder():
    os.makedirs("reports/radar_charts", exist_ok=True)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    peer_groups = pd.read_sql(
        """
        SELECT
            peer_group_name,
            company_id,
            is_benchmark
        FROM peer_groups
        """,
        conn,
    )
    financial_ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )
    conn.close()
    return peer_groups, financial_ratios


def calculate_peer_percentiles(peer_groups, financial_ratios):
    df = peer_groups.merge(
        financial_ratios,
        on="company_id",
        how="inner",
    )
    result = df[
        [
            "company_id",
            "peer_group_name",
            "year",
            "is_benchmark",
        ]
    ].copy()
    for metric in METRICS:
        result[f"{metric}_percentile"] = (
            df.groupby(["peer_group_name", "year"])[metric]
            .rank(method="min", pct=True)
        )
    return result


def save_to_db(peer_percentiles):
    conn = sqlite3.connect(DB_PATH)
    peer_percentiles.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False,
    )
    conn.close()

def create_radar_chart(row):
    labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "Sales CAGR",
        "EPS CAGR",
    ]
    values = row[RADAR_METRICS].fillna(0).tolist()
    values += values[:1]
    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False,
    ).tolist()

    angles += angles[:1]
    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw=dict(polar=True),
    )
    ax.plot(
        angles,
        values,
        linewidth=2,
    )
    ax.fill(
        angles,
        values,
        alpha=0.25,
    )
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    title = (
        f"{row['company_id']} "
        f"({row['peer_group_name']}) "
        f"{row['year']}"
    )
    plt.title(title)
    filename = (
        f"reports/radar_charts/"
        f"{row['company_id']}_{row['year']}.png"
    )
    plt.savefig(
        filename,
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()
def generate_radar_charts(peer_percentiles):

    create_output_folder()

    latest = (
        peer_percentiles
        .sort_values("year")
        .groupby("company_id")
        .tail(1)
    )

    for _, row in latest.iterrows():
        create_radar_chart(row)

    print(
        f"\nGenerated {len(latest)} radar charts."
    )
def main():

    peer_groups, financial_ratios = load_data()
    peer_percentiles = calculate_peer_percentiles(
        peer_groups,
        financial_ratios,
    )
    save_to_db(peer_percentiles)
    print("\nPeer Percentiles Sample\n")
    print(peer_percentiles.head())
    generate_radar_charts(peer_percentiles)


if __name__ == "__main__":
    main()