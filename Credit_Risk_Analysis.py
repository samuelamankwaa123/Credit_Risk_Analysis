from ucimlrepo import fetch_ucirepo
import pandas as pd
import sqlite3


print("Downloading credit-card dataset...")

# Download UCI dataset 350
dataset = fetch_ucirepo(id=350)

features = dataset.data.features.copy()
target = dataset.data.targets.copy()

# Combine features and default outcome
portfolio = pd.concat([features, target], axis=1)

# Rename columns to make them understandable
portfolio = portfolio.rename(
    columns={
        "X1": "credit_limit",
        "X2": "sex",
        "X3": "education",
        "X4": "marital_status",
        "X5": "age",
        "X6": "pay_sep",
        "X7": "pay_aug",
        "X8": "pay_jul",
        "X9": "pay_jun",
        "X10": "pay_may",
        "X11": "pay_apr",
        "X12": "bill_sep",
        "X13": "bill_aug",
        "X14": "bill_jul",
        "X15": "bill_jun",
        "X16": "bill_may",
        "X17": "bill_apr",
        "X18": "paid_sep",
        "X19": "paid_aug",
        "X20": "paid_jul",
        "X21": "paid_jun",
        "X22": "paid_may",
        "X23": "paid_apr",
    }
)

# Rename the outcome column
target_column = target.columns[0]
portfolio = portfolio.rename(
    columns={target_column: "default_next_month"}
)

print("\nFirst five customers:")
print(portfolio.head())

print("\nDataset dimensions:")
print(portfolio.shape)

print("\nColumn names:")
print(portfolio.columns.tolist())

# Create an SQLite database beside the Python program
connection = sqlite3.connect("credit_risk.db")

portfolio.to_sql(
    "credit_portfolio",
    connection,
    if_exists="replace",
    index=False
)

print("\nDatabase created successfully: credit_risk.db")

# Run our first portfolio SQL query
query = """
SELECT
    COUNT(*) AS customers,
    ROUND(AVG(credit_limit), 2) AS average_credit_limit,
    SUM(default_next_month) AS defaulting_customers,
    ROUND(
        100.0 * SUM(default_next_month) /
        NULLIF(COUNT(*), 0),
        2
    ) AS default_rate_percent
FROM credit_portfolio;
"""

result = pd.read_sql_query(query, connection)

print("\nPortfolio summary:")
print(result.to_string(index=False))

delinquency_query = """
SELECT
    CASE
        WHEN pay_sep <= 0 THEN 'Current / no delay'
        WHEN pay_sep = 1 THEN '1 month late'
        WHEN pay_sep = 2 THEN '2 months late'
        WHEN pay_sep BETWEEN 3 AND 5 THEN '3-5 months late'
        ELSE '6+ months late'
    END AS delinquency_status,

    COUNT(*) AS customers,

    ROUND(AVG(credit_limit), 2) AS average_credit_limit,

    SUM(default_next_month) AS defaulting_customers,

    ROUND(
        100.0 * SUM(default_next_month)
        / NULLIF(COUNT(*), 0),
        2
    ) AS default_rate_percent

FROM credit_portfolio

GROUP BY
    CASE
        WHEN pay_sep <= 0 THEN 'Current / no delay'
        WHEN pay_sep = 1 THEN '1 month late'
        WHEN pay_sep = 2 THEN '2 months late'
        WHEN pay_sep BETWEEN 3 AND 5 THEN '3-5 months late'
        ELSE '6+ months late'
    END

ORDER BY default_rate_percent DESC;
"""

delinquency_result = pd.read_sql_query(
    delinquency_query,
    connection
)

print("\nDefault risk by September repayment status:")
print(delinquency_result.to_string(index=False))
combined_risk_query = """
WITH risk_data AS (
    SELECT
        default_next_month,

        CASE
            WHEN pay_sep <= 0 THEN 'Current'
            WHEN pay_sep = 1 THEN '1 month late'
            ELSE '2+ months late'
        END AS delinquency_group,

        CASE
            WHEN bill_sep <= 0 THEN 'Below 30%'
            WHEN 1.0 * bill_sep / NULLIF(credit_limit, 0) < 0.30
                THEN 'Below 30%'
            WHEN 1.0 * bill_sep / NULLIF(credit_limit, 0) < 0.60
                THEN '30-59%'
            WHEN 1.0 * bill_sep / NULLIF(credit_limit, 0) < 0.90
                THEN '60-89%'
            ELSE '90% or more'
        END AS utilisation_band

    FROM credit_portfolio
)

SELECT
    delinquency_group,
    utilisation_band,
    COUNT(*) AS customers,
    SUM(default_next_month) AS defaulting_customers,

    ROUND(
        100.0 * SUM(default_next_month)
        / NULLIF(COUNT(*), 0),
        2
    ) AS default_rate_percent

FROM risk_data
GROUP BY
    delinquency_group,
    utilisation_band

ORDER BY default_rate_percent DESC;
"""

combined_risk_result = pd.read_sql_query(
    combined_risk_query,
    connection
)

print("\nCombined delinquency and utilisation risk:")
print(combined_risk_result.to_string(index=False))
connection.close()