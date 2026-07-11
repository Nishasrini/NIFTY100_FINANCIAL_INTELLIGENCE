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

if __name__ == "__main__":
    main()