import pandas as pd
import sqlite3
def calculate_npm(net_profit, sales):
    if sales == 0 or pd.isna(sales):
        return None
    return round((net_profit / sales) * 100, 2)
def calculate_opm(operating_profit, sales):
    if sales == 0 or pd.isna(sales):
        return None
    return round((operating_profit / sales) * 100, 2)
def calculate_roe(net_profit, equity_capital, reserves):
    equity = equity_capital + reserves
    if equity <= 0 or pd.isna(equity):
        return None
    return round((net_profit / equity) * 100, 2)
def calculate_roce(operating_profit,depreciation,equity_capital,reserves,borrowings,):
    capital_employed = (
        equity_capital + reserves + borrowings
    )
    if capital_employed <= 0 or pd.isna(capital_employed):
        return None
    ebit = operating_profit - depreciation
    return round(
        (ebit / capital_employed) * 100,
        2
    )
def build_profitability_ratios():
    conn = sqlite3.connect("data/nifty100.db")
    pl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )
    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )
    df = pd.merge(
        pl,
        bs,
        on=["company_id", "year"],
        how="inner"
    )
    df["net_profit_margin_pct"] = df.apply(
        lambda x: calculate_npm(
            x["net_profit"],
            x["sales"]
        ),
        axis=1
    )
    df["operating_profit_margin_pct"] = df.apply(
        lambda x: calculate_opm(
            x["operating_profit"],
            x["sales"]
        ),
        axis=1
    )
    df["return_on_equity_pct"] = df.apply(
        lambda x: calculate_roe(
            x["net_profit"],
            x["equity_capital"],
            x["reserves"]
        ),
        axis=1
    )
    df["return_on_capital_employed_pct"] = df.apply(
        lambda x: calculate_roce(
            x["operating_profit"],
            x["depreciation"],
            x["equity_capital"],
            x["reserves"],
            x["borrowings"]
        ),
        axis=1
    )
    # OPM Cross Validation
    df["opm_difference"] = (
        df["operating_profit_margin_pct"]
        - df["opm_percentage"]
    ).abs()

    print(
        "\nOPM Validation Summary"
    )
    print(
        df[
            [
                "company_id",
                "year",
                "operating_profit_margin_pct",
                "opm_percentage",
                "opm_difference",
            ]
        ].head()
    )
    print("\nProfitability Ratios Sample")
    print(
        df[
            [
                "company_id",
                "year",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
            ]
        ].head()
    )
    conn.close()
    return df
if __name__ == "__main__":
    ratios_df = build_profitability_ratios()