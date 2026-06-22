import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = "data/nifty100.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)

    with open("db/schema.sql", "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    return conn


def load_table(conn, dataframe, table_name):
    dataframe.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(dataframe)} rows into {table_name}")


def main():

    conn = create_database()

    raw_path = Path("data/raw")
    supporting_path = Path("data/supporting")

    audit = []

    raw_files = {
        "companies": "companies.xlsx",
        "profitandloss": "profitandloss.xlsx",
        "balancesheet": "balancesheet.xlsx",
        "cashflow": "cashflow.xlsx",
        "analysis": "analysis.xlsx",
        "documents": "documents.xlsx",
        "prosandcons": "prosandcons.xlsx",
    }

    supporting_files = {
        "sectors": "sectors.xlsx",
        "stock_prices": "stock_prices.xlsx",
        "market_cap": "market_cap.xlsx",
        "financial_ratios": "financial_ratios.xlsx",
        "peer_groups": "peer_groups.xlsx",
    }

    # #LOADING RAW FILES

    for table_name, file_name in raw_files.items():

        file_path = raw_path / file_name

        print(f"\nLoading {file_name}...")

        df = pd.read_excel(
            file_path,
            header=1
        )

        if {"company_id", "year"}.issubset(df.columns):

            before_count = len(df)

            df = df.drop_duplicates(
                subset=["company_id", "year"],
                keep="first"
            )

            removed = before_count - len(df)

            if removed > 0:
                print(f"Removed {removed} duplicate rows")

        load_table(
            conn,
            df,
            table_name
        )

        audit.append({
            "table": table_name,
            "rows_in": len(df),
            "rows_out": len(df),
            "rejected": 0
        })

    #LOADING SUPPORTING FILES 

    for table_name, file_name in supporting_files.items():
        file_path = supporting_path / file_name
        print(f"\nLoading {file_name}...")
        df = pd.read_excel(file_path)
        load_table(
            conn,
            df,
            table_name
        )
        audit.append({
            "table": table_name,
            "rows_in": len(df),
            "rows_out": len(df),
            "rejected": 0
        })
    audit_df = pd.DataFrame(audit)
    audit_df.to_csv("data/load_audit.csv", index=False)
    print("\nGenerated load_audit.csv")
    conn.commit()
    conn.close()
    print("\nDatabase created successfully!")
    print(f"Database saved at: {DB_PATH}")

if __name__ == "__main__":
    main()