import sqlite3
import pandas as pd
import yaml


DB_PATH = "data/nifty100.db"
CONFIG_PATH = "src/screener/screener_config.yaml"


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)

def load_financial_ratios():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT *
    FROM financial_ratios
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def apply_filters(df, config):
    quality = config["quality"]
    filtered_df = df.query(
        "return_on_equity_pct >= @quality['min_roe'] "
        "and debt_to_equity <= @quality['max_debt_to_equity'] "
        "and net_profit_margin_pct >= @quality['min_net_profit_margin'] "
        "and operating_profit_margin_pct >= @quality['min_operating_profit_margin'] "
        "and sales_5yr_cagr >= @quality['min_sales_5yr_cagr']"
    )
    return filtered_df


def main():
    config = load_config()
    df = load_financial_ratios()
    result = apply_filters(df, config)
    print(result)

if __name__ == "__main__":
    main()