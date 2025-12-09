"""
Script pour tester la stratégie FVG sur plusieurs années de données NQ

Ce script permet de :
1. Charger des données pour 2018, 2019, ou toute autre période
2. Analyser année par année
3. Générer un rapport complet avec comparaisons

Usage:
    python test_multi_year.py --file2018 nq_2018_1min.csv --file2019 nq_2019_1min.csv
    
    OU placer vos fichiers comme:
    - nq_2018_1min.csv
    - nq_2019_1min.csv
    
    et exécuter: python test_multi_year.py
"""

import argparse
import pandas as pd
import os
from fvg_backtest_strategy import FVGBacktester


def test_year(file_path, year_label):
    """Test la stratégie sur une année de données"""
    print("\n" + "=" * 80)
    print(f"BACKTEST {year_label}")
    print("=" * 80)
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier non trouvé: {file_path}")
        return None
    
    # Charger les données
    print(f"\n📂 Chargement: {file_path}")
    try:
        df = pd.read_csv(file_path)
        print(f"✓ {len(df)} lignes chargées")
        print(f"✓ Période: {df['DateTime'].min()} à {df['DateTime'].max()}")
    except Exception as e:
        print(f"❌ Erreur de chargement: {e}")
        return None
    
    # Exécuter le backtest
    try:
        backtester = FVGBacktester(dataframe=df)
        results = backtester.run_backtest()
        
        if len(results) == 0:
            print(f"\n⚠️ Aucun trade généré pour {year_label}")
            return None
        
        # Afficher les statistiques
        backtester.print_statistics()
        
        # Retourner les résultats pour analyse comparative
        stats = backtester.calculate_statistics()
        stats['year'] = year_label
        stats['trades_df'] = results
        
        return stats
        
    except Exception as e:
        print(f"❌ Erreur pendant le backtest: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_years(all_stats):
    """Compare les résultats entre différentes années"""
    if len(all_stats) < 2:
        return
    
    print("\n" + "=" * 80)
    print("COMPARAISON INTER-ANNUELLE")
    print("=" * 80)
    
    # Tableau de comparaison
    print("\n📊 TABLEAU COMPARATIF:\n")
    print(f"{'Année':<15} {'Trades':<10} {'Win Rate':<12} {'Profit Factor':<15} {'PnL Total':<15} {'PnL Moyen':<15}")
    print("-" * 95)
    
    for stats in all_stats:
        year = stats['year']
        trades = stats['total_trades']
        wr = f"{stats['win_rate_overall']:.1f}%"
        pf = f"{stats['profit_factor']:.2f}" if stats['profit_factor'] != float('inf') else "∞"
        total_pnl = f"{stats['total_pnl_points']:.2f}"
        avg_pnl = f"{stats['average_pnl_points']:.2f}"
        
        print(f"{year:<15} {trades:<10} {wr:<12} {pf:<15} {total_pnl:<15} {avg_pnl:<15}")
    
    # Totaux
    print("\n" + "=" * 80)
    print("STATISTIQUES GLOBALES (TOUTES ANNÉES)")
    print("=" * 80)
    
    total_trades = sum(s['total_trades'] for s in all_stats)
    total_winning = sum(s['winning_trades'] for s in all_stats)
    total_pnl = sum(s['total_pnl_points'] for s in all_stats)
    total_gross_profit = sum(s['gross_profit'] for s in all_stats)
    total_gross_loss = sum(s['gross_loss'] for s in all_stats)
    
    global_win_rate = (total_winning / total_trades * 100) if total_trades > 0 else 0
    global_pf = (total_gross_profit / total_gross_loss) if total_gross_loss > 0 else float('inf')
    global_avg_pnl = total_pnl / total_trades if total_trades > 0 else 0
    
    # Combiner tous les trades pour calculer R-Multiple global
    all_trades = pd.concat([s['trades_df'] for s in all_stats], ignore_index=True)
    all_trades['r_multiple'] = all_trades['pnl_points'] / all_trades['risk_points']
    global_r_multiple = all_trades['r_multiple'].mean()
    
    # Calculer drawdown global
    all_trades_sorted = all_trades.sort_values('date')
    cumulative_pnl = all_trades_sorted['pnl_points'].cumsum()
    running_max = cumulative_pnl.expanding().max()
    drawdown = cumulative_pnl - running_max
    max_drawdown = drawdown.min()
    
    print(f"""
📊 MÉTRIQUES GLOBALES:

  Total Trades: {total_trades}
  Win Rate Global: {global_win_rate:.2f}%
  Profit Factor Global: {global_pf:.2f}
  R-Multiple Moyen: {global_r_multiple:.2f}R
  
  PnL Total (toutes années): {total_pnl:.2f} points
  PnL Moyen par Trade: {global_avg_pnl:.2f} points
  Max Drawdown: {max_drawdown:.2f} points
  
  Meilleure Année: {max(all_stats, key=lambda x: x['total_pnl_points'])['year']} ({max(s['total_pnl_points'] for s in all_stats):.2f} points)
  Pire Année: {min(all_stats, key=lambda x: x['total_pnl_points'])['year']} ({min(s['total_pnl_points'] for s in all_stats):.2f} points)
    """)
    
    # Exporter tous les trades
    output_file = 'backtest_multi_year_results.csv'
    all_trades_sorted.to_csv(output_file, index=False)
    print(f"✅ Tous les trades exportés vers: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Test FVG strategy sur plusieurs années')
    parser.add_argument('--file2018', default='nq_2018_1min.csv', help='Fichier CSV pour 2018')
    parser.add_argument('--file2019', default='nq_2019_1min.csv', help='Fichier CSV pour 2019')
    parser.add_argument('--files', nargs='+', help='Liste de fichiers à tester')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("TEST STRATÉGIE FVG - MULTI-ANNÉES")
    print("=" * 80)
    
    all_stats = []
    
    if args.files:
        # Mode: fichiers personnalisés
        for file_path in args.files:
            year_label = os.path.basename(file_path).split('.')[0]
            stats = test_year(file_path, year_label)
            if stats:
                all_stats.append(stats)
    else:
        # Mode: 2018 et 2019
        # Test 2018
        if os.path.exists(args.file2018):
            stats_2018 = test_year(args.file2018, "2018")
            if stats_2018:
                all_stats.append(stats_2018)
        else:
            print(f"\n⚠️ Fichier 2018 non trouvé: {args.file2018}")
            print("   Utilisez --file2018 pour spécifier le chemin")
        
        # Test 2019
        if os.path.exists(args.file2019):
            stats_2019 = test_year(args.file2019, "2019")
            if stats_2019:
                all_stats.append(stats_2019)
        else:
            print(f"\n⚠️ Fichier 2019 non trouvé: {args.file2019}")
            print("   Utilisez --file2019 pour spécifier le chemin")
    
    # Comparaison si plusieurs années testées
    if len(all_stats) > 0:
        if len(all_stats) > 1:
            compare_years(all_stats)
        
        print("\n" + "=" * 80)
        print("BACKTEST TERMINÉ")
        print("=" * 80)
        print(f"\n✅ {len(all_stats)} année(s) testée(s)")
        print(f"✅ {sum(s['total_trades'] for s in all_stats)} trades au total")
    else:
        print("\n" + "=" * 80)
        print("❌ AUCUNE DONNÉE TESTÉE")
        print("=" * 80)
        print("\n📝 INSTRUCTIONS:")
        print("   1. Placez vos fichiers CSV de données NQ 1-minute dans le répertoire")
        print("   2. Nommez-les: nq_2018_1min.csv, nq_2019_1min.csv")
        print("   3. Format requis: DateTime,Open,High,Low,Close")
        print("   4. Exécutez: python test_multi_year.py")
        print("\n   OU utilisez des noms personnalisés:")
        print("   python test_multi_year.py --file2018 mon_fichier_2018.csv --file2019 mon_fichier_2019.csv")


if __name__ == "__main__":
    main()
