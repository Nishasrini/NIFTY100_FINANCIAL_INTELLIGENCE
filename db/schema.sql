PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

CREATE TABLE profitandloss (
    id INTEGER,
    company_id TEXT NOT NULL,
    year TEXT NOT NULL,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    opm_percentage REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL,
    PRIMARY KEY (company_id, year)
    
);

CREATE TABLE balancesheet (
    id INTEGER,
    company_id TEXT NOT NULL,
    year TEXT NOT NULL,
    equity_capital REAL,
    reserves REAL,
    borrowings REAL,
    other_liabilities REAL,
    total_liabilities REAL,
    fixed_assets REAL,
    cwip REAL,
    investments REAL,
    other_asset REAL,
    total_assets REAL,
    PRIMARY KEY (company_id, year)
    
);

CREATE TABLE cashflow (
    id INTEGER,
    company_id TEXT NOT NULL,
    year TEXT NOT NULL,
    operating_activity REAL,
    investing_activity REAL,
    financing_activity REAL,
    net_cash_flow REAL,
    PRIMARY KEY (company_id, year)
);

CREATE TABLE analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    compounded_sales_growth TEXT,
    compounded_profit_growth TEXT,
    stock_price_cagr TEXT,
    roe TEXT
    
);
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    Year INTEGER,
    Annual_Report TEXT
    
);

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    pros TEXT,
    cons TEXT
    
);

-- supporting file tables

CREATE TABLE sectors (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    broad_sector TEXT,
    sub_sector TEXT,
    index_weight_pct REAL,
    market_cap_category TEXT
);

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    adjusted_close REAL
);

CREATE TABLE market_cap (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    market_cap_crore REAL,
    enterprise_value_crore REAL,
    pe_ratio REAL,
    pb_ratio REAL,
    ev_ebitda REAL,
    dividend_yield_pct REAL
);

DROP TABLE IF EXISTS financial_ratios;

CREATE TABLE financial_ratios (

    company_id TEXT,
    year TEXT,

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    return_on_capital_employed_pct REAL,

    debt_to_equity REAL,
    interest_coverage REAL,
    asset_turnover REAL,

    sales_3yr_cagr REAL,
    sales_5yr_cagr REAL,
    sales_10yr_cagr REAL,

    net_profit_3yr_cagr REAL,
    net_profit_5yr_cagr REAL,
    net_profit_10yr_cagr REAL,

    eps_3yr_cagr REAL,
    eps_5yr_cagr REAL,
    eps_10yr_cagr REAL,

    free_cash_flow_cr REAL,
    capex_cr REAL,
    cfo_quality_score REAL,
    capex_intensity_pct REAL,
    fcf_conversion_pct REAL,

    capital_allocation_pattern TEXT,

    PRIMARY KEY(company_id,year)
);

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group_name TEXT,
    company_id TEXT,
    is_benchmark INTEGER
);