# OLS Return Predictability Analysis

## Overview

This project investigates the predictability of stock returns using regression models on financial and macroeconomic indicators. By exploring the statistical relationship between various predictors and subsequent returns, this analysis seeks to identify signals that can potentially enhance investment decision-making. Key metrics include in-sample fit, statistical significance, and the consistency of predictive power across different periods.

## Data Sources

- Stock Returns Data: Monthly returns for individual stocks and market indices.
- Predictive Variables: Financial ratios, macroeconomic indicators, and technical factors that are commonly hypothesized to influence future returns.

## Key Steps

### Data Cleaning & Preprocessing:

- Merged stock returns with predictive variables, aligning time series data across all indicators.
- Handled missing values by forward-filling and interpolating to maintain continuity without introducing look-ahead bias.

### Regression Analysis:

- Applied linear regression to examine relationships between each predictor and future returns.
- Conducted multivariate regressions to analyze the combined impact of predictors on returns.
- Tested for multicollinearity among predictors to ensure the stability of coefficients.

### Model Evaluation:

- Evaluated in-sample fit using R-squared values to measure the proportion of variance explained.
- Analyzed statistical significance through t-statistics and p-values for each predictor.
- Conducted time-based subsample analysis to assess if predictability remains consistent across different market cycles.

### Out-of-Sample Testing:

- Used rolling window regressions to simulate out-of-sample performance, estimating model stability over time.
- Compared predicted vs. actual returns in the test set to evaluate predictive accuracy.

## Results and Findings

### Predictive Power of Variables:

- Financial ratios such as Price-to-Earnings and Dividend Yield showed strong predictive power with statistically significant coefficients in most periods.
- Macroeconomic indicators, including interest rates and inflation, provided valuable signals, especially during periods of economic transition.
- Technical factors (e.g., past returns and volatility) demonstrated mixed predictability, with stronger results in high-volatility markets.

### Model Performance:

- In-sample R-squared values indicated a moderate to strong fit, suggesting that selected variables capture meaningful variations in stock returns.
- Out-of-sample results: The predictive accuracy of the model was consistent but diminished compared to in-sample performance, as expected in financial time series data.
- The regression model maintained significance across rolling windows, indicating robustness to some market condition changes.

### Subsample Analysis:

- The model's predictive power varied across different market regimes, with better performance during economic recessions and weaker predictability in bullish markets.

## Insights and Best Practices

- Variable Selection: Economic and financial indicators tend to perform well as return predictors; however, their effectiveness may fluctuate with market conditions.
- Rolling Window Analysis: Helps capture time-varying relationships in financial data, enhancing model robustness in out-of-sample contexts.
- Model Stability: Regularly test for multicollinearity to ensure predictors provide unique information and adjust models accordingly over time.

## Files Included
- StockReturns.csv: Dataset containing monthly stock returns.
- PredictiveVariables.csv: Dataset of financial ratios, macroeconomic indicators, and technical factors.

## Future Improvements

- Experiment with non-linear models (e.g., machine learning techniques) to capture more complex relationships.
- Incorporate additional macroeconomic variables (e.g., GDP growth) and alternative data sources (e.g., sentiment analysis) for a broader predictive scope.
- Investigate expanding the analysis to global markets to assess the model's generalizability.

This analysis sheds light on the potential for using financial and economic indicators to predict stock returns, highlighting the importance of variable selection, time-based testing, and market sensitivity when developing predictive financial models.
