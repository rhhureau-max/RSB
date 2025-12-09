"""
Fair Value Gap (FVG) Backtest Strategy for NQ Nasdaq Futures

This script implements a complete backtesting system for a trading strategy based on 
Fair Value Gaps (FVG) detected during the New York market open (08:30-09:00 EST/EDT).

Strategy Logic:
1. Detect first FVG between 08:30-09:00 NY time
2. Wait for breakout confirmation
3. Enter trade with defined risk management
4. Exit at multiple take profit levels or stop loss

Author: Quantitative Developer
Date: 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, time
import pytz
from typing import Tuple, Optional, Dict, List


class FVGBacktester:
    """
    Fair Value Gap (FVG) Backtesting Engine
    
    Attributes:
        data: DataFrame with OHLC data in 1-minute timeframe
        results: List of trade results
        timezone_ny: New York timezone object
    """
    
    def __init__(self, data_path: str = None, dataframe: pd.DataFrame = None):
        """
        Initialize the backtester with either a file path or DataFrame
        
        Args:
            data_path: Path to CSV file with columns: DateTime, Open, High, Low, Close
            dataframe: Pre-loaded DataFrame (alternative to data_path)
        """
        if dataframe is not None:
            self.data = dataframe.copy()
        elif data_path is not None:
            self.data = pd.read_csv(data_path)
        else:
            raise ValueError("Either data_path or dataframe must be provided")
        
        # Initialize timezone
        self.timezone_ny = pytz.timezone('America/New_York')
        
        # Prepare data
        self._prepare_data()
        
        # Results storage
        self.results = []
        self.trades_df = None
        
    def _prepare_data(self):
        """Prepare data with proper datetime indexing and NY timezone conversion"""
        # Convert DateTime column to datetime
        self.data['DateTime'] = pd.to_datetime(self.data['DateTime'])
        
        # Convert to NY timezone
        if self.data['DateTime'].dt.tz is None:
            # Assume UTC if no timezone
            self.data['DateTime'] = self.data['DateTime'].dt.tz_localize('UTC')
        
        self.data['DateTime'] = self.data['DateTime'].dt.tz_convert(self.timezone_ny)
        
        # Extract date and time components
        self.data['Date'] = self.data['DateTime'].dt.date
        self.data['Time'] = self.data['DateTime'].dt.time
        
        # Sort by datetime
        self.data = self.data.sort_values('DateTime').reset_index(drop=True)
        
    def detect_fvg(self, candles: pd.DataFrame, start_idx: int) -> Optional[Dict]:
        """
        Detect Fair Value Gap starting from a specific candle
        
        Args:
            candles: DataFrame with OHLC data
            start_idx: Starting index for detection
            
        Returns:
            Dictionary with FVG details or None if no FVG detected
        """
        # Need at least 3 candles to detect FVG (n-1, n, n+1)
        if start_idx + 2 >= len(candles):
            return None
        
        n_minus_1 = candles.iloc[start_idx]
        n = candles.iloc[start_idx + 1]
        n_plus_1 = candles.iloc[start_idx + 2]
        
        # Bullish FVG: High of (n-1) < Low of (n+1)
        if n_minus_1['High'] < n_plus_1['Low']:
            return {
                'type': 'bullish',
                'lower_bound': n_minus_1['High'],
                'upper_bound': n_plus_1['Low'],
                'candle_idx': start_idx + 2,  # FVG confirmed at n+1
                'datetime': n_plus_1['DateTime']
            }
        
        # Bearish FVG: Low of (n-1) > High of (n+1)
        if n_minus_1['Low'] > n_plus_1['High']:
            return {
                'type': 'bearish',
                'lower_bound': n_plus_1['High'],
                'upper_bound': n_minus_1['Low'],
                'candle_idx': start_idx + 2,  # FVG confirmed at n+1
                'datetime': n_plus_1['DateTime']
            }
        
        return None
    
    def find_first_fvg(self, day_data: pd.DataFrame) -> Optional[Dict]:
        """
        Find the first FVG in the 08:30-09:00 window
        
        Args:
            day_data: DataFrame for a single day
            
        Returns:
            Dictionary with FVG details or None
        """
        # Filter for 08:30-09:00 window
        setup_window = day_data[
            (day_data['Time'] >= time(8, 30)) & 
            (day_data['Time'] < time(9, 0))
        ].reset_index(drop=True)
        
        if len(setup_window) < 3:
            return None
        
        # Search for first FVG
        for i in range(len(setup_window) - 2):
            fvg = self.detect_fvg(setup_window, i)
            if fvg is not None:
                # Store original index in full day data
                fvg['original_idx'] = day_data[
                    day_data['DateTime'] == fvg['datetime']
                ].index[0]
                return fvg
        
        return None
    
    def find_entry_signal(self, day_data: pd.DataFrame, fvg: Dict, 
                         start_idx: int) -> Optional[Dict]:
        """
        Find entry signal after FVG detection
        
        Args:
            day_data: DataFrame for a single day
            fvg: FVG dictionary with type and bounds
            start_idx: Index to start looking for entry (after FVG formation)
            
        Returns:
            Dictionary with entry details or None
        """
        # Look at candles after FVG formation
        remaining_candles = day_data.loc[start_idx:]
        
        for idx, candle in remaining_candles.iterrows():
            if fvg['type'] == 'bullish':
                # Short entry: Close below FVG lower bound
                if candle['Close'] < fvg['lower_bound']:
                    return {
                        'type': 'short',
                        'entry_price': candle['Close'],
                        'entry_datetime': candle['DateTime'],
                        'trigger_high': candle['High'],
                        'trigger_low': candle['Low'],
                        'entry_idx': idx
                    }
            
            elif fvg['type'] == 'bearish':
                # Long entry: Close above FVG upper bound
                if candle['Close'] > fvg['upper_bound']:
                    return {
                        'type': 'long',
                        'entry_price': candle['Close'],
                        'entry_datetime': candle['DateTime'],
                        'trigger_high': candle['High'],
                        'trigger_low': candle['Low'],
                        'entry_idx': idx
                    }
        
        return None
    
    def calculate_risk_levels(self, entry: Dict) -> Dict:
        """
        Calculate stop loss and take profit levels
        
        Args:
            entry: Entry signal dictionary
            
        Returns:
            Dictionary with SL and TP levels
        """
        if entry['type'] == 'short':
            # SL 0.5 points above trigger high
            sl_price = entry['trigger_high'] + 0.5
            risk = sl_price - entry['entry_price']
            
        else:  # long
            # SL 0.5 points below trigger low
            sl_price = entry['trigger_low'] - 0.5
            risk = entry['entry_price'] - sl_price
        
        # Calculate TP levels
        if entry['type'] == 'short':
            tp1 = entry['entry_price'] - (1.0 * risk)
            tp2 = entry['entry_price'] - (1.5 * risk)
            tp3 = entry['entry_price'] - (2.0 * risk)
        else:  # long
            tp1 = entry['entry_price'] + (1.0 * risk)
            tp2 = entry['entry_price'] + (1.5 * risk)
            tp3 = entry['entry_price'] + (2.0 * risk)
        
        return {
            'sl_price': sl_price,
            'risk': risk,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3
        }
    
    def simulate_trade(self, day_data: pd.DataFrame, entry: Dict, 
                      levels: Dict) -> Dict:
        """
        Simulate trade execution and track results
        
        Args:
            day_data: DataFrame for the trading day
            entry: Entry signal dictionary
            levels: Risk management levels dictionary
            
        Returns:
            Dictionary with trade results
        """
        # Track position status
        position_status = {
            'tp1_hit': False,
            'tp2_hit': False,
            'tp3_hit': False,
            'sl_hit': False,
            'remaining_position': 1.0  # 100%
        }
        
        pnl_points = 0.0
        exit_details = []
        
        # Look at candles after entry
        remaining_data = day_data.loc[entry['entry_idx'] + 1:]
        
        for idx, candle in remaining_data.iterrows():
            if position_status['remaining_position'] <= 0:
                break
            
            # Check for SL hit first
            if entry['type'] == 'short':
                if candle['High'] >= levels['sl_price']:
                    # SL hit - close remaining position
                    loss = (levels['sl_price'] - entry['entry_price']) * position_status['remaining_position']
                    pnl_points += loss
                    exit_details.append({
                        'exit_type': 'SL',
                        'exit_price': levels['sl_price'],
                        'position_closed': position_status['remaining_position'],
                        'pnl': loss
                    })
                    position_status['sl_hit'] = True
                    position_status['remaining_position'] = 0
                    break
            else:  # long
                if candle['Low'] <= levels['sl_price']:
                    # SL hit - close remaining position
                    loss = (levels['sl_price'] - entry['entry_price']) * position_status['remaining_position']
                    pnl_points += loss
                    exit_details.append({
                        'exit_type': 'SL',
                        'exit_price': levels['sl_price'],
                        'position_closed': position_status['remaining_position'],
                        'pnl': loss
                    })
                    position_status['sl_hit'] = True
                    position_status['remaining_position'] = 0
                    break
            
            # Check for TP hits
            if entry['type'] == 'short':
                # Check TP3 first (furthest)
                if not position_status['tp3_hit'] and candle['Low'] <= levels['tp3']:
                    gain = (entry['entry_price'] - levels['tp3']) * 0.34
                    pnl_points += gain
                    exit_details.append({
                        'exit_type': 'TP3',
                        'exit_price': levels['tp3'],
                        'position_closed': 0.34,
                        'pnl': gain
                    })
                    position_status['tp3_hit'] = True
                    position_status['remaining_position'] -= 0.34
                
                # Check TP2
                if not position_status['tp2_hit'] and candle['Low'] <= levels['tp2']:
                    gain = (entry['entry_price'] - levels['tp2']) * 0.33
                    pnl_points += gain
                    exit_details.append({
                        'exit_type': 'TP2',
                        'exit_price': levels['tp2'],
                        'position_closed': 0.33,
                        'pnl': gain
                    })
                    position_status['tp2_hit'] = True
                    position_status['remaining_position'] -= 0.33
                
                # Check TP1
                if not position_status['tp1_hit'] and candle['Low'] <= levels['tp1']:
                    gain = (entry['entry_price'] - levels['tp1']) * 0.33
                    pnl_points += gain
                    exit_details.append({
                        'exit_type': 'TP1',
                        'exit_price': levels['tp1'],
                        'position_closed': 0.33,
                        'pnl': gain
                    })
                    position_status['tp1_hit'] = True
                    position_status['remaining_position'] -= 0.33
                    
            else:  # long
                # Check TP3 first (furthest)
                if not position_status['tp3_hit'] and candle['High'] >= levels['tp3']:
                    gain = (levels['tp3'] - entry['entry_price']) * 0.34
                    pnl_points += gain
                    exit_details.append({
                        'exit_type': 'TP3',
                        'exit_price': levels['tp3'],
                        'position_closed': 0.34,
                        'pnl': gain
                    })
                    position_status['tp3_hit'] = True
                    position_status['remaining_position'] -= 0.34
                
                # Check TP2
                if not position_status['tp2_hit'] and candle['High'] >= levels['tp2']:
                    gain = (levels['tp2'] - entry['entry_price']) * 0.33
                    pnl_points += gain
                    exit_details.append({
                        'exit_type': 'TP2',
                        'exit_price': levels['tp2'],
                        'position_closed': 0.33,
                        'pnl': gain
                    })
                    position_status['tp2_hit'] = True
                    position_status['remaining_position'] -= 0.33
                
                # Check TP1
                if not position_status['tp1_hit'] and candle['High'] >= levels['tp1']:
                    gain = (levels['tp1'] - entry['entry_price']) * 0.33
                    pnl_points += gain
                    exit_details.append({
                        'exit_type': 'TP1',
                        'exit_price': levels['tp1'],
                        'position_closed': 0.33,
                        'pnl': gain
                    })
                    position_status['tp1_hit'] = True
                    position_status['remaining_position'] -= 0.33
        
        # If position still open at end of day, close at market (SL)
        if position_status['remaining_position'] > 0:
            if entry['type'] == 'short':
                loss = (levels['sl_price'] - entry['entry_price']) * position_status['remaining_position']
            else:
                loss = (levels['sl_price'] - entry['entry_price']) * position_status['remaining_position']
            pnl_points += loss
            position_status['sl_hit'] = True
        
        return {
            'date': entry['entry_datetime'].date(),
            'type': entry['type'],
            'entry_price': entry['entry_price'],
            'entry_time': entry['entry_datetime'].time(),
            'sl_price': levels['sl_price'],
            'tp1_price': levels['tp1'],
            'tp2_price': levels['tp2'],
            'tp3_price': levels['tp3'],
            'tp1_hit': position_status['tp1_hit'],
            'tp2_hit': position_status['tp2_hit'],
            'tp3_hit': position_status['tp3_hit'],
            'sl_hit': position_status['sl_hit'],
            'pnl_points': pnl_points,
            'risk_points': levels['risk']
        }
    
    def run_backtest(self) -> pd.DataFrame:
        """
        Run the complete backtest on all available data
        
        Returns:
            DataFrame with trade results
        """
        print("Starting FVG Backtest...")
        print(f"Data range: {self.data['DateTime'].min()} to {self.data['DateTime'].max()}")
        print(f"Total candles: {len(self.data)}")
        print("-" * 80)
        
        # Group by date
        unique_dates = self.data['Date'].unique()
        
        for date in unique_dates:
            # Get data for this day
            day_data = self.data[self.data['Date'] == date].copy()
            
            # Step 1: Find first FVG in 08:30-09:00 window
            fvg = self.find_first_fvg(day_data)
            
            if fvg is None:
                continue  # No FVG found, skip this day
            
            # Step 2: Find entry signal after FVG
            entry = self.find_entry_signal(day_data, fvg, fvg['original_idx'] + 1)
            
            if entry is None:
                continue  # No entry signal, skip this day
            
            # Step 3: Calculate risk management levels
            levels = self.calculate_risk_levels(entry)
            
            # Step 4: Simulate trade
            trade_result = self.simulate_trade(day_data, entry, levels)
            
            self.results.append(trade_result)
            
            # Print progress
            if len(self.results) % 10 == 0:
                print(f"Processed {len(self.results)} trades...")
        
        # Convert results to DataFrame
        self.trades_df = pd.DataFrame(self.results)
        
        print("-" * 80)
        print(f"Backtest complete! Total trades: {len(self.results)}")
        
        return self.trades_df
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate performance statistics
        
        Returns:
            Dictionary with performance metrics
        """
        if self.trades_df is None or len(self.trades_df) == 0:
            return {
                'total_trades': 0,
                'error': 'No trades executed'
            }
        
        df = self.trades_df
        
        # Basic statistics
        total_trades = len(df)
        winning_trades = len(df[df['pnl_points'] > 0])
        losing_trades = len(df[df['pnl_points'] <= 0])
        
        # Win rates
        win_rate_overall = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        win_rate_tp1 = (df['tp1_hit'].sum() / total_trades * 100) if total_trades > 0 else 0
        win_rate_tp2 = (df['tp2_hit'].sum() / total_trades * 100) if total_trades > 0 else 0
        win_rate_tp3 = (df['tp3_hit'].sum() / total_trades * 100) if total_trades > 0 else 0
        
        # PnL statistics
        total_pnl = df['pnl_points'].sum()
        avg_pnl = df['pnl_points'].mean()
        
        # Profit factor
        gross_profit = df[df['pnl_points'] > 0]['pnl_points'].sum()
        gross_loss = abs(df[df['pnl_points'] <= 0]['pnl_points'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
        
        # Maximum drawdown
        cumulative_pnl = df['pnl_points'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = cumulative_pnl - running_max
        max_drawdown = drawdown.min()
        
        # Trade type statistics
        long_trades = len(df[df['type'] == 'long'])
        short_trades = len(df[df['type'] == 'short'])
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate_overall': win_rate_overall,
            'win_rate_tp1': win_rate_tp1,
            'win_rate_tp2': win_rate_tp2,
            'win_rate_tp3': win_rate_tp3,
            'total_pnl_points': total_pnl,
            'average_pnl_points': avg_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'max_drawdown_points': max_drawdown,
            'long_trades': long_trades,
            'short_trades': short_trades
        }
    
    def print_statistics(self):
        """Print formatted statistics to console"""
        stats = self.calculate_statistics()
        
        print("\n" + "=" * 80)
        print("BACKTEST PERFORMANCE STATISTICS")
        print("=" * 80)
        
        if 'error' in stats:
            print(f"Error: {stats['error']}")
            return
        
        print(f"\n📊 TRADE SUMMARY")
        print(f"  Total Trades:        {stats['total_trades']}")
        print(f"  Winning Trades:      {stats['winning_trades']}")
        print(f"  Losing Trades:       {stats['losing_trades']}")
        print(f"  Long Trades:         {stats['long_trades']}")
        print(f"  Short Trades:        {stats['short_trades']}")
        
        print(f"\n🎯 WIN RATES")
        print(f"  Overall Win Rate:    {stats['win_rate_overall']:.2f}%")
        print(f"  TP1 Hit Rate:        {stats['win_rate_tp1']:.2f}%")
        print(f"  TP2 Hit Rate:        {stats['win_rate_tp2']:.2f}%")
        print(f"  TP3 Hit Rate:        {stats['win_rate_tp3']:.2f}%")
        
        print(f"\n💰 PROFIT & LOSS")
        print(f"  Total PnL:           {stats['total_pnl_points']:.2f} points")
        print(f"  Average PnL:         {stats['average_pnl_points']:.2f} points")
        print(f"  Gross Profit:        {stats['gross_profit']:.2f} points")
        print(f"  Gross Loss:          {stats['gross_loss']:.2f} points")
        print(f"  Profit Factor:       {stats['profit_factor']:.2f}")
        
        print(f"\n📉 RISK METRICS")
        print(f"  Max Drawdown:        {stats['max_drawdown_points']:.2f} points")
        
        print("\n" + "=" * 80)
    
    def export_results(self, output_path: str):
        """
        Export results to CSV file
        
        Args:
            output_path: Path to save the results CSV
        """
        if self.trades_df is not None:
            self.trades_df.to_csv(output_path, index=False)
            print(f"\n✅ Results exported to: {output_path}")
        else:
            print("❌ No results to export. Run backtest first.")


def main():
    """
    Example usage of the FVG Backtester
    
    This demonstrates how to:
    1. Load data from CSV
    2. Run the backtest
    3. Display statistics
    4. Export results
    """
    print("=" * 80)
    print("Fair Value Gap (FVG) Backtest Strategy")
    print("=" * 80)
    
    # Example 1: Using CSV file
    # Uncomment and modify the path to your data file
    """
    backtester = FVGBacktester(data_path='nq_futures_1min_data.csv')
    results = backtester.run_backtest()
    backtester.print_statistics()
    backtester.export_results('fvg_backtest_results.csv')
    """
    
    # Example 2: Using DataFrame
    # Create sample data for demonstration
    print("\nGenerating sample data for demonstration...")
    
    # Generate sample 1-minute data
    from datetime import datetime, timedelta
    
    start_date = datetime(2024, 1, 1, 8, 0, 0)
    dates = [start_date + timedelta(minutes=i) for i in range(1000)]
    
    # Create realistic sample data with FVG opportunities
    np.random.seed(42)
    base_price = 16000
    
    sample_data = {
        'DateTime': dates,
        'Open': base_price + np.random.randn(1000) * 10,
        'High': base_price + np.random.randn(1000) * 10 + 5,
        'Low': base_price + np.random.randn(1000) * 10 - 5,
        'Close': base_price + np.random.randn(1000) * 10
    }
    
    # Ensure High is highest and Low is lowest
    df_sample = pd.DataFrame(sample_data)
    df_sample['High'] = df_sample[['Open', 'High', 'Close']].max(axis=1)
    df_sample['Low'] = df_sample[['Open', 'Low', 'Close']].min(axis=1)
    
    print("\n⚠️  NOTE: This is using SAMPLE DATA for demonstration.")
    print("    For real backtesting, provide your CSV file with actual NQ data.")
    print("\n📝 Expected CSV format:")
    print("    DateTime, Open, High, Low, Close")
    print("    2024-01-01 08:30:00, 16000.0, 16010.5, 15995.0, 16005.0")
    print("    ...")
    
    # Run backtest on sample data
    backtester = FVGBacktester(dataframe=df_sample)
    results = backtester.run_backtest()
    
    if len(results) > 0:
        backtester.print_statistics()
        
        print("\n📋 Sample of Trade Results:")
        print(results.head(10).to_string())
        
        # Optionally export results
        # backtester.export_results('fvg_backtest_results.csv')
    else:
        print("\n❌ No trades were generated with the sample data.")
        print("   This is expected with random data. Use real NQ futures data for actual backtesting.")
    
    print("\n" + "=" * 80)
    print("HOW TO USE WITH YOUR DATA:")
    print("=" * 80)
    print("""
# Method 1: Using CSV file
backtester = FVGBacktester(data_path='path/to/your/nq_data.csv')
results = backtester.run_backtest()
backtester.print_statistics()
backtester.export_results('results.csv')

# Method 2: Using existing DataFrame
import pandas as pd
df = pd.read_csv('your_data.csv')
backtester = FVGBacktester(dataframe=df)
results = backtester.run_backtest()
backtester.print_statistics()
    """)


if __name__ == "__main__":
    main()
