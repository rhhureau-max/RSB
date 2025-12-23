#!/usr/bin/env python3
"""
ICT Midnight Open Analysis Script for NQ Futures
=================================================

This script analyzes the probability of Nasdaq (NQ) futures returning to touch
the Midnight Open (MO) price during the London Killzone session.

Midnight Open (MO): The opening price at 23:00 Chicago time (11 PM)
London Killzone (KZ): The period from 01:00 to 05:00 Chicago time (1 AM - 5 AM)

The analysis calculates:
- Total number of trading days analyzed
- Number of days where the MO was touched during the KZ
- Success rate (percentage of days with MO touch)
- Distribution of touches by day of week

Author: Trading Analysis Script
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time
import pytz
import warnings
# Suppress only specific matplotlib warnings
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')


def load_and_prepare_data(csv_path):
    """
    Load CSV data and prepare it with proper datetime indexing.
    
    Parameters:
    -----------
    csv_path : str
        Path to the CSV file containing NQ futures data
        Expected columns: Date, Time, Open, High, Low, Close
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with DatetimeIndex in Chicago timezone
    """
    print(f"Loading data from: {csv_path}")
    
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Display initial data info
    print(f"Initial data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Combine Date and Time columns into a single datetime column
    # Handle various possible date/time formats
    if 'Date' in df.columns and 'Time' in df.columns:
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    elif 'date' in df.columns and 'time' in df.columns:
        df['DateTime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    elif 'Datetime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['Datetime'])
    elif 'datetime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['datetime'])
    else:
        raise ValueError("Could not find date/time columns in CSV")
    
    # Set DateTime as index
    df.set_index('DateTime', inplace=True)
    
    # Localize to Chicago timezone (US/Central)
    chicago_tz = pytz.timezone('US/Central')
    # If data is already timezone-aware, convert it; otherwise, localize it
    if df.index.tz is None:
        df.index = df.index.tz_localize(chicago_tz, ambiguous='NaT', nonexistent='NaT')
    else:
        df.index = df.index.tz_convert(chicago_tz)
    
    # Remove any NaT values that might have been created
    df = df[df.index.notna()]
    
    # Ensure required columns exist (case-insensitive)
    columns_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if col_lower == 'open':
            columns_map['Open'] = col
        elif col_lower == 'high':
            columns_map['High'] = col
        elif col_lower == 'low':
            columns_map['Low'] = col
        elif col_lower == 'close':
            columns_map['Close'] = col
    
    # Rename columns to standard names
    df = df.rename(columns={v: k for k, v in columns_map.items()})
    
    # Verify we have the required columns
    required_cols = ['Open', 'High', 'Low', 'Close']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Sort by datetime
    df = df.sort_index()
    
    # Remove duplicates
    df = df[~df.index.duplicated(keep='first')]
    
    print(f"Data prepared successfully. Shape: {df.shape}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    
    return df[['Open', 'High', 'Low', 'Close']]


def identify_midnight_open(df):
    """
    Identify the Midnight Open (MO) price for each trading day.
    MO is defined as the opening price at 23:00 Chicago time.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with DatetimeIndex in Chicago timezone
        
    Returns:
    --------
    pd.Series
        Series with date as index and MO price as values
    """
    print("\nIdentifying Midnight Open prices (23:00 Chicago time)...")
    
    # Filter for 23:00 (11 PM) Chicago time
    midnight_opens = df[df.index.time == time(23, 0)]
    
    # Create a series with the date as index and the Open price as value
    mo_series = midnight_opens['Open'].copy()
    mo_series.index = mo_series.index.date
    
    print(f"Found {len(mo_series)} Midnight Open prices")
    
    return mo_series


def analyze_killzone_touches(df, mo_series):
    """
    Analyze if the Midnight Open price was touched during the London Killzone.
    Killzone: 01:00 to 05:00 Chicago time (inclusive of 01:00, exclusive of 05:00)
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with DatetimeIndex in Chicago timezone
    mo_series : pd.Series
        Series with date as index and MO price as values
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with analysis results per day
    """
    print("\nAnalyzing Killzone touches (01:00-05:00 Chicago time)...")
    
    results = []
    
    for date, mo_price in mo_series.items():
        # Get the next day's date for the killzone
        next_day = pd.Timestamp(date) + pd.Timedelta(days=1)
        
        # Define killzone period: 01:00 to 05:00 on the next day
        kz_start = pd.Timestamp(next_day.date()).replace(hour=1, minute=0, tzinfo=df.index.tz)
        kz_end = pd.Timestamp(next_day.date()).replace(hour=5, minute=0, tzinfo=df.index.tz)
        
        # Filter data for the killzone period
        kz_data = df[(df.index >= kz_start) & (df.index < kz_end)]
        
        # Check if we have data for this killzone
        if len(kz_data) == 0:
            continue
        
        # Check if any candle touched the MO price
        # Touch condition: Low <= MO <= High
        touched = ((kz_data['Low'] <= mo_price) & (kz_data['High'] >= mo_price)).any()
        
        # Get day of week (0=Monday, 6=Sunday)
        day_of_week = pd.Timestamp(date).dayofweek
        day_name = pd.Timestamp(date).day_name()
        
        results.append({
            'Date': date,
            'MO_Price': mo_price,
            'Touched': touched,
            'DayOfWeek': day_of_week,
            'DayName': day_name,
            'KZ_Candles': len(kz_data)
        })
    
    results_df = pd.DataFrame(results)
    
    print(f"Analyzed {len(results_df)} trading days")
    
    return results_df


def calculate_statistics(results_df):
    """
    Calculate and display statistics from the analysis.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with analysis results
        
    Returns:
    --------
    dict
        Dictionary containing statistical results
    """
    print("\n" + "="*60)
    print("STATISTICAL RESULTS")
    print("="*60)
    
    total_days = len(results_df)
    days_touched = results_df['Touched'].sum()
    success_rate = (days_touched / total_days * 100) if total_days > 0 else 0
    
    stats = {
        'total_days': total_days,
        'days_touched': days_touched,
        'days_not_touched': total_days - days_touched,
        'success_rate': success_rate
    }
    
    print(f"\nTotal Trading Days Analyzed: {total_days}")
    print(f"Days where MO was touched during KZ: {days_touched}")
    print(f"Days where MO was NOT touched during KZ: {total_days - days_touched}")
    print(f"\nSuccess Rate (MO Touch): {success_rate:.2f}%")
    
    # Statistics by day of week
    print("\n" + "-"*60)
    print("BREAKDOWN BY DAY OF WEEK")
    print("-"*60)
    
    day_stats = results_df.groupby('DayName').agg({
        'Touched': ['sum', 'count', 'mean']
    }).round(4)
    
    # Reorder by day of week
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_stats_ordered = pd.DataFrame()
    for day in day_order:
        if day in day_stats.index:
            day_stats_ordered = pd.concat([day_stats_ordered, day_stats.loc[[day]]])
    
    print("\nDay of Week Statistics:")
    for day in day_stats_ordered.index:
        total = int(day_stats_ordered.loc[day, ('Touched', 'count')])
        touched = int(day_stats_ordered.loc[day, ('Touched', 'sum')])
        rate = day_stats_ordered.loc[day, ('Touched', 'mean')] * 100
        print(f"{day:12s}: {touched:3d}/{total:3d} touches ({rate:5.2f}%)")
    
    print("\n" + "="*60)
    
    return stats, day_stats_ordered


def create_visualization(results_df, stats):
    """
    Create visualizations of the analysis results.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with analysis results
    stats : dict
        Dictionary containing statistical results
    """
    print("\nCreating visualizations...")
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('ICT Midnight Open Analysis - NQ Futures', fontsize=16, fontweight='bold')
    
    # 1. Overall Success Rate (Pie Chart)
    ax1 = axes[0, 0]
    sizes = [stats['days_touched'], stats['days_not_touched']]
    labels = [f'Touched\n({stats["days_touched"]} days)', 
              f'Not Touched\n({stats["days_not_touched"]} days)']
    colors = ['#2ecc71', '#e74c3c']
    explode = (0.05, 0)
    
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax1.set_title(f'Overall MO Touch Rate\nSuccess Rate: {stats["success_rate"]:.2f}%', 
                  fontweight='bold', fontsize=12)
    
    # 2. Touches by Day of Week (Bar Chart)
    ax2 = axes[0, 1]
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_data = results_df.groupby('DayName')['Touched'].agg(['sum', 'count'])
    
    # Reorder and prepare data
    day_counts = []
    day_totals = []
    day_labels = []
    for day in day_order:
        if day in day_data.index:
            day_labels.append(day[:3])  # Abbreviated day name
            day_counts.append(int(day_data.loc[day, 'sum']))
            day_totals.append(int(day_data.loc[day, 'count']))
    
    x_pos = np.arange(len(day_labels))
    bars = ax2.bar(x_pos, day_counts, color='#3498db', alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for i, (bar, count, total) in enumerate(zip(bars, day_counts, day_totals)):
        height = bar.get_height()
        rate = (count / total * 100) if total > 0 else 0
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({rate:.1f}%)',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax2.set_xlabel('Day of Week', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Number of MO Touches', fontweight='bold', fontsize=11)
    ax2.set_title('MO Touches by Day of Week', fontweight='bold', fontsize=12)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(day_labels, rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Success Rate by Day of Week (Line Chart)
    ax3 = axes[1, 0]
    day_rates = [(day_data.loc[day, 'sum'] / day_data.loc[day, 'count'] * 100) 
                 if day in day_data.index else 0 
                 for day in day_order]
    valid_days = [day[:3] for day in day_order if day in day_data.index]
    valid_rates = [rate for day, rate in zip(day_order, day_rates) if day in day_data.index]
    
    ax3.plot(range(len(valid_days)), valid_rates, marker='o', linewidth=2, 
             markersize=8, color='#e74c3c', label='Touch Rate')
    ax3.axhline(y=stats["success_rate"], color='#2ecc71', linestyle='--', 
                linewidth=2, label=f'Overall Average ({stats["success_rate"]:.1f}%)')
    
    ax3.set_xlabel('Day of Week', fontweight='bold', fontsize=11)
    ax3.set_ylabel('Success Rate (%)', fontweight='bold', fontsize=11)
    ax3.set_title('Success Rate by Day of Week', fontweight='bold', fontsize=12)
    ax3.set_xticks(range(len(valid_days)))
    ax3.set_xticklabels(valid_days, rotation=45)
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='best', fontsize=9)
    ax3.set_ylim(0, 100)
    
    # 4. Time Series of Touches (Last 100 days)
    ax4 = axes[1, 1]
    last_n = min(100, len(results_df))
    recent_data = results_df.tail(last_n).copy()
    recent_data['Date_Formatted'] = pd.to_datetime(recent_data['Date']).dt.strftime('%Y-%m-%d')
    
    colors_scatter = ['#2ecc71' if x else '#e74c3c' for x in recent_data['Touched']]
    x_pos_scatter = range(len(recent_data))
    
    ax4.scatter(x_pos_scatter, recent_data['Touched'].astype(int), 
               c=colors_scatter, s=50, alpha=0.6, edgecolors='black')
    
    # Add a moving average line
    window = min(10, len(recent_data) // 2)
    if window > 0:
        recent_data['MA'] = recent_data['Touched'].rolling(window=window, center=True).mean()
        ax4.plot(x_pos_scatter, recent_data['MA'], color='#3498db', 
                linewidth=2, alpha=0.7, label=f'{window}-day Moving Avg')
    
    ax4.set_xlabel('Trading Days (Most Recent)', fontweight='bold', fontsize=11)
    ax4.set_ylabel('MO Touched (1=Yes, 0=No)', fontweight='bold', fontsize=11)
    ax4.set_title(f'Touch Pattern - Last {last_n} Days', fontweight='bold', fontsize=12)
    ax4.set_ylim(-0.2, 1.2)
    ax4.set_yticks([0, 1])
    ax4.set_yticklabels(['No', 'Yes'])
    ax4.grid(True, alpha=0.3)
    if window > 0:
        ax4.legend(loc='best', fontsize=9)
    
    plt.tight_layout()
    
    # Save the figure
    output_path = 'ict_midnight_open_analysis.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")
    
    # Display the plot
    plt.show()
    
    return fig


def main(csv_path):
    """
    Main function to run the complete ICT Midnight Open analysis.
    
    Parameters:
    -----------
    csv_path : str
        Path to the CSV file containing NQ futures data
    """
    print("="*60)
    print("ICT MIDNIGHT OPEN ANALYSIS")
    print("Analyzing NQ Futures - London Killzone Statistics")
    print("="*60)
    
    try:
        # Step 1: Load and prepare data
        df = load_and_prepare_data(csv_path)
        
        # Step 2: Identify Midnight Open prices
        mo_series = identify_midnight_open(df)
        
        # Step 3: Analyze killzone touches
        results_df = analyze_killzone_touches(df, mo_series)
        
        # Step 4: Calculate statistics
        stats, day_stats = calculate_statistics(results_df)
        
        # Step 5: Create visualizations
        create_visualization(results_df, stats)
        
        # Optional: Save detailed results to CSV
        output_csv = 'ict_midnight_open_results.csv'
        results_df.to_csv(output_csv, index=False)
        print(f"\nDetailed results saved to: {output_csv}")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETED SUCCESSFULLY")
        print("="*60)
        
        return results_df, stats
        
    except Exception as e:
        print(f"\nERROR: An error occurred during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    import sys
    
    # Check if CSV path is provided as command line argument
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        # Default path - update this to your actual CSV file path
        csv_path = "NQ_M1_data.csv"
        print(f"No CSV path provided. Using default: {csv_path}")
        print("Usage: python ict_midnight_open_analysis.py <path_to_csv>")
        print()
    
    # Run the analysis
    results_df, stats = main(csv_path)
    
    if results_df is not None:
        print("\nTo use this script with your data:")
        print(f"  python ict_midnight_open_analysis.py /path/to/your/NQ_data.csv")
