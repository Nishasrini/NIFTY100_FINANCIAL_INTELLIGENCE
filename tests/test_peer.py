import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from src.analytics.peer import calculate_peer_percentiles


def test_calculate_peer_percentiles():

    peer_groups = pd.DataFrame({
        "peer_group_name": ["IT", "IT"],
        "company_id": ["TCS", "INFY"],
        "is_benchmark": [True, False]
    })

    financial_ratios = pd.DataFrame({
        "company_id": ["TCS", "INFY"],
        "year": [2024, 2024],
        "net_profit_margin_pct": [20, 15],
        "operating_profit_margin_pct": [25, 20],
        "return_on_equity_pct": [30, 25],
        "return_on_capital_employed_pct": [28, 22],
        "debt_to_equity": [0.10, 0.20],
        "interest_coverage": [40, 35],
        "asset_turnover": [1.2, 1.1],
        "sales_3yr_cagr": [12, 10],
        "sales_5yr_cagr": [11, 9],
        "sales_10yr_cagr": [10, 8],
        "net_profit_3yr_cagr": [13, 11],
        "net_profit_5yr_cagr": [12, 10],
        "net_profit_10yr_cagr": [11, 9],
        "eps_3yr_cagr": [14, 12],
        "eps_5yr_cagr": [13, 11],
        "eps_10yr_cagr": [12, 10],
        "free_cash_flow_cr": [1000, 800],
        "capex_cr": [200, 250],
        "cfo_quality_score": [1.5, 1.2],
        "capex_intensity_pct": [5, 6],
        "fcf_conversion_pct": [80, 70],
    })

    result = calculate_peer_percentiles(
        peer_groups,
        financial_ratios
    )

    assert len(result) == 2

    assert "net_profit_margin_pct_percentile" in result.columns
    assert "return_on_equity_pct_percentile" in result.columns
    assert "fcf_conversion_pct_percentile" in result.columns

    assert result["company_id"].tolist() == ["TCS", "INFY"]