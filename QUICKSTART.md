# Quick Start Guide - FVG Backtest Strategy

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install pandas numpy pytz
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Example

```bash
python example_usage.py
```

This will:
- Load sample NQ futures data
- Detect FVG patterns
- Execute trades with risk management
- Display comprehensive statistics

### Step 3: Use Your Own Data

#### Prepare Your Data

Your CSV file should have these columns:
```
DateTime,Open,High,Low,Close
```

Example:
```csv
DateTime,Open,High,Low,Close
2024-01-02 13:30:00,16000.0,16010.0,15995.0,16005.0
2024-01-02 13:31:00,16005.0,16012.0,16002.0,16010.0
```

**Important:** 
- DateTime should be in UTC (will be converted to NY time automatically)
- Data must be in 1-minute timeframe
- Ensure data covers the 08:30-09:00 EST/EDT window

#### Run Your Backtest

```python
from fvg_backtest_strategy import FVGBacktester

# Load your data
backtester = FVGBacktester(data_path='path/to/your/nq_data.csv')

# Run backtest
results = backtester.run_backtest()

# Show statistics
backtester.print_statistics()

# Export results
backtester.export_results('my_backtest_results.csv')
```

### Step 4: Analyze Results

The backtest will display:

```
================================================================================
BACKTEST PERFORMANCE STATISTICS
================================================================================

📊 TRADE SUMMARY
  Total Trades:        45
  Winning Trades:      28
  Losing Trades:       17

🎯 WIN RATES
  Overall Win Rate:    62.22%
  TP1 Hit Rate:        55.56%
  TP2 Hit Rate:        40.00%
  TP3 Hit Rate:        22.22%

💰 PROFIT & LOSS
  Total PnL:           125.50 points
  Profit Factor:       3.10

📉 RISK METRICS
  Max Drawdown:        -15.25 points
================================================================================
```

## 📖 Strategy Overview

### What is a Fair Value Gap (FVG)?

**Bullish FVG:** When the high of candle (n-1) is below the low of candle (n+1)
- Creates a "gap" in price
- Strategy enters SHORT when price breaks below the FVG

**Bearish FVG:** When the low of candle (n-1) is above the high of candle (n+1)
- Creates a "gap" in price  
- Strategy enters LONG when price breaks above the FVG

### Trading Rules

1. **Setup Detection:** 08:30-09:00 NY time
   - Find the FIRST FVG in this window
   - If no FVG found, skip the day

2. **Entry Signal:**
   - Wait for price to break through the FVG zone
   - Enter immediately on candle close

3. **Risk Management:**
   - Stop Loss: 0.5 points beyond trigger candle extreme
   - Take Profit 1: 1R (33% position)
   - Take Profit 2: 1.5R (33% position)
   - Take Profit 3: 2R (34% position)

## 🛠️ Customization

### Change Setup Window

Edit `fvg_backtest_strategy.py`:

```python
# Find line ~160 in find_first_fvg()
setup_window = day_data[
    (day_data['Time'] >= time(8, 30)) &  # Change start time
    (day_data['Time'] < time(9, 0))      # Change end time
]
```

### Change Stop Loss Distance

Edit `fvg_backtest_strategy.py`:

```python
# Find line ~220 in calculate_risk_levels()
sl_price = entry['trigger_high'] + 0.5  # Change 0.5 to your value
```

### Change Take Profit Levels

Edit `fvg_backtest_strategy.py`:

```python
# Find line ~235 in calculate_risk_levels()
tp1 = entry['entry_price'] - (1.0 * risk)   # Change 1.0 (1R)
tp2 = entry['entry_price'] - (1.5 * risk)   # Change 1.5 (1.5R)
tp3 = entry['entry_price'] - (2.0 * risk)   # Change 2.0 (2R)
```

### Change Position Sizing

Edit `fvg_backtest_strategy.py`:

```python
# Find lines ~310-370 in simulate_trade()
gain = (entry['entry_price'] - levels['tp3']) * 0.34  # Change 0.34 (34%)
gain = (entry['entry_price'] - levels['tp2']) * 0.33  # Change 0.33 (33%)
gain = (entry['entry_price'] - levels['tp1']) * 0.33  # Change 0.33 (33%)
```

## 📊 Understanding Results

### Results CSV Columns

| Column | Description |
|--------|-------------|
| date | Trade date |
| type | 'long' or 'short' |
| entry_price | Entry price |
| entry_time | Entry time (NY) |
| sl_price | Stop loss price |
| tp1_price, tp2_price, tp3_price | Take profit prices |
| tp1_hit, tp2_hit, tp3_hit | Whether each TP was hit |
| sl_hit | Whether SL was hit |
| pnl_points | Profit/Loss in points |
| risk_points | Risk taken in points |

### Key Metrics

- **Win Rate**: % of profitable trades
- **TP Hit Rates**: % of trades reaching each TP level
- **Profit Factor**: Gross Profit / Gross Loss (>1 is profitable)
- **Max Drawdown**: Largest peak-to-trough decline

## ⚠️ Important Notes

1. **Paper Trading First**: Test on paper before live trading
2. **No Slippage**: This backtest assumes perfect fills
3. **No Commissions**: Add commissions to get realistic results
4. **Historical Data**: Past performance ≠ future results
5. **Market Conditions**: Strategy may perform differently in different market regimes

## 🔧 Troubleshooting

### No Trades Generated

**Issue**: Backtest runs but generates 0 trades

**Solutions:**
1. Check your data covers 08:30-09:00 NY time
2. Verify DateTime format is correct
3. Ensure data is 1-minute timeframe
4. Check for data gaps or missing candles

### Timezone Issues

**Issue**: Times don't match expected NY times

**Solutions:**
1. Ensure input data is in UTC
2. Or localize your data before loading:
```python
df['DateTime'] = pd.to_datetime(df['DateTime']).dt.tz_localize('America/New_York')
```

### Installation Issues

**Issue**: pip install fails

**Solutions:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with specific versions
pip install pandas==1.5.3 numpy==1.24.3 pytz==2023.3
```

## 📚 More Information

- **Full Documentation**: See [FVG_STRATEGY_README.md](FVG_STRATEGY_README.md)
- **Strategy Details**: See [README.md](README.md)
- **Code Examples**: See [example_usage.py](example_usage.py)

## 🤝 Support

For questions or issues:
1. Check the full documentation
2. Review the example code
3. Verify your data format
4. Test with the provided sample data first

---

**Happy Backtesting! 📈**
