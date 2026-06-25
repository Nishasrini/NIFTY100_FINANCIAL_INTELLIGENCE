import pandas as pd
import sqlite3


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR percentage.
    """

    if pd.isna(start_value) or pd.isna(end_value):
        return None

    if start_value <= 0 or end_value <= 0:
        return None

    try:
        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(cagr, 2)
    except Exception:
        return None


def is_turnaround(start_value, end_value):
    """
    Turnaround: start value negative, end value positive.
    """
    return start_value < 0 and end_value > 0


def calculate_metric_cagr(df, metric):

    df = df.sort_values("year").reset_index(drop=True)

    results = []

    for i in range(len(df)):

        row = {
            "company_id": df.loc[i, "company_id"],
            "year": df.loc[i, "year"]
        }

        current_value = df.loc[i, metric]

        for period in [3, 5, 10]:

            if i >= period:

                start_value = df.loc[i - period, metric]

                row[f"{metric}_{period}yr_cagr"] = calculate_cagr(
                    start_value,
                    current_value,
                    period
                )

                row[f"{metric}_{period}yr_turnaround"] = is_turnaround(
                    start_value,
                    current_value
                )

            else:

                row[f"{metric}_{period}yr_cagr"] = None
                row[f"{metric}_{period}yr_turnaround"] = False

        results.append(row)

    return pd.DataFrame(results)


def generate_all_cagr(df):

    revenue_results = []
    pat_results = []
    eps_results = []

    for _, company_df in df.groupby("company_id"):

        revenue_results.append(
            calculate_metric_cagr(company_df, "sales")
        )

        pat_results.append(
            calculate_metric_cagr(company_df, "net_profit")
        )

        eps_results.append(
            calculate_metric_cagr(company_df, "eps")
        )

    revenue_cagr = pd.concat(revenue_results, ignore_index=True)
    pat_cagr = pd.concat(pat_results, ignore_index=True)
    eps_cagr = pd.concat(eps_results, ignore_index=True)

    return revenue_cagr, pat_cagr, eps_cagr


if __name__ == "__main__":

    conn = sqlite3.connect("data/nifty100.db")

    df = pd.read_sql("""
    SELECT
        company_id,
        year,
        sales,
        net_profit,
        eps
    FROM profitandloss
    ORDER BY company_id, year
    """, conn)

    revenue_cagr, pat_cagr, eps_cagr = generate_all_cagr(df)

    print("\nRevenue CAGR")
    print(revenue_cagr.head())

    print("\nPAT CAGR")
    print(pat_cagr.head())

    print("\nEPS CAGR")
    print(eps_cagr.head())

    conn.close()