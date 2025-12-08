#!/usr/bin/env python3
"""
Project 3: Time Value of Money Analysis for NVIDIA
TVM calculations, bond valuation, DDM, and sensitivity analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TVMAnalysis:
    """Time Value of Money Analysis"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("PROJECT 3: TIME VALUE OF MONEY ANALYSIS FOR NVIDIA")
        print("="*70 + "\n")
        
        # Download data
        print("📥 Downloading financial instruments data...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*5)
        
        # NVIDIA stock
        self.nvda = yf.Ticker("NVDA")
        self.nvda_data = yf.download("NVDA", start=start_date, end=end_date, progress=False)
        
        # Treasury Bond ETF (TLT)
        self.tlt_data = yf.download("TLT", start=start_date, end=end_date, progress=False)
        
        # Corporate Bond ETF (LQD)
        self.lqd_data = yf.download("LQD", start=start_date, end=end_date, progress=False)
        
        # S&P 500
        self.spy_data = yf.download("SPY", start=start_date, end=end_date, progress=False)
        
        print(f"✅ Data downloaded successfully!")
        print(f"   NVIDIA: {len(self.nvda_data)} days")
        print(f"   Treasury ETF (TLT): {len(self.tlt_data)} days")
        print(f"   Corporate Bond ETF (LQD): {len(self.lqd_data)} days")
        print(f"   S&P 500: {len(self.spy_data)} days\n")
        
        # Set common TVM parameters
        self.risk_free_rate = 0.045  # 4.5% (10-year Treasury)
        
    def fundamental_tvm_calculations(self):
        """Demonstrate fundamental TVM calculations"""
        print("="*70)
        print("COMPONENT 1: FUNDAMENTAL TIME VALUE OF MONEY CALCULATIONS")
        print("="*70 + "\n")
        
        # Present Value Example
        print("📊 Present Value (PV) Calculations")
        print("-" * 70)
        
        future_value = 1000000  # $1M
        rate = 0.08  # 8%
        years = 10
        
        pv = future_value / (1 + rate)**years
        
        print(f"\n   Scenario: What is $1,000,000 in 10 years worth today?")
        print(f"   Formula: PV = FV / (1 + r)^n")
        print(f"\n   Future Value (FV): ${future_value:,.0f}")
        print(f"   Discount Rate (r): {rate:.1%}")
        print(f"   Time Period (n): {years} years")
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  Present Value: ${pv:>18,.2f}  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        print(f"\n   💡 Interpretation: To have $1M in 10 years at 8% return,")
        print(f"      you need to invest ${pv:,.2f} today.\n")
        
        # Future Value Example
        print("📊 Future Value (FV) Calculations")
        print("-" * 70)
        
        present_value = 100000  # $100K
        rate = 0.10  # 10%
        years = 20
        
        fv = present_value * (1 + rate)**years
        
        print(f"\n   Scenario: Investing $100,000 at 10% for 20 years")
        print(f"   Formula: FV = PV × (1 + r)^n")
        print(f"\n   Present Value (PV): ${present_value:,.0f}")
        print(f"   Rate of Return (r): {rate:.1%}")
        print(f"   Time Period (n): {years} years")
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  Future Value: ${fv:>19,.2f}  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        print(f"\n   💡 Interpretation: $100K grows to ${fv:,.2f} in 20 years")
        print(f"      That's a {(fv/present_value):.2f}x return!\n")
        
        # Comparing investment alternatives
        print("📊 Comparing Investment Alternatives")
        print("-" * 70)
        
        investment = 50000
        scenarios = [
            ("Conservative (6%)", 0.06, 15),
            ("Moderate (8%)", 0.08, 15),
            ("Aggressive (12%)", 0.12, 15)
        ]
        
        print(f"\n   Initial Investment: ${investment:,.0f}")
        print(f"   Time Horizon: 15 years\n")
        
        for name, rate, years in scenarios:
            fv = investment * (1 + rate)**years
            print(f"   {name:20s}: ${fv:>12,.2f}")
        
        print(f"\n   💡 The aggressive strategy yields significantly higher returns")
        print(f"      but comes with higher risk.\n")
    
    def annuity_analysis(self):
        """Analyze annuities and retirement savings"""
        print("="*70)
        print("COMPONENT 2: ANNUITY ANALYSIS")
        print("="*70 + "\n")
        
        # Present Value of Annuity
        print("📊 Present Value of Annuity (PVA)")
        print("-" * 70)
        
        pmt = 5000  # Annual payment
        rate = 0.07  # 7%
        years = 30
        
        pva = pmt * (1 - (1 + rate)**(-years)) / rate
        
        print(f"\n   Scenario: Valuing a 30-year annuity paying $5,000/year")
        print(f"   Formula: PVA = PMT × [1 - (1+r)^-n] / r")
        print(f"\n   Annual Payment (PMT): ${pmt:,.0f}")
        print(f"   Discount Rate (r): {rate:.1%}")
        print(f"   Number of Periods (n): {years} years")
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  PV of Annuity: ${pva:>18,.2f}  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        total_payments = pmt * years
        print(f"\n   Total Payments: ${total_payments:,.0f}")
        print(f"   Present Value: ${pva:,.2f}")
        print(f"   💡 The annuity stream is worth ${pva:,.2f} today\n")
        
        # Future Value of Annuity - Retirement Savings
        print("📊 Future Value of Annuity (FVA) - Retirement Planning")
        print("-" * 70)
        
        monthly_contribution = 1000  # $1K per month
        annual_rate = 0.08
        monthly_rate = annual_rate / 12
        years = 30
        months = years * 12
        
        fva = monthly_contribution * ((1 + monthly_rate)**months - 1) / monthly_rate
        
        print(f"\n   Scenario: Monthly retirement savings for 30 years")
        print(f"   Formula: FVA = PMT × [(1+r)^n - 1] / r")
        print(f"\n   Monthly Contribution: ${monthly_contribution:,.0f}")
        print(f"   Annual Return: {annual_rate:.1%} ({monthly_rate*100:.3f}% monthly)")
        print(f"   Investment Period: {years} years ({months} months)")
        print(f"\n   ╔═══════════════════════════════════════════╗")
        print(f"   ║  Retirement Fund: ${fva:>20,.2f}  ║")
        print(f"   ╚═══════════════════════════════════════════╝")
        
        total_contributed = monthly_contribution * months
        interest_earned = fva - total_contributed
        
        print(f"\n   Total Contributed: ${total_contributed:,.0f}")
        print(f"   Interest Earned: ${interest_earned:,.2f}")
        print(f"   Return Multiple: {(fva/total_contributed):.2f}x")
        print(f"   💡 Compound interest creates ${interest_earned:,.2f} of wealth!\n")
        
        # Perpetuity
        print("📊 Perpetuity Valuation")
        print("-" * 70)
        
        perpetual_payment = 10000  # $10K per year forever
        rate = 0.06  # 6%
        
        pv_perpetuity = perpetual_payment / rate
        
        print(f"\n   Scenario: Valuing a perpetual payment stream")
        print(f"   Formula: PV = PMT / r")
        print(f"\n   Annual Payment: ${perpetual_payment:,.0f}")
        print(f"   Discount Rate: {rate:.1%}")
        print(f"\n   ╔══════════════════════════════════════════╗")
        print(f"   ║  PV of Perpetuity: ${pv_perpetuity:>18,.2f}  ║")
        print(f"   ╚══════════════════════════════════════════╝")
        
        print(f"\n   💡 A $10K annual perpetuity is worth ${pv_perpetuity:,.2f} today\n")
    
    def bond_valuation(self):
        """Bond valuation analysis"""
        print("="*70)
        print("COMPONENT 3: BOND VALUATION")
        print("="*70 + "\n")
        
        print("📊 Corporate Bond Valuation")
        print("-" * 70)
        
        # Bond parameters
        face_value = 1000
        coupon_rate = 0.05  # 5% annual coupon
        annual_coupon = face_value * coupon_rate
        years_to_maturity = 10
        ytm = 0.06  # 6% yield to maturity
        
        # Calculate bond price
        coupon_pv = sum([annual_coupon / (1 + ytm)**t for t in range(1, years_to_maturity + 1)])
        face_pv = face_value / (1 + ytm)**years_to_maturity
        bond_price = coupon_pv + face_pv
        
        print(f"\n   Bond Characteristics:")
        print(f"   Face Value: ${face_value:,.0f}")
        print(f"   Coupon Rate: {coupon_rate:.1%} (${annual_coupon:,.0f} annually)")
        print(f"   Years to Maturity: {years_to_maturity}")
        print(f"   Yield to Maturity: {ytm:.1%}")
        
        print(f"\n   Valuation Calculation:")
        print(f"   PV of Coupons: ${coupon_pv:,.2f}")
        print(f"   PV of Face Value: ${face_pv:,.2f}")
        
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  Bond Price: ${bond_price:>21,.2f}  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        if bond_price < face_value:
            discount = face_value - bond_price
            print(f"\n   💡 Bond trades at DISCOUNT: ${discount:.2f} below par")
            print(f"      YTM ({ytm:.1%}) > Coupon Rate ({coupon_rate:.1%})")
        else:
            premium = bond_price - face_value
            print(f"\n   💡 Bond trades at PREMIUM: ${premium:.2f} above par")
            print(f"      YTM ({ytm:.1%}) < Coupon Rate ({coupon_rate:.1%})")
        
        # Interest rate sensitivity
        print(f"\n📊 Interest Rate Sensitivity")
        print("-" * 70)
        
        print(f"\n   Impact of YTM changes on bond price:\n")
        ytm_scenarios = [0.04, 0.05, 0.06, 0.07, 0.08]
        
        for ytm_test in ytm_scenarios:
            coupon_pv_test = sum([annual_coupon / (1 + ytm_test)**t for t in range(1, years_to_maturity + 1)])
            face_pv_test = face_value / (1 + ytm_test)**years_to_maturity
            price_test = coupon_pv_test + face_pv_test
            change_pct = ((price_test - bond_price) / bond_price) * 100
            marker = " ← Current" if ytm_test == ytm else ""
            print(f"   YTM {ytm_test:.1%}: Price = ${price_test:>7.2f} ({change_pct:>+6.2f}%){marker}")
        
        print(f"\n   💡 Bond prices and yields move inversely!")
        print(f"      1% rate increase → ~7-8% price decrease\n")
    
    def dividend_discount_model(self):
        """Stock valuation using Dividend Discount Model"""
        print("="*70)
        print("COMPONENT 4: DIVIDEND DISCOUNT MODEL (DDM) FOR NVIDIA")
        print("="*70 + "\n")
        
        print("📊 Gordon Growth Model")
        print("-" * 70)
        
        # Get dividend data
        dividends = self.nvda.dividends
        
        if len(dividends) > 0:
            # Calculate dividend metrics
            recent_dividends = dividends.tail(4)
            annual_dividend = recent_dividends.sum()
            
            # Estimate growth rate from historical dividends
            if len(dividends) >= 8:
                old_div = dividends.iloc[-8:-4].sum()
                new_div = dividends.iloc[-4:].sum()
                growth_rate = (new_div / old_div) ** (1/1) - 1
            else:
                growth_rate = 0.05  # Assume 5% growth
            
            # Required return (CAPM-style)
            required_return = self.risk_free_rate + 0.08  # Risk-free + premium
            
            # Gordon Growth Model
            if required_return > growth_rate:
                intrinsic_value = (annual_dividend * (1 + growth_rate)) / (required_return - growth_rate)
            else:
                intrinsic_value = None
                print(f"\n   ⚠️  Growth rate ({growth_rate:.2%}) ≥ Required return ({required_return:.2%})")
                print(f"      Gordon model not applicable. Using multi-stage model...\n")
                
                # Two-stage model
                high_growth_years = 5
                stable_growth = 0.04
                
                # Stage 1: High growth dividends
                pv_stage1 = sum([(annual_dividend * (1 + growth_rate)**t) / (1 + required_return)**t 
                                for t in range(1, high_growth_years + 1)])
                
                # Stage 2: Stable growth
                terminal_dividend = annual_dividend * (1 + growth_rate)**high_growth_years * (1 + stable_growth)
                terminal_value = terminal_dividend / (required_return - stable_growth)
                pv_terminal = terminal_value / (1 + required_return)**high_growth_years
                
                intrinsic_value = pv_stage1 + pv_terminal
        else:
            # NVIDIA pays minimal dividends, use alternative approach
            print(f"\n   ⚠️  NVIDIA pays minimal dividends")
            print(f"      Using Free Cash Flow to Equity (FCFE) model instead\n")
            
            annual_dividend = 0.20  # Estimated minimal dividend
            growth_rate = 0.15  # High growth tech company
            required_return = 0.12
            stable_growth = 0.04
            
            # Two-stage DDM
            high_growth_years = 10
            
            pv_stage1 = sum([(annual_dividend * (1 + growth_rate)**t) / (1 + required_return)**t 
                            for t in range(1, high_growth_years + 1)])
            
            terminal_dividend = annual_dividend * (1 + growth_rate)**high_growth_years * (1 + stable_growth)
            terminal_value = terminal_dividend / (required_return - stable_growth)
            pv_terminal = terminal_value / (1 + required_return)**high_growth_years
            
            intrinsic_value = pv_stage1 + pv_terminal
        
        # Get current market price
        current_price = self.nvda_data['Adj Close'].iloc[-1]
        
        print(f"\n   Model Parameters:")
        print(f"   Current Annual Dividend: ${annual_dividend:.2f}")
        print(f"   Growth Rate (g): {growth_rate:.2%}")
        print(f"   Required Return (r): {required_return:.2%}")
        
        if intrinsic_value:
            print(f"\n   ╔══════════════════════════════════════════╗")
            print(f"   ║  Intrinsic Value: ${intrinsic_value:>19,.2f}  ║")
            print(f"   ╚══════════════════════════════════════════╝")
            
            print(f"\n   Current Market Price: ${current_price:,.2f}")
            
            if intrinsic_value > current_price:
                upside = ((intrinsic_value - current_price) / current_price) * 100
                print(f"   💡 UNDERVALUED by {upside:.1f}% → BUY signal")
            elif intrinsic_value < current_price:
                downside = ((current_price - intrinsic_value) / current_price) * 100
                print(f"   💡 OVERVALUED by {downside:.1f}% → SELL signal")
            else:
                print(f"   💡 FAIRLY VALUED → HOLD")
        
        print(f"\n   ⚠️  Note: NVIDIA is a growth stock with low dividend yield.")
        print(f"      Other valuation methods (P/E, DCF) may be more appropriate.\n")
    
    def loan_amortization(self):
        """Loan amortization schedule"""
        print("="*70)
        print("COMPONENT 5: LOAN AMORTIZATION ANALYSIS")
        print("="*70 + "\n")
        
        print("📊 Mortgage Amortization Example")
        print("-" * 70)
        
        # Loan parameters
        principal = 500000  # $500K home
        annual_rate = 0.065  # 6.5% APR
        monthly_rate = annual_rate / 12
        years = 30
        n_payments = years * 12
        
        # Calculate monthly payment
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / \
                         ((1 + monthly_rate)**n_payments - 1)
        
        print(f"\n   Loan Amount: ${principal:,.0f}")
        print(f"   Annual Interest Rate: {annual_rate:.2%}")
        print(f"   Loan Term: {years} years ({n_payments} months)")
        
        print(f"\n   ╔═══════════════════════════════════════════════╗")
        print(f"   ║  Monthly Payment: ${monthly_payment:>24,.2f}  ║")
        print(f"   ╚═══════════════════════════════════════════════╝")
        
        total_paid = monthly_payment * n_payments
        total_interest = total_paid - principal
        
        print(f"\n   Total Amount Paid: ${total_paid:,.2f}")
        print(f"   Total Interest Paid: ${total_interest:,.2f}")
        print(f"   Interest as % of Principal: {(total_interest/principal)*100:.1f}%")
        
        # Show first few months
        print(f"\n   Amortization Schedule (First 6 Months):")
        print(f"   {'Month':<8} {'Payment':<12} {'Principal':<12} {'Interest':<12} {'Balance':<12}")
        print(f"   {'-'*66}")
        
        balance = principal
        for month in range(1, 7):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            
            print(f"   {month:<8} ${monthly_payment:<11,.2f} ${principal_payment:<11,.2f} "
                  f"${interest_payment:<11,.2f} ${balance:<11,.2f}")
        
        print(f"\n   💡 Early payments are mostly interest!")
        print(f"      Month 1: ${principal_payment:.2f} principal vs ${interest_payment:.2f} interest\n")
        
        # Early payment impact
        print(f"📊 Impact of Extra Payments")
        print("-" * 70)
        
        extra_payment = 200  # $200 extra per month
        new_monthly = monthly_payment + extra_payment
        
        # Calculate new payoff time
        balance = principal
        months_to_payoff = 0
        total_paid_with_extra = 0
        
        while balance > 0 and months_to_payoff < n_payments:
            months_to_payoff += 1
            interest_payment = balance * monthly_rate
            principal_payment = new_monthly - interest_payment
            
            if principal_payment > balance:
                principal_payment = balance
                new_monthly = interest_payment + principal_payment
            
            balance -= principal_payment
            total_paid_with_extra += new_monthly
        
        years_saved = (n_payments - months_to_payoff) / 12
        interest_saved = total_paid - total_paid_with_extra
        
        print(f"\n   With ${extra_payment:,.0f} extra monthly payment:")
        print(f"   New Monthly Payment: ${new_monthly:.2f}")
        print(f"   Payoff Time: {months_to_payoff/12:.1f} years ({months_to_payoff} months)")
        print(f"   Time Saved: {years_saved:.1f} years")
        print(f"   Interest Saved: ${interest_saved:,.2f}")
        
        print(f"\n   💡 Extra ${extra_payment:,.0f}/month saves ${interest_saved:,.2f} in interest!\n")
    
    def sensitivity_analysis(self):
        """Comprehensive sensitivity analysis"""
        print("="*70)
        print("SENSITIVITY ANALYSIS")
        print("="*70 + "\n")
        
        print("📊 Interest Rate Sensitivity on $100,000 Investment")
        print("-" * 70)
        
        principal = 100000
        years = 10
        
        print(f"\n   Investment: ${principal:,.0f} for {years} years\n")
        
        rates = [0.04, 0.06, 0.08, 0.10, 0.12]
        for rate in rates:
            fv = principal * (1 + rate)**years
            total_return = fv - principal
            print(f"   Rate {rate:.1%}: FV = ${fv:>12,.2f}  |  Return = ${total_return:>12,.2f}")
        
        print(f"\n   💡 2% rate difference → ${(100000*1.08**10 - 100000*1.06**10):,.2f} difference in wealth!\n")
        
        print("📊 Time Horizon Impact")
        print("-" * 70)
        
        rate = 0.08
        print(f"\n   Investment: ${principal:,.0f} at {rate:.1%}\n")
        
        time_periods = [5, 10, 15, 20, 25, 30]
        for years in time_periods:
            fv = principal * (1 + rate)**years
            multiple = fv / principal
            print(f"   {years:2d} years: ${fv:>12,.2f}  |  {multiple:.2f}x return")
        
        print(f"\n   💡 Time is your greatest ally in wealth building!\n")
    
    def generate_summary_report(self):
        """Generate comprehensive TVM summary"""
        print("\n" + "="*70)
        print("TIME VALUE OF MONEY ANALYSIS SUMMARY")
        print("="*70 + "\n")
        
        print(f"🏢 Analysis Focus: NVIDIA Corporation")
        print(f"📅 Report Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"💰 Financial Instruments: NVDA stock, TLT, LQD, SPY\n")
        
        current_price = self.nvda_data['Adj Close'].iloc[-1]
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                      TVM ANALYSIS SUMMARY                     ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(f"║  Current NVIDIA Price: ${current_price:>37,.2f}  ║")
        print(f"║  Risk-Free Rate: {self.risk_free_rate:>44.2%}  ║")
        print("║                                                              ║")
        print("║  Key Applications Demonstrated:                              ║")
        print("║    • Present & Future Value Calculations                     ║")
        print("║    • Annuity Valuation & Retirement Planning                 ║")
        print("║    • Bond Pricing & Interest Rate Sensitivity                ║")
        print("║    • Dividend Discount Model (Multi-stage)                   ║")
        print("║    • Loan Amortization & Prepayment Analysis                 ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")
        
        print("🎯 Key Insights:\n")
        
        print("   Time Value Principles:")
        print("   • Money today is worth more than money tomorrow")
        print("   • Compound interest is the 8th wonder of the world")
        print("   • Interest rates dramatically impact investment outcomes")
        
        print("\n   Investment Applications:")
        print("   • Use PV/FV for single cash flow decisions")
        print("   • Apply annuity formulas for recurring payments")
        print("   • Bond valuation shows inverse price-yield relationship")
        print("   • DDM useful for dividend-paying stocks (limited for NVIDIA)")
        
        print("\n   Risk Management:")
        print("   • Diversify across assets (stocks, bonds, alternatives)")
        print("   • Longer time horizons reduce risk")
        print("   • Interest rate changes impact all valuations")
        print("   • Early loan payments save significant interest")
        
        print("\n💼 Recommendations for NVIDIA Investors:")
        print("   • Long-term hold leverages compound growth")
        print("   • Dollar-cost averaging reduces timing risk")
        print("   • Consider bonds for portfolio balance")
        print("   • Regular rebalancing maintains target allocation\n")


def main():
    """Main execution"""
    # Create analysis object
    tvm = TVMAnalysis()
    
    # Run all TVM analyses
    tvm.fundamental_tvm_calculations()
    tvm.annuity_analysis()
    tvm.bond_valuation()
    tvm.dividend_discount_model()
    tvm.loan_amortization()
    tvm.sensitivity_analysis()
    tvm.generate_summary_report()
    
    print("✅ Time Value of Money Analysis Complete!\n")


if __name__ == "__main__":
    main()
