#!/usr/bin/env python3
"""
Project 1: Generative AI Investment Analysis for NVIDIA
Capital Budgeting Methods, Real Options, and Monte Carlo Simulation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import yfinance as yf
from datetime import datetime, timedelta

class AIInvestmentAnalysis:
    """AI Investment Analysis using Capital Budgeting Methods"""
    
    def __init__(self, company_ticker="NVDA"):
        self.ticker = company_ticker
        self.stock = yf.Ticker(company_ticker)
        self.setup_project_parameters()
        
    def setup_project_parameters(self):
        """Setup AI investment project parameters"""
        print("\n" + "="*70)
        print("PROJECT 1: GENERATIVE AI INVESTMENT ANALYSIS FOR NVIDIA")
        print("="*70 + "\n")
        
        # Download financial data
        print("📥 Downloading NVIDIA financial data...")
        self.cashflow = self.stock.cashflow
        
        # Calculate FCF
        try:
            operating_cf = self.cashflow.iloc[0, 0] if len(self.cashflow) > 0 else 50e9
            capex = abs(self.cashflow.iloc[1, 0]) if len(self.cashflow) > 1 else operating_cf * 0.1
            self.fcf = operating_cf - capex
        except:
            self.fcf = 50e9  # Default estimate for NVIDIA
        
        # Project parameters
        self.initial_investment = self.fcf * 0.01  # 1% of FCF
        self.project_life = 5  # years
        self.ai_efficiency_factor = 0.35  # NVIDIA is a tech leader
        self.annual_cash_flow = self.initial_investment * self.ai_efficiency_factor
        self.discount_rate = 0.12  # 12% for tech companies
        self.risk_free_rate = 0.045  # 4.5% current rate
        
        print(f"✅ AI Investment Project Parameters:")
        print(f"   Company Free Cash Flow: ${self.fcf/1e9:.2f} billion")
        print(f"   Initial Investment (1% of FCF): ${self.initial_investment/1e6:.2f} million")
        print(f"   AI Efficiency Factor: {self.ai_efficiency_factor:.1%}")
        print(f"   Expected Annual Cash Flow: ${self.annual_cash_flow/1e6:.2f} million")
        print(f"   Project Life: {self.project_life} years")
        print(f"   Discount Rate: {self.discount_rate:.1%}")
        print(f"\n   AI Project Scope: Generative AI for chip design automation,")
        print(f"   customer service, and software development acceleration\n")
    
    def calculate_npv(self):
        """Calculate Net Present Value"""
        print("📊 Method 1: NET PRESENT VALUE (NPV)")
        print("-" * 70)
        
        # Calculate present value of cash flows
        cash_flows = [self.annual_cash_flow] * self.project_life
        years = np.arange(1, self.project_life + 1)
        
        pv_cash_flows = [cf / (1 + self.discount_rate)**year 
                        for year, cf in zip(years, cash_flows)]
        
        total_pv = sum(pv_cash_flows)
        npv = total_pv - self.initial_investment
        
        self.npv = npv
        
        print(f"\n   Formula: NPV = Σ[CFt / (1+r)^t] - Initial Investment")
        print(f"\n   Calculation:")
        for year in years:
            pv = cash_flows[year-1] / (1 + self.discount_rate)**year
            print(f"   Year {year}: ${cash_flows[year-1]/1e6:.2f}M / (1.12)^{year} = ${pv/1e6:.2f}M")
        
        print(f"\n   Total PV of Cash Flows: ${total_pv/1e6:.2f} million")
        print(f"   Initial Investment: ${self.initial_investment/1e6:.2f} million")
        print(f"   ╔══════════════════════════════════════╗")
        print(f"   ║  NET PRESENT VALUE: ${npv/1e6:>13.2f}M  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        if npv > 0:
            print(f"\n   ✅ Decision: ACCEPT - Project creates value (NPV > 0)")
        else:
            print(f"\n   ❌ Decision: REJECT - Project destroys value (NPV < 0)")
        
        print(f"\n   Advantages for AI Projects:")
        print(f"   • Accounts for time value of money")
        print(f"   • Measures absolute value creation")
        print(f"   • Considers all cash flows over project life")
        
        print(f"\n   Limitations for AI Projects:")
        print(f"   • Doesn't capture strategic flexibility")
        print(f"   • Single discount rate may not reflect AI risks")
        print(f"   • Ignores learning and pivot options\n")
        
        return npv
    
    def calculate_irr(self):
        """Calculate Internal Rate of Return"""
        print("📊 Method 2: INTERNAL RATE OF RETURN (IRR)")
        print("-" * 70)
        
        # Create cash flow array
        cash_flows = [-self.initial_investment]
        cash_flows.extend([self.annual_cash_flow] * self.project_life)
        
        # Calculate IRR using numpy-financial
        try:
            import numpy_financial as npf
            irr = npf.irr(cash_flows)
        except ImportError:
            # Fallback: manual IRR calculation using Newton's method
            def npv_at_rate(rate):
                return sum([cf / (1 + rate)**i for i, cf in enumerate(cash_flows)])
            
            # Binary search for IRR
            low, high = -0.5, 1.0
            for _ in range(100):
                mid = (low + high) / 2
                npv = npv_at_rate(mid)
                if abs(npv) < 1:
                    break
                if npv > 0:
                    low = mid
                else:
                    high = mid
            irr = mid
        
        self.irr = irr
        
        print(f"\n   Formula: Find r where NPV = 0")
        print(f"   0 = -Initial Investment + Σ[CFt / (1+IRR)^t]")
        print(f"\n   Cash Flows:")
        print(f"   Year 0: -${self.initial_investment/1e6:.2f}M (Initial Investment)")
        for year in range(1, self.project_life + 1):
            print(f"   Year {year}: ${self.annual_cash_flow/1e6:.2f}M")
        
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  INTERNAL RATE OF RETURN: {irr:>9.2%}  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        print(f"\n   Hurdle Rate (Discount Rate): {self.discount_rate:.2%}")
        
        if irr > self.discount_rate:
            print(f"   ✅ Decision: ACCEPT - IRR ({irr:.2%}) > Hurdle Rate ({self.discount_rate:.2%})")
        else:
            print(f"   ❌ Decision: REJECT - IRR ({irr:.2%}) < Hurdle Rate ({self.discount_rate:.2%})")
        
        print(f"\n   Advantages for AI Projects:")
        print(f"   • Easy to understand and communicate")
        print(f"   • Doesn't require explicit discount rate")
        print(f"   • Good for ranking AI projects")
        
        print(f"\n   Limitations for AI Projects:")
        print(f"   • May have multiple IRRs with non-conventional cash flows")
        print(f"   • Assumes reinvestment at IRR (unrealistic for AI)")
        print(f"   • Scale-independent (doesn't show absolute value)\n")
        
        return irr
    
    def calculate_payback_period(self):
        """Calculate Payback Period"""
        print("📊 Method 3: PAYBACK PERIOD")
        print("-" * 70)
        
        cumulative_cf = 0
        payback_period = 0
        
        print(f"\n   Formula: Time to recover initial investment")
        print(f"\n   Cumulative Cash Flow Analysis:")
        print(f"   Year 0: -${self.initial_investment/1e6:.2f}M")
        
        for year in range(1, self.project_life + 1):
            cumulative_cf += self.annual_cash_flow
            print(f"   Year {year}: ${cumulative_cf/1e6:.2f}M cumulative")
            
            if cumulative_cf >= self.initial_investment and payback_period == 0:
                # Calculate exact payback with interpolation
                previous_cf = cumulative_cf - self.annual_cash_flow
                remaining = self.initial_investment - previous_cf
                fraction = remaining / self.annual_cash_flow
                payback_period = (year - 1) + fraction
        
        self.payback_period = payback_period
        
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  PAYBACK PERIOD: {payback_period:>16.2f} years  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        target_payback = 3  # 3 years for tech projects
        if payback_period <= target_payback:
            print(f"\n   ✅ Decision: ACCEPT - Payback ({payback_period:.2f} yrs) ≤ Target ({target_payback} yrs)")
        else:
            print(f"\n   ⚠️  Decision: CAUTION - Payback ({payback_period:.2f} yrs) > Target ({target_payback} yrs)")
        
        print(f"\n   Advantages for AI Projects:")
        print(f"   • Simple and intuitive")
        print(f"   • Focuses on risk and liquidity")
        print(f"   • Good for high-uncertainty AI projects")
        
        print(f"\n   Limitations for AI Projects:")
        print(f"   • Ignores cash flows after payback")
        print(f"   • Doesn't consider time value of money")
        print(f"   • Arbitrary cutoff period\n")
        
        return payback_period
    
    def calculate_profitability_index(self):
        """Calculate Profitability Index"""
        print("📊 Method 4: PROFITABILITY INDEX (PI)")
        print("-" * 70)
        
        # Calculate PV of future cash flows
        years = np.arange(1, self.project_life + 1)
        pv_inflows = sum([self.annual_cash_flow / (1 + self.discount_rate)**year 
                         for year in years])
        
        pi = pv_inflows / self.initial_investment
        self.pi = pi
        
        print(f"\n   Formula: PI = PV of Future Cash Flows / Initial Investment")
        print(f"\n   PV of Future Cash Flows: ${pv_inflows/1e6:.2f}M")
        print(f"   Initial Investment: ${self.initial_investment/1e6:.2f}M")
        
        print(f"\n   ╔══════════════════════════════════════╗")
        print(f"   ║  PROFITABILITY INDEX: {pi:>15.3f}  ║")
        print(f"   ╚══════════════════════════════════════╝")
        
        if pi > 1:
            print(f"\n   ✅ Decision: ACCEPT - PI ({pi:.3f}) > 1.0")
            print(f"   💡 Every $1 invested returns ${pi:.2f}")
        else:
            print(f"\n   ❌ Decision: REJECT - PI ({pi:.3f}) < 1.0")
        
        print(f"\n   Advantages for AI Projects:")
        print(f"   • Good for capital rationing situations")
        print(f"   • Considers time value of money")
        print(f"   • Useful for ranking AI projects")
        
        print(f"\n   Limitations for AI Projects:")
        print(f"   • Doesn't show absolute value creation")
        print(f"   • May favor small AI projects over large ones")
        print(f"   • Doesn't capture AI-specific flexibilities\n")
        
        return pi
    
    def sensitivity_analysis(self):
        """Perform sensitivity analysis on key variables"""
        print("=" * 70)
        print("SENSITIVITY ANALYSIS FOR AI PROJECT")
        print("=" * 70 + "\n")
        
        # Variables to analyze
        base_npv = self.npv
        
        print("📈 Testing sensitivity to key AI variables:\n")
        
        # 1. AI Efficiency Factor sensitivity
        print("1. AI Efficiency Factor (Annual Cash Flow Impact)")
        efficiency_range = np.linspace(0.20, 0.50, 7)
        for eff in efficiency_range:
            annual_cf = self.initial_investment * eff
            pv = sum([annual_cf / (1 + self.discount_rate)**year 
                     for year in range(1, self.project_life + 1)])
            npv = pv - self.initial_investment
            marker = " ← BASE" if abs(eff - self.ai_efficiency_factor) < 0.01 else ""
            print(f"   Efficiency {eff:.1%}: NPV = ${npv/1e6:>8.2f}M{marker}")
        
        # 2. Discount rate sensitivity
        print(f"\n2. Discount Rate (Risk Premium)")
        discount_range = np.linspace(0.08, 0.16, 9)
        for disc in discount_range:
            pv = sum([self.annual_cash_flow / (1 + disc)**year 
                     for year in range(1, self.project_life + 1)])
            npv = pv - self.initial_investment
            marker = " ← BASE" if abs(disc - self.discount_rate) < 0.005 else ""
            print(f"   Discount Rate {disc:.1%}: NPV = ${npv/1e6:>8.2f}M{marker}")
        
        # 3. Project life sensitivity
        print(f"\n3. Project Life (Technology Refresh Cycle)")
        for life in [3, 4, 5, 6, 7]:
            pv = sum([self.annual_cash_flow / (1 + self.discount_rate)**year 
                     for year in range(1, life + 1)])
            npv = pv - self.initial_investment
            marker = " ← BASE" if life == self.project_life else ""
            print(f"   Project Life {life} years: NPV = ${npv/1e6:>8.2f}M{marker}")
        
        print(f"\n💡 Key Insights:")
        print(f"   • NPV is most sensitive to AI efficiency factor")
        print(f"   • Discount rate significantly impacts project value")
        print(f"   • Longer project life adds substantial value\n")
    
    def real_options_analysis(self):
        """Real Options Analysis - Binomial Model for AI Expansion"""
        print("=" * 70)
        print("REAL OPTIONS ANALYSIS: AI EXPANSION OPTION")
        print("=" * 70 + "\n")
        
        print("📊 Valuing the option to expand AI deployment across NVIDIA\n")
        
        # Option parameters
        S0 = self.npv if self.npv > 0 else self.initial_investment * 0.5  # Current project value
        K = self.initial_investment * 1.5  # Expansion investment
        T = 2  # 2 years to decide
        sigma = 0.50  # 50% volatility for AI projects
        r = self.risk_free_rate
        N = 4  # Quarterly periods
        
        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
        
        print(f"Option Parameters:")
        print(f"   Current AI Project Value (S0): ${S0/1e6:.2f}M")
        print(f"   Expansion Investment (K): ${K/1e6:.2f}M")
        print(f"   Time to Decision: {T} years")
        print(f"   Volatility (σ): {sigma:.1%}")
        print(f"   Risk-free Rate: {r:.2%}")
        print(f"   Periods: {N} (quarterly)")
        print(f"\n   Binomial Parameters:")
        print(f"   Up factor (u): {u:.4f}")
        print(f"   Down factor (d): {d:.4f}")
        print(f"   Risk-neutral probability (p): {p:.4f}\n")
        
        # Build binomial tree for underlying
        asset_values = np.zeros((N + 1, N + 1))
        for i in range(N + 1):
            for j in range(i + 1):
                asset_values[j, i] = S0 * (u ** (i - j)) * (d ** j)
        
        # Calculate option values (expansion option)
        option_values = np.zeros((N + 1, N + 1))
        
        # Terminal values - option to expand by 2x
        expansion_factor = 2.0
        for j in range(N + 1):
            expanded_value = asset_values[j, N] * expansion_factor
            option_values[j, N] = max(expanded_value - K, 0)
        
        # Backward induction
        for i in range(N - 1, -1, -1):
            for j in range(i + 1):
                hold_value = np.exp(-r * dt) * (p * option_values[j, i + 1] + 
                                                (1 - p) * option_values[j + 1, i + 1])
                expanded_value = asset_values[j, i] * expansion_factor
                exercise_value = max(expanded_value - K, 0)
                option_values[j, i] = max(hold_value, exercise_value)
        
        expansion_option_value = option_values[0, 0]
        
        print(f"╔══════════════════════════════════════════════════╗")
        print(f"║  EXPANSION OPTION VALUE: ${expansion_option_value/1e6:>19.2f}M  ║")
        print(f"╚══════════════════════════════════════════════════╝\n")
        
        # Expanded NPV
        traditional_npv = self.npv
        expanded_npv = traditional_npv + expansion_option_value
        
        print(f"Value Comparison:")
        print(f"   Traditional NPV: ${traditional_npv/1e6:>10.2f}M")
        print(f"   + Expansion Option: ${expansion_option_value/1e6:>10.2f}M")
        print(f"   ─────────────────────────────────")
        print(f"   Expanded NPV: ${expanded_npv/1e6:>10.2f}M")
        print(f"\n   💡 Real Options add {(expansion_option_value/traditional_npv*100):.1f}% to project value!\n")
        
        print(f"Strategic Insights:")
        print(f"   • Flexibility to expand has significant value")
        print(f"   • Staged AI implementation reduces risk")
        print(f"   • Option value justifies pilot approach")
        print(f"   • Decision points at quarters 2, 4, 6, 8\n")
        
        return expansion_option_value
    
    def monte_carlo_simulation(self, n_simulations=10000):
        """Monte Carlo Simulation for AI Project NPV"""
        print("=" * 70)
        print("MONTE CARLO SIMULATION: AI PROJECT RISK ANALYSIS")
        print("=" * 70 + "\n")
        
        print(f"🎲 Running {n_simulations:,} simulations...\n")
        
        np.random.seed(42)
        npv_simulations = []
        
        for _ in range(n_simulations):
            # Simulate uncertain variables
            efficiency = np.random.normal(0.35, 0.10)  # Mean 35%, std 10%
            efficiency = max(0.15, min(0.60, efficiency))  # Bound between 15-60%
            
            discount = np.random.uniform(0.10, 0.15)  # Uniform 10-15%
            
            project_life = np.random.choice([3, 5, 7], p=[0.2, 0.5, 0.3])
            
            initial_inv = self.initial_investment * np.random.uniform(0.8, 1.2)
            
            # Calculate NPV for this simulation
            annual_cf = initial_inv * efficiency
            pv = sum([annual_cf / (1 + discount)**year 
                     for year in range(1, project_life + 1)])
            npv = pv - initial_inv
            
            npv_simulations.append(npv)
        
        npv_simulations = np.array(npv_simulations)
        
        # Calculate statistics
        mean_npv = np.mean(npv_simulations)
        std_npv = np.std(npv_simulations)
        prob_positive = np.sum(npv_simulations > 0) / n_simulations
        var_5 = np.percentile(npv_simulations, 5)
        ci_90_low = np.percentile(npv_simulations, 5)
        ci_90_high = np.percentile(npv_simulations, 95)
        
        print(f"📊 Simulation Results:")
        print(f"   Mean NPV: ${mean_npv/1e6:.2f}M")
        print(f"   Standard Deviation: ${std_npv/1e6:.2f}M")
        print(f"   Probability of Success (NPV > 0): {prob_positive:.1%}")
        print(f"   Value at Risk (5th percentile): ${var_5/1e6:.2f}M")
        print(f"   90% Confidence Interval: [${ci_90_low/1e6:.2f}M, ${ci_90_high/1e6:.2f}M]\n")
        
        # Risk assessment
        if prob_positive >= 0.70:
            print(f"   ✅ LOW RISK: {prob_positive:.1%} probability of success")
        elif prob_positive >= 0.50:
            print(f"   ⚠️  MODERATE RISK: {prob_positive:.1%} probability of success")
        else:
            print(f"   ❌ HIGH RISK: {prob_positive:.1%} probability of success")
        
        print(f"\n💡 Risk Insights:")
        print(f"   • Expected value: ${mean_npv/1e6:.2f}M")
        print(f"   • Worst case (5%): ${var_5/1e6:.2f}M")
        print(f"   • Best case (95%): ${ci_90_high/1e6:.2f}M")
        print(f"   • Risk-adjusted return is favorable for NVIDIA\n")
        
        # Create visualization
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        ax1.hist(npv_simulations/1e6, bins=50, edgecolor='black', alpha=0.7)
        ax1.axvline(mean_npv/1e6, color='red', linestyle='--', linewidth=2, label=f'Mean: ${mean_npv/1e6:.2f}M')
        ax1.axvline(0, color='green', linestyle='--', linewidth=2, label='Break-even')
        ax1.set_xlabel('NPV ($ Millions)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Distribution of AI Project NPV\n(Monte Carlo Simulation)', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        # Cumulative probability
        sorted_npv = np.sort(npv_simulations/1e6)
        cumulative = np.arange(1, len(sorted_npv) + 1) / len(sorted_npv)
        ax2.plot(sorted_npv, cumulative, linewidth=2)
        ax2.axvline(0, color='green', linestyle='--', linewidth=2, label='Break-even')
        ax2.axhline(0.5, color='red', linestyle='--', alpha=0.5)
        ax2.set_xlabel('NPV ($ Millions)', fontsize=12)
        ax2.set_ylabel('Cumulative Probability', fontsize=12)
        ax2.set_title('Cumulative Distribution of NPV', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/home/runner/work/RSB/RSB/monte_carlo_npv.png', dpi=300, bbox_inches='tight')
        print(f"📊 Visualization saved: monte_carlo_npv.png\n")
        plt.close()
        
        return npv_simulations
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "=" * 70)
        print("COMPREHENSIVE AI INVESTMENT RECOMMENDATION")
        print("=" * 70 + "\n")
        
        print(f"🏢 Company: NVIDIA Corporation")
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"💡 Project: Generative AI for Design Automation & Operations\n")
        
        print(f"╔══════════════════════════════════════════════════════════════╗")
        print(f"║                   CAPITAL BUDGETING SUMMARY                  ║")
        print(f"╠══════════════════════════════════════════════════════════════╣")
        print(f"║  Net Present Value (NPV)    : ${self.npv/1e6:>23.2f}M      ║")
        print(f"║  Internal Rate of Return    : {self.irr:>24.2%}      ║")
        print(f"║  Payback Period             : {self.payback_period:>23.2f} years  ║")
        print(f"║  Profitability Index (PI)   : {self.pi:>28.3f}      ║")
        print(f"╚══════════════════════════════════════════════════════════════╝\n")
        
        # Decision matrix
        decisions = []
        if self.npv > 0:
            decisions.append("✅ NPV > 0: ACCEPT")
        else:
            decisions.append("❌ NPV < 0: REJECT")
            
        if self.irr > self.discount_rate:
            decisions.append(f"✅ IRR ({self.irr:.2%}) > Hurdle ({self.discount_rate:.2%}): ACCEPT")
        else:
            decisions.append(f"❌ IRR < Hurdle: REJECT")
            
        if self.payback_period <= 3:
            decisions.append(f"✅ Payback ({self.payback_period:.2f} yrs) ≤ 3 yrs: ACCEPT")
        else:
            decisions.append(f"⚠️  Payback > 3 years: CAUTION")
            
        if self.pi > 1:
            decisions.append(f"✅ PI ({self.pi:.3f}) > 1.0: ACCEPT")
        else:
            decisions.append(f"❌ PI < 1.0: REJECT")
        
        print(f"Decision Criteria:")
        for decision in decisions:
            print(f"   {decision}")
        
        # Final recommendation
        accept_count = sum(1 for d in decisions if "✅" in d)
        
        print(f"\n" + "=" * 70)
        if accept_count >= 3:
            print(f"🎯 FINAL RECOMMENDATION: ACCEPT THE AI INVESTMENT PROJECT")
            print(f"=" * 70)
            print(f"\n   All major criteria support project acceptance.")
            print(f"   The AI investment creates value for NVIDIA shareholders.")
        else:
            print(f"⚠️  FINAL RECOMMENDATION: REVIEW PROJECT PARAMETERS")
            print(f"=" * 70)
            print(f"\n   Mixed signals from different methods.")
            print(f"   Consider refining assumptions or project scope.")
        
        print(f"\n💼 Strategic Considerations:")
        print(f"   • NVIDIA's AI leadership position supports this investment")
        print(f"   • Generative AI aligns with core business strategy")
        print(f"   • First-mover advantage in AI chip design")
        print(f"   • Potential for significant competitive differentiation")
        print(f"   • Real options value adds flexibility")
        print(f"\n   Recommendation: Proceed with pilot phase, maintain expansion options\n")


def main():
    """Main execution"""
    # Create analysis object
    analysis = AIInvestmentAnalysis("NVDA")
    
    # Run all analyses
    analysis.calculate_npv()
    analysis.calculate_irr()
    analysis.calculate_payback_period()
    analysis.calculate_profitability_index()
    analysis.sensitivity_analysis()
    analysis.real_options_analysis()
    analysis.monte_carlo_simulation()
    analysis.generate_summary_report()
    
    print("\n✅ AI Investment Analysis Complete!")
    print("📄 Results saved and displayed above.\n")


if __name__ == "__main__":
    main()
