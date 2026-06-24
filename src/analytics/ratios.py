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
def calculate_debt_to_equity(
    borrowings,
    equity_capital,
    reserves,
):
    equity = equity_capital + reserves

    if equity <= 0 or pd.isna(equity):
        return None

    return round(
        borrowings / equity,
        2,
    )
def calculate_interest_coverage(
    operating_profit,
    other_income,
    interest,
):
    if pd.isna(interest):
        return None

    if interest == 0:
        return 999

    return round(
        (
            operating_profit
            + other_income
        )
        / interest,
        2,
    )
def calculate_asset_turnover(
    sales,
    total_assets,
):
    if total_assets == 0 or pd.isna(total_assets):
        return None

    return round(
        sales / total_assets,
        2,
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
    df["debt_to_equity"] = df.apply(
        lambda x: calculate_debt_to_equity(
            x["borrowings"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    df["interest_coverage"] = df.apply(
        lambda x: calculate_interest_coverage(
            x["operating_profit"],
            x["other_income"],
            x["interest"],
        ),
        axis=1,
    )
    df["asset_turnover"] = df.apply(
        lambda x: calculate_asset_turnover(
            x["sales"],
            x["total_assets"],
        ),
        axis=1,
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
                "debt_to_equity",
                "interest_coverage",
                "asset_turnover",
            ]
        ].head()
    )

    conn.close()
    return df
if __name__ == "__main__":
    ratios_df = build_profitability_ratios()