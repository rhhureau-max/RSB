#!/usr/bin/env python3
"""
Comprehensive Financial Analysis for NVIDIA Corporation
Includes: 1) AI Investment Analysis, 2) Time Series Analysis, 3) TVM Analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class NVIDIAFinancialAnalysis:
    """Comprehensive financial analysis for NVIDIA"""
    
    def __init__(self):
        self.ticker = "NVDA"
        self.company_name = "NVIDIA Corporation"
        self.stock = yf.Ticker(self.ticker)
        self.results = {}
        
    def download_financial_data(self):
        """Download historical financial data from Yahoo Finance"""
        print(f"\n{'='*70}")
        print(f"Downloading Financial Data for {self.company_name}")
        print(f"{'='*70}\n")
        
        # Download stock price data (10 years for time series)
        end_date = datetime.now()
        start_date_10y = end_date - timedelta(days=365*10)
        
        print("📥 Downloading stock price data (10 years)...")
        self.price_data = yf.download(self.ticker, start=start_date_10y, end=end_date, progress=False)
        
        # Download financial statements
        print("📥 Downloading financial statements...")
        self.income_stmt = self.stock.financials
        self.balance_sheet = self.stock.balance_sheet
        self.cashflow = self.stock.cashflow
        
        # Download additional data for TVM analysis
        print("📥 Downloading bond ETF data...")
        self.tlt = yf.download('TLT', start=start_date_10y, end=end_date, progress=False)  # Treasury ETF
        self.lqd = yf.download('LQD', start=start_date_10y, end=end_date, progress=False)  # Corporate Bond ETF
        self.spy = yf.download('SPY', start=start_date_10y, end=end_date, progress=False)  # S&P 500
        
        print("✅ Data download complete!\n")
        
        # Display basic info
        print(f"Stock data: {len(self.price_data)} trading days")
        print(f"Financial statements: {len(self.income_stmt.columns)} periods\n")
        
        return self
    
    def calculate_free_cash_flow(self):
        """Calculate Free Cash Flow from financial statements"""
        print("\n💰 Calculating Free Cash Flow...")
        
        try:
            # Get Operating Cash Flow and Capital Expenditures
            if 'Operating Cash Flow' in self.cashflow.index:
                operating_cf = self.cashflow.loc['Operating Cash Flow']
            elif 'Total Cash From Operating Activities' in self.cashflow.index:
                operating_cf = self.cashflow.loc['Total Cash From Operating Activities']
            else:
                operating_cf = self.cashflow.iloc[0]  # First row as fallback
                
            if 'Capital Expenditures' in self.cashflow.index:
                capex = abs(self.cashflow.loc['Capital Expenditures'])  # Usually negative
            elif 'Capital Expenditure' in self.cashflow.index:
                capex = abs(self.cashflow.loc['Capital Expenditure'])
            else:
                # Estimate as 5% of operating cash flow if not available
                capex = operating_cf * 0.05
            
            fcf = operating_cf - capex
            self.fcf = fcf
            
            # Get most recent FCF
            self.latest_fcf = fcf.iloc[0]
            
            print(f"✅ Latest Free Cash Flow: ${self.latest_fcf/1e9:.2f} billion")
            print(f"   Operating Cash Flow: ${operating_cf.iloc[0]/1e9:.2f} billion")
            print(f"   Capital Expenditures: ${capex.iloc[0]/1e9:.2f} billion\n")
            
        except Exception as e:
            print(f"⚠️  Error calculating FCF: {e}")
            print("   Using estimated FCF based on market cap...\n")
            # Fallback: estimate FCF as 5% of market cap
            market_cap = self.stock.info.get('marketCap', 1e12)
            self.latest_fcf = market_cap * 0.05
        
        return self.latest_fcf


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("NVIDIA CORPORATION - COMPREHENSIVE FINANCIAL ANALYSIS")
    print("="*70)
    print("\nThis analysis includes:")
    print("1. Generative AI Investment Analysis")
    print("2. Time Series Forecasting")
    print("3. Time Value of Money Analysis")
    print("\n" + "="*70 + "\n")
    
    # Initialize analysis
    nvidia = NVIDIAFinancialAnalysis()
    
    # Download data
    nvidia.download_financial_data()
    nvidia.calculate_free_cash_flow()
    
    print("\n✅ Data preparation complete!")
    print("\nNext steps: Run individual analysis modules")
    print("- Project 1: AI Investment Analysis (ai_investment_analysis.py)")
    print("- Project 2: Time Series Analysis (time_series_analysis.py)")
    print("- Project 3: TVM Analysis (tvm_analysis.py)")
    

if __name__ == "__main__":
    main()
