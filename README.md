# Credit Risk Analysis

This project explores credit risk using a credit-card customer dataset from the UCI Machine Learning Repository.

The project combines Python, SQL, machine learning, and Tableau to analyze customer credit behaviour and default risk.

## Project Components

### Python Analysis

The Python script:

- Downloads the credit-card dataset from the UCI Machine Learning Repository
- Cleans and renames the dataset columns
- Creates a credit portfolio dataset
- Exports the portfolio to CSV for Tableau
- Creates an SQLite database
- Runs SQL queries for credit-risk analysis
- Builds a Logistic Regression model to predict customer default
- Evaluates the model using a confusion matrix and classification report

### SQL Analysis

SQL is used to analyze the credit portfolio, including:

- Overall portfolio default rate
- Average credit limit
- Customer delinquency
- Default rates by repayment status
- Credit utilisation
- Combined delinquency and utilisation risk

### Tableau Visualization

Tableau is used to create visualizations and dashboards from the exported credit portfolio data.

Current visualizations include:

- Overall portfolio default rate
- Default rate by delinquency status
- Default rate by education category

Additional credit-risk visualizations can be added as the project develops.

## Project Files

- `Credit_Risk_Analysis.py` - Python, SQL, and machine-learning analysis
- `credit_portfolio.csv` - Dataset exported for Tableau
- `credit_risk.db` - SQLite database used for SQL analysis
- Tableau workbook/dashboard - Interactive credit-risk visualizations

## Technologies Used

- Python
- Pandas
- SQLite / SQL
- Scikit-learn
- Tableau
- UCI Machine Learning Repository

## Objective

The objective of this project is to demonstrate how credit portfolio data can be explored using SQL and Python, visualized using Tableau, and used to build a basic predictive model for customer default risk.

This is an educational data-analysis project and does not represent the credit-risk models or decision-making processes of any specific financial institution.
