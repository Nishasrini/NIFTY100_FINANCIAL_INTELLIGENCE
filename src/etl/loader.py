import pandas as pd
def load_excel(file_path):
    return pd.read_excel(file_path, header=1)
def normalize_ticker(ticker):
    return str(ticker).strip().upper()
def normalize_year(year):
    year = str(year).strip()
    if year.startswith("Mar-"):
        yy = int(year.split("-")[1])
        return f"20{yy:02d}-03"
    return year
files = [
    "data/raw/companies.xlsx",
    "data/raw/profitandloss.xlsx",
    "data/raw/balancesheet.xlsx",
    "data/raw/cashflow.xlsx",
    "data/raw/analysis.xlsx",
    "data/raw/documents.xlsx",
    "data/raw/prosandcons.xlsx"
]

for file in files:
    df = load_excel(file)
    print(f"{file} loaded successfully. Rows: {len(df)}")

    