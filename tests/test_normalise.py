import sys
import os

sys.path.append(os.path.abspath("."))

from src.etl.loader import normalize_ticker, normalize_year

def test_ticker():
    assert normalize_ticker("tcs") == "TCS"
    assert normalize_ticker(" TCS ") == "TCS"

def test_year():
    assert normalize_year("Mar-23") == "2023-03"
    assert normalize_year("Mar-24") == "2024-03"