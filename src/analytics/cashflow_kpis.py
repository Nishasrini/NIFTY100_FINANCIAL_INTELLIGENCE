import sqlite3
import pandas as pd
import numpy as np
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

    df = load_data()

    result = calculate_cashflow_metrics(df)

    print("\nCash Flow KPI Sample\n")

    print(
        result[
            [
                "company_id",
                "year",
                "free_cash_flow_cr",
                "capex_cr",
                "cfo_quality_score",
                "cfo_quality_label",
                "capex_intensity_pct",
                "capex_category",
                "fcf_conversion_pct",
                "capital_allocation_pattern"
            ]
        ].head(20)
    )

    save_to_database(result)

    print("\nCash Flow KPIs saved successfully.")


if __name__ == "__main__":
    main()