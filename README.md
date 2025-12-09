# RSB - Financial Modeling & Trading Strategies

This repository contains advanced financial modeling projects and quantitative trading strategies.

## Fair Value Gap (FVG) Backtest Strategy

A complete Python backtesting system for NQ Nasdaq Futures trading based on Fair Value Gap (FVG) patterns detected during the New York market open.

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run example
python example_usage.py

# Use with your own data
python fvg_backtest_strategy.py
```

### Features

- ✅ Automatic timezone conversion (UTC → EST/EDT)
- ✅ FVG detection (bullish & bearish patterns)
- ✅ Smart entry signals with breakout confirmation
- ✅ Dynamic risk management (SL & TP levels)
- ✅ Multiple take profit targets (TP1, TP2, TP3)
- ✅ Comprehensive statistics (Win Rate, Profit Factor, Drawdown)
- ✅ CSV export of results

### Files

- **`fvg_backtest_strategy.py`** - Main backtesting engine
- **`example_usage.py`** - Usage examples and demonstrations
- **`example_nq_data.csv`** - Sample data with FVG patterns
- **`FVG_STRATEGY_README.md`** - Detailed documentation (French)
- **`requirements.txt`** - Python dependencies

### Usage

```python
from fvg_backtest_strategy import FVGBacktester

# Load your NQ futures 1-minute data
backtester = FVGBacktester(data_path='your_nq_data.csv')

# Run backtest
results = backtester.run_backtest()

# Print statistics
backtester.print_statistics()

# Export results
backtester.export_results('results.csv')
```

### Data Format

CSV file with columns: `DateTime, Open, High, Low, Close`

```
DateTime,Open,High,Low,Close
2024-01-02 13:30:00,16000.0,16010.0,15995.0,16005.0
2024-01-02 13:31:00,16005.0,16012.0,16002.0,16010.0
...
```

*Note: Times should be in UTC (will be converted to NY time automatically)*

### Documentation

See [FVG_STRATEGY_README.md](FVG_STRATEGY_README.md) for complete documentation in French, including:
- Strategy logic details
- Parameter customization
- Performance metrics
- Risk considerations

### Requirements

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- pytz >= 2021.1

---

## Other Projects

This repository also contains other financial modeling projects:
- Advanced Financial Modeling & Time Series Analysis
- Time Value of Money Analysis
- Energy Data Analysis