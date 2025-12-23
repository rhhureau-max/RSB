# RSB

## ICT Midnight Open Analysis Tool

This repository includes a comprehensive Python tool for analyzing ICT (Inner Circle Trader) statistics on NQ futures data.

### Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the analysis:**
```bash
python ict_midnight_open_analysis.py your_NQ_data.csv
```

3. **Generate sample data for testing:**
```bash
python generate_sample_nq_data.py
python ict_midnight_open_analysis.py sample_NQ_M1_data.csv
```

### Documentation

For detailed documentation, see [ICT_ANALYSIS_README.md](ICT_ANALYSIS_README.md)

### Features

- ✅ Analyzes Midnight Open (23:00 Chicago time) probability of touch
- ✅ London Killzone analysis (01:00-05:00 Chicago time)
- ✅ Comprehensive statistics by day of week
- ✅ Visual analytics with charts and graphs
- ✅ CSV export of detailed results
- ✅ Handles Chicago timezone automatically
- ✅ Robust error handling and data validation

### Output

The analysis produces:
- Console output with detailed statistics
- `ict_midnight_open_results.csv` - Detailed daily results
- `ict_midnight_open_analysis.png` - Visual analytics dashboard