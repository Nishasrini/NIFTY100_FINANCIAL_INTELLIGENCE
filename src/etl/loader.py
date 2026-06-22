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
# files = [
#     "data/raw/companies.xlsx",
#     "data/raw/profitandloss.xlsx",
#     "data/raw/balancesheet.xlsx",
#     "data/raw/cashflow.xlsx",
#     "data/raw/analysis.xlsx",
#     "data/raw/documents.xlsx",
#     "data/raw/prosandcons.xlsx"
# ]
supporting_files = {
    "sectors": "data/supporting/sectors.xlsx",
    "stock_prices": "data/supporting/stock_prices.xlsx",
    "market_cap": "data/supporting/market_cap.xlsx",
    "financial_ratios": "data/supporting/financial_ratios.xlsx",
    "peer_groups": "data/supporting/peer_groups.xlsx"
}

# for file in files:
#     df = load_excel(file)
#     print(f"{file} loaded successfully. Rows: {len(df)}")

for table_name, file_path in supporting_files.items():
    df = pd.read_excel(file_path)

    print(f"Loaded {table_name}: {len(df)} rows")