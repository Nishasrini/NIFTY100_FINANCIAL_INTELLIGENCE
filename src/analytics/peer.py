import sqlite3
import pandas as pd
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


def main():

    peer_groups, financial_ratios = load_data()
    peer_percentiles = calculate_peer_percentiles(
        peer_groups,
        financial_ratios,
    )
    save_to_db(peer_percentiles)
    print("\nPeer Percentiles Sample\n")
    print(peer_percentiles.head())


if __name__ == "__main__":
    main()