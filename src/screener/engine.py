import sqlite3
import pandas as pd
import yaml


DB_PATH = "data/nifty100.db"
CONFIG_PATH = "src/screener/screener_config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )
    market = pd.read_sql(
        """
        SELECT company_id, year, pe_ratio, pb_ratio, dividend_yield_pct
        FROM market_cap
        """,
        conn
    )
    balance = pd.read_sql(
        """
        SELECT company_id, year, borrowings
        FROM balancesheet
        """,
        conn
    )
    balance = balance[
        balance["year"].str.startswith("Mar")]
    sectors = pd.read_sql(
        """
        SELECT company_id, broad_sector
        FROM sectors
        """,
        conn
    )
    conn.close()
    ratios["merge_year"] = ratios["year"].str[-4:]
    balance["merge_year"] = balance["year"].str[-4:]
    market["merge_year"] = market["year"].astype(str)
    market = market.drop(columns=["year"])
    balance = balance.drop(columns=["year"])
    df = ratios.merge(
        market,
        on=["company_id", "merge_year"],
        how="left"
    )
    df = df.merge(
        balance,
        on=["company_id", "merge_year"],
        how="left"
    )
    df = df.merge(
        sectors,
        on="company_id",
        how="left"
    )
    df.drop(columns=["merge_year"], inplace=True)

    return df
def apply_filters(df, config, screener):
    if screener == "quality":
        quality = config["quality"]
        return df.query(
            "return_on_equity_pct >= @quality['min_roe'] "
            "and debt_to_equity <= @quality['max_debt_to_equity'] "
            "and free_cash_flow_cr >= @quality['min_free_cash_flow']"
        )
    elif screener == "growth":
        growth = config["growth"]

        return df.query(
            "net_profit_5yr_cagr >= @growth['min_pat_5yr_cagr']"
        )
    elif screener == "momentum":
        momentum = config["momentum"]
        return df.query(
            "sales_5yr_cagr >= @momentum['min_sales_5yr_cagr']"
        )
    elif screener == "value":
        value = config["value"]
        return df.query(
            "pe_ratio <= @value['max_pe'] and "
            "pb_ratio <= @value['max_pb']"
        )
    elif screener == "dividend":
        dividend = config["dividend"]
        return df.query(
            "dividend_yield_pct >= @dividend['min_dividend_yield']"
        )
    elif screener == "debt_free":
        debt = config["debt_free"]
        return df.query(
            "borrowings <= @debt['max_borrowings']"
        )
    else:
        print(f"{screener} screener cannot be executed because the required columns are not available.")
        return pd.DataFrame()
def normalize(series):
    series = series.fillna(series.median())
    if series.max() == series.min():
        return pd.Series(1.0, index=series.index)
    return (series - series.min()) / (series.max() - series.min())

def calculate_scores(df):
    df["roe_score"] = normalize(df["return_on_equity_pct"])
    df["roce_score"] = normalize(
        df["return_on_capital_employed_pct"]
    )
    df["npm_score"] = normalize(
        df["net_profit_margin_pct"]
    )
    df["profitability_score"] = (
        df["roe_score"] +
        df["roce_score"] +
        df["npm_score"]
    ) / 3
    df["sales_score"] = normalize(
        df["sales_5yr_cagr"]
    )
    df["profit_score"] = normalize(
        df["net_profit_5yr_cagr"]
    )
    df["eps_score"] = normalize(
        df["eps_5yr_cagr"]
    )
    df["growth_score"] = (
        df["sales_score"] +
        df["profit_score"] +
        df["eps_score"]
    ) / 3
    df["pe_score"] = 1 - normalize(
        df["pe_ratio"]
    )
    df["pb_score"] = 1 - normalize(
        df["pb_ratio"]
    )
    df["valuation_score"] = (
        df["pe_score"] +
        df["pb_score"]
    ) / 2
    df["composite_score"] = (
        0.50 * df["profitability_score"] +
        0.30 * df["growth_score"] +
        0.20 * df["valuation_score"]
    )
    return df

def rank_companies(df):
    df["overall_rank"] = (
        df["composite_score"]
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )
    df["sector_rank"] = (
        df.groupby("broad_sector")["composite_score"]
        .rank(
            ascending=False,
            method="dense"
        )
        .astype(int)
    )
    return df

def main():
    config = load_config()
    df = load_data()
    screeners = [
        "quality",
        "growth",
        "momentum",
        "value",
        "dividend",
        "debt_free"
    ]
    for screener in screeners:
        print("=" * 60)
        print(f"{screener.upper()} SCREENER")
        print("=" * 60)
        result = apply_filters(df, config, screener)
        print(result)
        print(f"Companies Found: {len(result)}\n")
    latest_year = (
    df.groupby("company_id")["year"]
      .max()
      .reset_index()
    )

    df = df.merge(
        latest_year,
        on=["company_id", "year"]
    )
    ranked_df = calculate_scores(df)
    conn = sqlite3.connect(DB_PATH)
    ranked_df = rank_companies(ranked_df)
    ranked_df = ranked_df.sort_values("overall_rank")
    print(ranked_df.head(20))
    ranked_df.to_excel(
        "src/screener/screener_output.xlsx",
        index=False
    )
    print("Output saved as screener_output.xlsx")


if __name__ == "__main__":
    main()