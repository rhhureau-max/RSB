#!/usr/bin/env python3
"""
Sample NQ Data Generator
========================

This script generates sample NQ futures data for testing the ICT Midnight Open analysis.
The generated data simulates realistic price movements and can be used to test the analysis script.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_nq_data(start_date='2023-01-01', end_date='2023-12-31', 
                            initial_price=15000, output_file='sample_NQ_M1_data.csv'):
    """
    Generate sample 1-minute NQ futures data for testing.
    
    Parameters:
    -----------
    start_date : str
        Start date for data generation (YYYY-MM-DD)
    end_date : str
        End date for data generation (YYYY-MM-DD)
    initial_price : float
        Initial price for the NQ futures
    output_file : str
        Output CSV file name
    """
    print(f"Generating sample NQ data from {start_date} to {end_date}...")
    
    # Convert dates
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Generate date range (only weekdays for simplicity)
    dates = pd.bdate_range(start=start, end=end, freq='B')
    
    all_data = []
    current_price = initial_price
    reference_price = None  # Initialize reference price for killzone logic
    
    for date in dates:
        # Generate 24 hours of 1-minute data
        for hour in range(24):
            for minute in range(60):
                timestamp = date + timedelta(hours=hour, minutes=minute)
                
                # Create realistic price movement
                # More volatility during certain hours (London/NY sessions)
                if hour in [1, 2, 3, 4, 8, 9, 13, 14, 15]:  # Key trading hours
                    volatility = 5.0
                else:
                    volatility = 2.0
                
                # Random walk with drift
                price_change = np.random.normal(0, volatility)
                current_price += price_change
                
                # Generate OHLC for the minute
                open_price = current_price
                
                # Create intra-minute movement
                high_offset = abs(np.random.normal(0, volatility * 0.5))
                low_offset = abs(np.random.normal(0, volatility * 0.5))
                close_change = np.random.normal(0, volatility * 0.3)
                
                high_price = open_price + high_offset
                low_price = open_price - low_offset
                close_price = open_price + close_change
                
                # Ensure OHLC integrity
                high_price = max(open_price, close_price, high_price)
                low_price = min(open_price, close_price, low_price)
                
                # Add some bias towards touching midnight open during killzone
                # This creates more realistic test data
                if hour in [1, 2, 3, 4]:  # Killzone hours
                    # 70% chance of extending range towards a reference level
                    if np.random.random() < 0.7:
                        if minute == 0 and hour == 1:
                            # Mark a reference price (simulating midnight open)
                            reference_price = open_price
                        elif reference_price is not None:
                            # Bias towards touching the reference
                            if reference_price > high_price:
                                high_price = max(high_price, 
                                               open_price + abs(reference_price - open_price) * 0.5)
                            elif reference_price < low_price:
                                low_price = min(low_price,
                                              open_price - abs(open_price - reference_price) * 0.5)
                
                # Round to 2 decimal places (typical for NQ)
                open_price = round(open_price, 2)
                high_price = round(high_price, 2)
                low_price = round(low_price, 2)
                close_price = round(close_price, 2)
                
                current_price = close_price
                
                # Create data row
                all_data.append({
                    'Date': timestamp.strftime('%Y-%m-%d'),
                    'Time': timestamp.strftime('%H:%M:%S'),
                    'Open': open_price,
                    'High': high_price,
                    'Low': low_price,
                    'Close': close_price
                })
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    
    print(f"Generated {len(df)} rows of data")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Price range: {df['Low'].min():.2f} to {df['High'].max():.2f}")
    print(f"Data saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    # Generate sample data
    df = generate_sample_nq_data(
        start_date='2023-01-01',
        end_date='2023-03-31',  # 3 months of data
        initial_price=15000,
        output_file='sample_NQ_M1_data.csv'
    )
    
    print("\nSample data preview:")
    print(df.head(10))
    print("\n...")
    print(df.tail(10))
    
    print("\n" + "="*60)
    print("Sample data generation complete!")
    print("You can now run the analysis with:")
    print("  python ict_midnight_open_analysis.py sample_NQ_M1_data.csv")
    print("="*60)
