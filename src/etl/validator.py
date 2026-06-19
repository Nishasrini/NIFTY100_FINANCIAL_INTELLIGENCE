import pandas as pd
class Validator:
    def __init__(self):
        self.failures = []
    def add_failure(self, table, field, issue):
        self.failures.append([table, field, issue])
    def company_id_not_null(self, df, table):
        if "company_id" not in df.columns:
            return
        if df["company_id"].isnull().any():
            self.add_failure(
                table,
                "company_id",
                "Contains null values"
            )
    def year_not_null(self, df, table):
        year_col = None
        if "year" in df.columns:
            year_col = "year"
        elif "Year" in df.columns:
            year_col = "Year"
        if year_col is None:
            return
        if df[year_col].isnull().any():
            self.add_failure(
                table,
                year_col,
                "Contains null values"
            )
    def duplicate_records(self, df, table):
        cols = []
        if "company_id" in df.columns:
            cols.append("company_id")
        if "year" in df.columns:
            cols.append("year")
        if "Year" in df.columns:
            cols.append("Year")
        if len(cols) < 2:
            return
        if df.duplicated(subset=cols).any():
            self.add_failure(
                table,
                ",".join(cols),
                "Duplicate records found"
            )
    def sales_positive(self, df):
        if (df["sales"] <= 0).any():
            self.add_failure(
                "profitandloss",
                "sales",
                "Sales must be > 0"
            )
    def balance_sheet_check(self, df):
        mismatch = (
            df["total_assets"]
            != df["total_liabilities"]
        )
        if mismatch.any():
            self.add_failure(
                "balancesheet",
                "total_assets,total_liabilities",
                "Assets != Liabilities"
            )
    def cashflow_check(self, df):
        expected = (
            df["operating_activity"]
            + df["investing_activity"]
            + df["financing_activity"]
        )
        mismatch = expected != df["net_cash_flow"]
        if mismatch.any():
            self.add_failure(
                "cashflow",
                "net_cash_flow",
                "Cashflow mismatch"
            )
    def save_report(self):
        report = pd.DataFrame(
            self.failures,
            columns=[
                "table",
                "field",
                "issue"
            ]
        )
        report.to_csv(
            "validation_failures.csv",
            index=False
        )
if __name__ == "__main__":
    validator = Validator()
    companies = pd.read_excel("data/raw/companies.xlsx",header=1)
    profitandloss = pd.read_excel("data/raw/profitandloss.xlsx",header=1)
    balancesheet = pd.read_excel("data/raw/balancesheet.xlsx",header=1)
    cashflow = pd.read_excel("data/raw/cashflow.xlsx",header=1)
    analysis = pd.read_excel("data/raw/analysis.xlsx",header=1)
    documents = pd.read_excel("data/raw/documents.xlsx",header=1)
    prosandcons = pd.read_excel( "data/raw/prosandcons.xlsx" ,header=1)
    datasets = {
        "companies": companies,
        "profitandloss": profitandloss,
        "balancesheet": balancesheet,
        "cashflow": cashflow,
        "analysis": analysis,
        "documents": documents,
        "prosandcons": prosandcons
    }
    for name, df in datasets.items():
        validator.company_id_not_null(df, name)
        validator.year_not_null(df, name)
        validator.duplicate_records(df, name)
    validator.sales_positive(profitandloss)
    validator.balance_sheet_check(balancesheet)
    validator.cashflow_check(cashflow)
    validator.save_report()
    print("validation_failures.csv generated")