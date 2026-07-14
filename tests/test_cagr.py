import os
import sys
import pandas as pd
import pytest

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, PROJECT_ROOT)

from src.analytics.cagr import calculate_cagr, generate_all_cagr


def test_calculate_cagr():

    result = calculate_cagr(
        start_value=100,
        end_value=150,
        years=3
    )

    # CAGR = ((150/100)^(1/3)-1)*100
    assert round(result, 2) == 14.47


def test_cagr_zero_start_value():

    result = calculate_cagr(
        start_value=0,
        end_value=100,
        years=3
    )

    assert result is None


def test_cagr_missing_years():

    result = calculate_cagr(
        start_value=100,
        end_value=150,
        years=0
    )

    assert result is None


def test_generate_all_cagr():

    df = pd.DataFrame({
        "company_id": ["ABC", "ABC", "ABC"],
        "year": [2020, 2021, 2023],
        "sales": [100, 120, 150],
        "net_profit": [10, 15, 20],
        "eps": [5, 6, 8]
    })
    revenue_cagr, pat_cagr, eps_cagr = generate_all_cagr(df)
    assert "company_id" in revenue_cagr.columns
    assert "sales_3yr_cagr" in revenue_cagr.columns
    assert "net_profit_3yr_cagr" in pat_cagr.columns
    assert "eps_3yr_cagr" in eps_cagr.columns

    