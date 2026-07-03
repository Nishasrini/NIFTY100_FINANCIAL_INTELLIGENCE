import pytest
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

sys.path.insert(0, PROJECT_ROOT)
from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_asset_turnover,
)


# -------------------------
# Net Profit Margin
# -------------------------

def test_calculate_npm():
    assert calculate_npm(20, 100) == 20.00


def test_calculate_npm_zero_sales():
    assert calculate_npm(20, 0) is None


# -------------------------
# Operating Profit Margin
# -------------------------

def test_calculate_opm():
    assert calculate_opm(30, 100) == 30.00


def test_calculate_opm_zero_sales():
    assert calculate_opm(30, 0) is None


# -------------------------
# Return on Equity
# -------------------------

def test_calculate_roe():
    assert calculate_roe(20, 10, 90) == 20.00


def test_calculate_roe_negative_equity():
    assert calculate_roe(20, -50, 40) is None


# -------------------------
# ROCE
# -------------------------

def test_calculate_roce():
    result = calculate_roce(
        "ABB",
        operating_profit=100,
        depreciation=20,
        equity_capital=100,
        reserves=300,
        borrowings=100,
    )

    expected = round((80 / 500) * 100, 2)

    assert result == expected


def test_calculate_roce_bank():
    result = calculate_roce(
        "HDFCBANK",
        operating_profit=100,
        depreciation=20,
        equity_capital=100,
        reserves=300,
        borrowings=100,
    )

    assert result is None


def test_calculate_roce_negative_capital():
    result = calculate_roce(
        "ABB",
        operating_profit=100,
        depreciation=20,
        equity_capital=-100,
        reserves=20,
        borrowings=10,
    )

    assert result is None


# -------------------------
# Debt to Equity
# -------------------------

def test_debt_to_equity():
    assert calculate_debt_to_equity(50, 100, 100) == 0.25


def test_debt_to_equity_negative_equity():
    assert calculate_debt_to_equity(50, -100, 50) is None


# -------------------------
# Interest Coverage
# -------------------------

def test_interest_coverage():
    assert calculate_interest_coverage(100, 20, 10) == 12.00


def test_interest_coverage_zero_interest():
    assert calculate_interest_coverage(100, 20, 0) == 999


def test_interest_coverage_null_interest():
    assert calculate_interest_coverage(100, 20, None) is None


# -------------------------
# Asset Turnover
# -------------------------

def test_asset_turnover():
    assert calculate_asset_turnover(200, 100) == 2.00


def test_asset_turnover_zero_assets():
    assert calculate_asset_turnover(200, 0) is None