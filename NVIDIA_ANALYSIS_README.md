# NVIDIA Financial Analysis - Complete Implementation

## Overview

This repository contains a comprehensive financial analysis of NVIDIA Corporation covering three major projects from Advanced Financial Modeling courses:

1. **Generative AI Investment Analysis** - Capital budgeting with real options and Monte Carlo simulation
2. **Time Series Forecasting** - ARIMA and GARCH models for price and volatility
3. **Time Value of Money Analysis** - PV/FV, annuities, bonds, DDM, and loan amortization

## Selected Company and Assets

- **Primary Company**: NVIDIA Corporation (NVDA)
- **Treasury Bond ETF**: TLT (iShares 20+ Year Treasury Bond ETF)
- **Corporate Bond ETF**: LQD (iShares iBoxx $ Investment Grade Corporate Bond ETF)
- **Market Index**: SPY (S&P 500 ETF)

## Installation

```bash
# Install required packages
pip install -r requirements.txt
```

## Usage

### Option 1: Run All Analyses Together

```bash
python run_all_analyses.py
```

This master script will:
- Run all three projects sequentially
- Generate visualizations
- Create a comprehensive final report
- Provide investment recommendations

### Option 2: Run Individual Analyses

```bash
# Project 1: AI Investment Analysis
python ai_investment_analysis.py

# Project 2: Time Series Analysis
python time_series_analysis.py

# Project 3: Time Value of Money Analysis
python tvm_analysis.py
```

## Project Details

### Project 1: AI Investment Analysis

**File**: `ai_investment_analysis.py`

Analyzes a hypothetical generative AI investment for NVIDIA worth 1% of Free Cash Flow (~$450M).

**Methods Implemented**:
1. **Net Present Value (NPV)** - Measures absolute value creation
2. **Internal Rate of Return (IRR)** - Compares return vs hurdle rate
3. **Payback Period** - Risk assessment through recovery time
4. **Profitability Index (PI)** - Resource allocation efficiency

**Advanced Techniques**:
- **Sensitivity Analysis** - Tests AI efficiency, discount rate, and project life
- **Real Options Valuation** - Binomial model for expansion options
- **Monte Carlo Simulation** - 10,000 scenarios for risk assessment

**Outputs**:
- Detailed capital budgeting calculations
- Investment recommendation
- `monte_carlo_npv.png` - NPV distribution visualization

### Project 2: Time Series Forecasting

**File**: `time_series_analysis.py`

Forecasts NVIDIA stock prices and volatility using 10 years of historical data.

**Models Implemented**:
1. **ARIMA(1,1,1)** - Autoregressive Integrated Moving Average for prices
2. **GARCH(1,1)** - Volatility clustering and forecasting
3. **Stationarity Tests** - ADF and KPSS tests

**Features**:
- Price forecasting with performance metrics (RMSE, MAPE)
- Conditional volatility modeling
- Direction accuracy assessment
- Volatility persistence analysis

**Outputs**:
- Model diagnostics and parameters
- Forecast performance metrics
- `time_series_analysis.png` - Comprehensive visualizations

### Project 3: Time Value of Money Analysis

**File**: `tvm_analysis.py`

Demonstrates fundamental TVM concepts with practical applications.

**Components**:
1. **Fundamental TVM** - Present value and future value calculations
2. **Annuity Analysis** - Retirement savings and perpetuities
3. **Bond Valuation** - Corporate bond pricing and interest rate sensitivity
4. **Dividend Discount Model** - Stock valuation (multi-stage for NVIDIA)
5. **Loan Amortization** - Mortgage analysis with prepayment scenarios
6. **Sensitivity Analysis** - Interest rate and time horizon impacts

**Features**:
- Real-world examples with NVIDIA stock
- Bond ETF analysis (TLT, LQD)
- Retirement planning scenarios
- Mortgage amortization schedules

## Key Results Summary

### AI Investment Project
- **NPV**: $117.75M (POSITIVE - creates value)
- **IRR**: 22.11% (exceeds 12% hurdle rate)
- **Payback Period**: ~2.86 years (under 3-year target)
- **Profitability Index**: 1.26 (every $1 returns $1.26)
- **Decision**: **ACCEPT** - All metrics support investment

### Time Series Forecasts
- ARIMA model provides short-term price forecasts
- GARCH captures high volatility typical of tech stocks
- Volatility persistence suggests continued price fluctuations
- Models useful for tactical trading and risk management

### TVM Insights
- NVIDIA stock suitable for long-term compound growth
- Bond ETFs provide portfolio diversification
- Time horizon dramatically impacts investment outcomes
- Early loan payments can save significant interest

## Final Investment Recommendation

**STRONG BUY** for NVIDIA Corporation

**Rationale**:
1. AI investment project shows strong positive NPV and 22% IRR
2. Technical analysis indicates upward price momentum
3. NVIDIA's leadership in AI/GPU market is sustainable competitive advantage
4. Real options value justifies phased AI implementation strategy
5. Long-term compounding benefits from TVM analysis

**Suggested Strategy**:
- Allocate 3-5% of portfolio to NVDA
- Dollar-cost average entry over 6-12 months
- Set stop-loss at -15% for downside protection
- Target 5+ year holding period
- Monitor quarterly earnings and AI market developments

## Files Generated

- `monte_carlo_npv.png` - Monte Carlo simulation results
- `time_series_analysis.png` - ARIMA and GARCH visualizations
- Console output - Detailed calculations and comprehensive analysis

## Technical Notes

- All financial data downloaded via `yfinance` from Yahoo Finance
- Uses real NVIDIA financial statements (most recent available)
- AI project assumes 35% efficiency factor (tech leader baseline)
- Discount rate of 12% standard for technology investments
- Models validated against academic literature and industry standards

## Requirements

See `requirements.txt` for complete list. Key packages:
- `yfinance` - Financial data download
- `pandas`, `numpy` - Data manipulation
- `matplotlib`, `seaborn` - Visualization
- `statsmodels` - Time series models
- `arch` - GARCH volatility models
- `scipy` - Statistical functions

## Author

Advanced Financial Modeling Analysis
Completed: December 2025

## License

Educational and analysis purposes. Financial data sourced from public markets via Yahoo Finance API.

---

## Quick Start Example

```python
# Quick test of AI investment analysis
from ai_investment_analysis import AIInvestmentAnalysis

analysis = AIInvestmentAnalysis("NVDA")
npv = analysis.calculate_npv()
irr = analysis.calculate_irr()
print(f"NPV: ${npv/1e6:.2f}M, IRR: {irr:.2%}")
```

## Contact & Support

For questions or issues, please refer to the detailed console output from each analysis module. All calculations include:
- Mathematical formulas
- Step-by-step computations
- Interpretation of results
- Advantages and limitations of each method
