-- 1. List all companies with face value > 5
SELECT id, company_name, face_value
FROM companies
WHERE face_value > 5;

-- 2. Top 10 companies by sales
SELECT company_id, year, sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

-- 3. Companies with negative net profit
SELECT company_id, year, net_profit
FROM profitandloss
WHERE net_profit < 0;

-- 4. Top 10 companies by total assets
SELECT company_id, year, total_assets
FROM balancesheet
ORDER BY total_assets DESC
LIMIT 10;

-- 5. Debt-free companies
SELECT company_id, year
FROM balancesheet
WHERE borrowings = 0;

-- 6. Companies with negative operating cash flow
SELECT company_id, year, operating_activity
FROM cashflow
WHERE operating_activity < 0;

-- 7. Companies available in analysis table
SELECT DISTINCT company_id
FROM analysis;

-- 8. Number of annual reports per company
SELECT company_id, COUNT(*) AS report_count
FROM documents
GROUP BY company_id
ORDER BY report_count DESC;

-- 9. Companies having both pros and cons
SELECT company_id, pros, cons
FROM prosandcons
WHERE pros IS NOT NULL
  AND cons IS NOT NULL;

-- 10. Company count by sector
SELECT broad_sector, COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

-- 11. Highest market cap companies
SELECT company_id, year, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- 12. Highest ROE companies
SELECT company_id, year, return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;

-- 13. Number of companies in each peer group
SELECT peer_group_name, COUNT(*) AS companies
FROM peer_groups
GROUP BY peer_group_name
ORDER BY companies DESC;