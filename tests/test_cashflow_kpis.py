import os
import sys
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from src.analytics.cashflow_kpis import calculate_cashflow_metrics


def test_calculate_cashflow_metrics():

    df = pd.DataFrame({
        "company_id": ["ABC"],
        "year": [2024],
        "operating_activity": [100],
        "investing_activity": [-20],
        "financing_activity": [-10],
        "sales": [500],
        "net_profit": [80],
        "operating_profit": [120]
    })

    result = calculate_cashflow_metrics(df)

    assert result.loc[0, "free_cash_flow_cr"] == 80
    assert result.loc[0, "capex_cr"] == 20
    assert round(result.loc[0, "cfo_quality_score"], 2) == 1.25
    assert result.loc[0, "capital_allocation_pattern"] == "Reinvesting"