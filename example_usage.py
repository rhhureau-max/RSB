#!/usr/bin/env python3
"""
Example Usage of ICT Midnight Open Analysis Tool
=================================================

This script demonstrates how to use the ICT analysis tool programmatically.
"""

from ict_midnight_open_analysis import (
    load_and_prepare_data,
    identify_midnight_open,
    analyze_killzone_touches,
    calculate_statistics,
    create_visualization
)

def example_analysis(csv_path):
    """
    Example of using the ICT analysis functions programmatically.
    
    Parameters:
    -----------
    csv_path : str
        Path to your NQ data CSV file
    """
    print("="*60)
    print("EXAMPLE: Programmatic Usage of ICT Analysis")
    print("="*60)
    
    # Step 1: Load your data
    print("\n1. Loading data...")
    df = load_and_prepare_data(csv_path)
    print(f"   Loaded {len(df)} rows")
    
    # Step 2: Identify Midnight Opens
    print("\n2. Identifying Midnight Open prices...")
    mo_series = identify_midnight_open(df)
    print(f"   Found {len(mo_series)} Midnight Open prices")
    
    # Step 3: Analyze killzone touches
    print("\n3. Analyzing Killzone touches...")
    results_df = analyze_killzone_touches(df, mo_series)
    print(f"   Analyzed {len(results_df)} trading days")
    
    # Step 4: Calculate statistics
    print("\n4. Calculating statistics...")
    stats, day_stats = calculate_statistics(results_df)
    
    # Step 5: Access specific statistics
    print("\n5. Accessing specific results:")
    print(f"   - Success Rate: {stats['success_rate']:.2f}%")
    print(f"   - Total Days: {stats['total_days']}")
    print(f"   - Days with Touch: {stats['days_touched']}")
    
    # Step 6: Filter results for specific days
    print("\n6. Example: Filtering for Monday data only...")
    monday_data = results_df[results_df['DayName'] == 'Monday']
    monday_touches = monday_data['Touched'].sum()
    monday_total = len(monday_data)
    monday_rate = (monday_touches / monday_total * 100) if monday_total > 0 else 0
    print(f"   Monday Success Rate: {monday_rate:.2f}% ({monday_touches}/{monday_total})")
    
    # Step 7: Create visualization
    print("\n7. Creating visualization...")
    create_visualization(results_df, stats)
    
    print("\n" + "="*60)
    print("EXAMPLE COMPLETED")
    print("="*60)
    
    return results_df, stats


def filter_high_success_days(results_df, min_success_rate=70):
    """
    Example: Filter for days of week with high success rates.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        Results from analyze_killzone_touches
    min_success_rate : float
        Minimum success rate threshold (percentage)
    """
    print(f"\nFinding days with success rate >= {min_success_rate}%...")
    
    day_success = results_df.groupby('DayName').agg({
        'Touched': ['sum', 'count', 'mean']
    })
    
    day_success['rate'] = day_success[('Touched', 'mean')] * 100
    
    high_success_days = day_success[day_success['rate'] >= min_success_rate]
    
    print(f"\nDays of week with success rate >= {min_success_rate}%:")
    for day in high_success_days.index:
        rate = float(high_success_days.loc[day, 'rate'])
        touches = int(high_success_days.loc[day, ('Touched', 'sum')])
        total = int(high_success_days.loc[day, ('Touched', 'count')])
        print(f"  {day}: {rate:.2f}% ({touches}/{total})")
    
    return high_success_days


def main():
    """Main function to run examples."""
    # Use sample data if available
    csv_path = 'sample_NQ_M1_data.csv'
    
    print("Running example usage of ICT Midnight Open Analysis\n")
    
    try:
        # Run the full analysis
        results_df, stats = example_analysis(csv_path)
        
        # Example: Filter for high-success days
        high_success = filter_high_success_days(results_df, min_success_rate=70)
        
        # Example: Get recent results
        print("\n" + "="*60)
        print("Last 10 Trading Days:")
        print("="*60)
        recent = results_df.tail(10)[['Date', 'MO_Price', 'Touched', 'DayName']]
        for idx, row in recent.iterrows():
            touch_str = "✓ Touched" if row['Touched'] else "✗ Not touched"
            print(f"{row['Date']} ({row['DayName']:9s}): {touch_str} - MO: {row['MO_Price']:.2f}")
        
    except FileNotFoundError:
        print(f"\nERROR: File '{csv_path}' not found.")
        print("Please run generate_sample_nq_data.py first to create sample data:")
        print("  python generate_sample_nq_data.py")
        print("\nOr provide your own NQ data CSV file.")


if __name__ == "__main__":
    main()
