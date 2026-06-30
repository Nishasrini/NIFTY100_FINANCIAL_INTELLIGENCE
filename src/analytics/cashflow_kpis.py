import sqlite3
import pandas as pd
import numpy as np
from ratios import build_profitability_ratios
from cagr import generate_all_cagr
DB_PATH = "data/nifty100.db"
def capital_allocation_pattern(cfo, cfi, cff):
    if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff):
        return "Unknown"
    sign = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )
    patterns = {
        ("+", "-", "-"): "Reinvesting",
        ("+", "-", "+"): "Growth Funded",
        ("+", "+", "-"): "Asset Sale Returns",
        ("+", "+", "+"): "Cash Accumulation",
        ("-", "-", "+"): "External Funding",
        ("-", "+", "+"): "Distress",
        ("-", "-", "-"): "Cash Burn",
        ("-", "+", "-"): "Declining Business"
    }
    return patterns.get(sign, "Other")
def calculate_cashflow_metrics(df):
    # Free Cash Flow
    df["free_cash_flow_cr"] = (
        df["operating_activity"] +
        df["investing_activity"]
    )

    # CapEx Proxy
    df["capex_cr"] = df["investing_activity"].abs()

    # CFO Quality Ratio
    df["cfo_quality_score"] = np.where(
        df["net_profit"] == 0,
        np.nan,
        df["operating_activity"] / df["net_profit"]
    )

    # CFO Quality Label
    conditions = [
        df["cfo_quality_score"] > 1,
        df["cfo_quality_score"] >= 0.5,
        df["cfo_quality_score"] < 0.5
    ]

    labels = [
        "High Quality Earnings",
        "Average",
        "Accrual Risk"
    ]

    df["cfo_quality_label"] = np.select(
        conditions,
        labels,
        default="Unknown"
    )

    # CapEx Intensity
    df["capex_intensity_pct"] = np.where(
        df["sales"] == 0,
        np.nan,
        (df["capex_cr"] / df["sales"]) * 100
    )

    intensity = [
        df["capex_intensity_pct"] < 3,
        (df["capex_intensity_pct"] >= 3) &
        (df["capex_intensity_pct"] <= 8),
        df["capex_intensity_pct"] > 8
    ]

    intensity_labels = [
        "Asset Light",
        "Moderate",
        "Capital Intensive"
    ]

    df["capex_category"] = np.select(
        intensity,
        intensity_labels,
        default="Unknown"
    )

    # FCF Conversion
    df["fcf_conversion_pct"] = np.where(
        df["operating_profit"] == 0,
        np.nan,
        (df["free_cash_flow_cr"] /
         df["operating_profit"]) * 100
    )

    # Capital Allocation Pattern
    df["capital_allocation_pattern"] = df.apply(
        lambda row: capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"]
        ),
        axis=1
    )

    return df


def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT
        cf.company_id,
        cf.year,
        cf.operating_activity,
        cf.investing_activity,
        cf.financing_activity,
        cf.net_cash_flow,
        pl.sales,
        pl.net_profit,
        pl.operating_profit

    FROM cashflow cf

    JOIN profitandloss pl

    ON cf.company_id = pl.company_id
    AND cf.year = pl.year

    ORDER BY
        cf.company_id,
        cf.year;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def save_to_database(df):
    conn = sqlite3.connect(DB_PATH)
    try:

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            conn
        )
        ratios = ratios.merge(
            df[
                [
                    "company_id",
                    "year",
                    "free_cash_flow_cr",
                    "capex_cr",
                    "cfo_quality_score",
                    "capex_intensity_pct",
                    "fcf_conversion_pct"
                ]
            ],
            on=["company_id", "year"],
            how="left"
        )
        ratios.to_sql(
            "financial_ratios",
            conn,
            if_exists="replace",
            index=False
        )
    except Exception:
        df[
            [
                "company_id",
                "year",
                "free_cash_flow_cr",
                "capex_cr",
                "cfo_quality_score",
                "capex_intensity_pct",
                "fcf_conversion_pct"
            ]
        ].to_sql(
            "financial_ratios",
            conn,
            if_exists="replace",
            index=False
        )
    conn.close()

def main():

    # Load cashflow data
    df = load_data()

    # Calculate cashflow KPIs
    result = calculate_cashflow_metrics(df)

    ###################################################
    # STEP 1 - Profitability Ratios
    ###################################################

    ratio_df = build_profitability_ratios()

    ratio_df = ratio_df[
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
    ]

    ###################################################
    # STEP 2 - CAGR
    ###################################################

    conn = sqlite3.connect(DB_PATH)

    pl = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            sales,
            net_profit,
            eps
        FROM profitandloss
        ORDER BY company_id, year
        """,
        conn
    )

    revenue, pat, eps = generate_all_cagr(pl)

    revenue = revenue.rename(columns={
    "sales_3yr_cagr": "sales_3yr_cagr",
    "sales_5yr_cagr": "sales_5yr_cagr",
    "sales_10yr_cagr": "sales_10yr_cagr"
    })

    pat = pat.drop(columns=[
    "net_profit_3yr_turnaround",
    "net_profit_5yr_turnaround",
    "net_profit_10yr_turnaround"
    ], errors="ignore")

    eps = eps.drop(columns=[
    "eps_3yr_turnaround",
    "eps_5yr_turnaround",
    "eps_10yr_turnaround"
    ], errors="ignore")

    cagr = revenue.merge(
    pat,
    on=["company_id", "year"],
    how="left"
    )

    cagr = cagr.merge(
    eps,
    on=["company_id", "year"],
    how="left"
    )
    cagr = cagr[
    [
        "company_id",
        "year",
        "sales_3yr_cagr",
        "sales_5yr_cagr",
        "sales_10yr_cagr",
        "net_profit_3yr_cagr",
        "net_profit_5yr_cagr",
        "net_profit_10yr_cagr",
        "eps_3yr_cagr",
        "eps_5yr_cagr",
        "eps_10yr_cagr"
    ]
    ]


    ###################################################
    # STEP 3 - Cash Flow dataframe
    ###################################################

    cash = result[
        [
            "company_id",
            "year",
            "free_cash_flow_cr",
            "capex_cr",
            "cfo_quality_score",
            "capex_intensity_pct",
            "fcf_conversion_pct",
            "capital_allocation_pattern"
        ]
    ]
    financial_ratios = ratio_df.merge(
    cagr,
    on=["company_id", "year"],
    how="left"
    )

    financial_ratios = financial_ratios.merge(
    cash,
    on=["company_id", "year"],
    how="left"
    )
    financial_ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
    )

    print("\nFinancial Ratios Table Created Successfully\n")
    print(financial_ratios.head())

    print("\nTotal Rows :", len(financial_ratios))
    print("Total Companies :", financial_ratios["company_id"].nunique())
    conn.close()


if __name__ == "__main__":
    main()