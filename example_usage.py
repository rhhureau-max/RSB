"""
Example Usage of FVG Backtest Strategy

This script demonstrates how to use the FVG backtester with the example data.
"""

from fvg_backtest_strategy import FVGBacktester

def example_with_csv():
    """Example 1: Load data from CSV file and run backtest"""
    print("=" * 80)
    print("EXAMPLE 1: Using CSV File")
    print("=" * 80)
    
    # Initialize backtester with CSV file
    backtester = FVGBacktester(data_path='example_nq_data.csv')
    
    # Run the backtest
    print("\nRunning backtest...")
    results = backtester.run_backtest()
    
    # Print statistics
    backtester.print_statistics()
    
    # Show first few trades
    if len(results) > 0:
        print("\n📋 Trade Results:")
        print(results.to_string())
        
        # Export results
        backtester.export_results('example_backtest_results.csv')
    else:
        print("\n⚠️  No trades were executed. This could mean:")
        print("   - No FVG was detected in the 08:30-09:00 window")
        print("   - No entry signal was generated after FVG detection")
        print("   - Try using more/different data")


def example_with_dataframe():
    """Example 2: Load data as DataFrame and run backtest"""
    import pandas as pd
    
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Using DataFrame")
    print("=" * 80)
    
    # Load data
    df = pd.read_csv('example_nq_data.csv')
    
    print(f"\nLoaded {len(df)} rows of data")
    print("\nData sample:")
    print(df.head())
    
    # Initialize backtester with DataFrame
    backtester = FVGBacktester(dataframe=df)
    
    # Run the backtest
    print("\nRunning backtest...")
    results = backtester.run_backtest()
    
    # Print statistics
    backtester.print_statistics()
    
    # Get statistics as dictionary for further processing
    stats = backtester.calculate_statistics()
    
    print("\n📊 Statistics Dictionary:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_with_custom_analysis():
    """Example 3: Run backtest and perform custom analysis"""
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Custom Analysis")
    print("=" * 80)
    
    # Run backtest
    backtester = FVGBacktester(data_path='example_nq_data.csv')
    results = backtester.run_backtest()
    
    if len(results) > 0:
        # Custom analysis on results
        print("\n🔍 Custom Analysis:")
        
        # Analyze by trade type
        long_trades = results[results['type'] == 'long']
        short_trades = results[results['type'] == 'short']
        
        print(f"\nLong Trades Analysis:")
        if len(long_trades) > 0:
            print(f"  Count: {len(long_trades)}")
            print(f"  Avg PnL: {long_trades['pnl_points'].mean():.2f} points")
            print(f"  Total PnL: {long_trades['pnl_points'].sum():.2f} points")
            print(f"  Win Rate: {len(long_trades[long_trades['pnl_points'] > 0]) / len(long_trades) * 100:.2f}%")
        else:
            print("  No long trades")
        
        print(f"\nShort Trades Analysis:")
        if len(short_trades) > 0:
            print(f"  Count: {len(short_trades)}")
            print(f"  Avg PnL: {short_trades['pnl_points'].mean():.2f} points")
            print(f"  Total PnL: {short_trades['pnl_points'].sum():.2f} points")
            print(f"  Win Rate: {len(short_trades[short_trades['pnl_points'] > 0]) / len(short_trades) * 100:.2f}%")
        else:
            print("  No short trades")
        
        # Analyze TP hit patterns
        print(f"\n🎯 Take Profit Analysis:")
        tp1_only = results[(results['tp1_hit']) & (~results['tp2_hit']) & (~results['tp3_hit'])]
        tp2_reached = results[(results['tp1_hit']) & (results['tp2_hit']) & (~results['tp3_hit'])]
        tp3_reached = results[(results['tp1_hit']) & (results['tp2_hit']) & (results['tp3_hit'])]
        
        print(f"  TP1 Only: {len(tp1_only)} trades ({len(tp1_only)/len(results)*100:.1f}%)")
        print(f"  TP2 Reached: {len(tp2_reached)} trades ({len(tp2_reached)/len(results)*100:.1f}%)")
        print(f"  TP3 Reached: {len(tp3_reached)} trades ({len(tp3_reached)/len(results)*100:.1f}%)")
        
        # Risk/Reward analysis
        print(f"\n⚖️  Risk/Reward Analysis:")
        avg_risk = results['risk_points'].mean()
        avg_pnl = results['pnl_points'].mean()
        print(f"  Average Risk per Trade: {avg_risk:.2f} points")
        print(f"  Average PnL per Trade: {avg_pnl:.2f} points")
        print(f"  Avg R-Multiple: {avg_pnl/avg_risk:.2f}R")


if __name__ == "__main__":
    print("\n" + "🚀 FVG BACKTEST STRATEGY - EXAMPLE USAGE")
    print("=" * 80)
    print("\nThis script demonstrates different ways to use the FVG backtester.")
    print("Make sure you have 'example_nq_data.csv' in the same directory.")
    print("\n" + "=" * 80)
    
    try:
        # Run all examples
        example_with_csv()
        example_with_dataframe()
        example_with_custom_analysis()
        
        print("\n\n" + "=" * 80)
        print("✅ All examples completed successfully!")
        print("=" * 80)
        
        print("\n📚 Next Steps:")
        print("  1. Replace 'example_nq_data.csv' with your actual NQ futures data")
        print("  2. Ensure data is in 1-minute timeframe")
        print("  3. Run the backtest on historical data (2018 - present)")
        print("  4. Analyze the results and optimize parameters")
        print("  5. Consider walk-forward analysis for validation")
        
    except FileNotFoundError:
        print("\n❌ ERROR: example_nq_data.csv not found!")
        print("   Make sure the file is in the same directory as this script.")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
