# Sprint 2 Retrospective

## Overview
Sprint 2 focused on building the Financial Ratio Engine for the NIFTY100 Financial Intelligence Platform. The sprint included implementing profitability, leverage, efficiency, growth, and cash flow KPIs, validating the calculated values, and testing the ratio calculation functions.

## Completed Tasks
- Implemented Net Profit Margin (NPM)
- Implemented Operating Profit Margin (OPM)
- Implemented Return on Equity (ROE)
- Implemented Return on Capital Employed (ROCE)
- Implemented Debt-to-Equity Ratio
- Implemented Interest Coverage Ratio
- Implemented Asset Turnover Ratio
- Implemented Revenue CAGR calculations
- Implemented PAT CAGR calculations
- Implemented EPS CAGR calculations
- Implemented Cash Flow KPIs
- Populated the `financial_ratios` SQLite table
- Performed OPM and ROCE validation
- Created unit tests for KPI calculations
- Successfully passed all 16 unit tests
- Documented ratio edge cases

## Challenges Faced
- Handling division-by-zero scenarios
- Managing missing financial values
- Excluding Banking and NBFC companies from ROCE calculation
- Handling negative shareholder equity
- Validating calculated ratios against reference values
- Writing comprehensive unit tests for edge cases

## Key Learnings
- Financial ratio implementation using Python
- Data transformation with Pandas
- SQLite database operations
- Financial KPI validation techniques
- Unit testing using Pytest
- Edge-case handling and defensive programming

## Improvements for Future Sprints
- Increase unit test coverage
- Automate edge-case logging
- Improve validation reports
- Optimize KPI calculation performance
- Add integration tests for complete workflows

## Sprint Outcome
Sprint 2 was completed successfully. All required financial ratios were implemented, validated, tested, and documented, providing a reliable Financial Ratio Engine for subsequent analytics modules.