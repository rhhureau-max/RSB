# Guide de Test avec Données Historiques NQ

Ce guide explique comment tester la stratégie FVG sur vos données historiques NQ Nasdaq Futures.

## 📋 Prérequis

### Format des Données

Vos fichiers CSV doivent avoir ce format :

```csv
DateTime,Open,High,Low,Close
2018-01-02 13:30:00,16000.0,16010.0,15995.0,16005.0
2018-01-02 13:31:00,16005.0,16012.0,16002.0,16010.0
...
```

**Important :**
- **Timeframe** : 1 minute obligatoire
- **DateTime** : En UTC (sera converti automatiquement en NY time)
- **Colonnes** : DateTime, Open, High, Low, Close (dans cet ordre)
- **Période** : Données complètes incluant la fenêtre 08:30-09:00 NY time

### Obtenir les Données NQ

Vous pouvez obtenir des données historiques NQ 1-minute depuis :

1. **Interactive Brokers** - TWS API ou Historical Data
2. **NinjaTrader** - Export de données historiques
3. **TradingView** - Export CSV (limité)
4. **Kinetick** - Données de qualité institutionnelle
5. **QuantConnect** - Données futures gratuites
6. **Databento** - Données institutionnelles payantes

## 🚀 Test sur Une Année

### Méthode 1 : Utiliser directement le backtester

```python
from fvg_backtest_strategy import FVGBacktester

# Charger les données 2018
backtester = FVGBacktester(data_path='nq_2018_1min.csv')

# Exécuter le backtest
results = backtester.run_backtest()

# Afficher les statistiques
backtester.print_statistics()

# Exporter les résultats
backtester.export_results('resultats_2018.csv')
```

### Méthode 2 : Script de test multi-années

```bash
# Placer vos fichiers dans le répertoire
# - nq_2018_1min.csv
# - nq_2019_1min.csv

python test_multi_year.py
```

## 📊 Test sur Plusieurs Années (2018-2019)

### Préparation

1. **Nommer vos fichiers** :
   ```
   nq_2018_1min.csv
   nq_2019_1min.csv
   ```

2. **Les placer dans le répertoire du projet**

3. **Exécuter le test** :
   ```bash
   python test_multi_year.py
   ```

### Avec Noms Personnalisés

```bash
python test_multi_year.py --file2018 mes_donnees_2018.csv --file2019 mes_donnees_2019.csv
```

### Avec Plusieurs Fichiers

```bash
python test_multi_year.py --files data_2018.csv data_2019.csv data_2020.csv
```

## 📈 Résultats Générés

Le script `test_multi_year.py` génère :

### 1. Statistiques par Année

Pour chaque année testée :
- Nombre de trades
- Win Rate
- Profit Factor
- R-Multiple moyen
- Points gagnés/perdus
- Taux d'atteinte des TPs
- Max Drawdown

### 2. Comparaison Inter-Annuelle

Tableau comparatif :
```
Année           Trades     Win Rate     Profit Factor   PnL Total      PnL Moyen
---------------------------------------------------------------------------------------
2018            45         62.22%       3.10            125.50         2.79
2019            52         58.33%       2.85            98.75          1.90
```

### 3. Statistiques Globales

- Tous trades combinés
- Win Rate global
- Profit Factor global
- R-Multiple moyen
- PnL total sur toutes les années
- Meilleure/Pire année
- Max Drawdown global

### 4. Export CSV

Fichier `backtest_multi_year_results.csv` contenant tous les trades avec :
- Date, Type (Long/Short)
- Prix d'entrée, SL, TPs
- TPs atteints
- PnL en points
- R-Multiple

## 🔍 Analyse Détaillée

### Script d'Analyse Personnalisé

Créez votre propre script pour une analyse approfondie :

```python
from fvg_backtest_strategy import FVGBacktester
import pandas as pd

# Charger plusieurs années
data_2018 = pd.read_csv('nq_2018_1min.csv')
data_2019 = pd.read_csv('nq_2019_1min.csv')

# Combiner
data_all = pd.concat([data_2018, data_2019], ignore_index=True)

# Backtest sur tout
backtester = FVGBacktester(dataframe=data_all)
results = backtester.run_backtest()

# Analyse par mois
results['month'] = pd.to_datetime(results['date']).dt.to_period('M')
monthly_pnl = results.groupby('month')['pnl_points'].sum()

print("\nPnL par Mois:")
print(monthly_pnl)

# Analyse par type de trade
print("\nAnalyse Long vs Short:")
print(results.groupby('type')['pnl_points'].agg(['count', 'mean', 'sum']))

# Courbe de PnL
results['cumulative_pnl'] = results['pnl_points'].cumsum()
print("\nCourbe de PnL:")
print(results[['date', 'cumulative_pnl']])
```

## 📊 Exemples de Requêtes d'Analyse

### 1. Meilleurs/Pires Mois

```python
monthly_stats = results.groupby(results['date'].dt.to_period('M')).agg({
    'pnl_points': ['sum', 'count'],
    'tp3_hit': 'sum'
})
print(monthly_stats.sort_values(('pnl_points', 'sum'), ascending=False))
```

### 2. Performance par Jour de la Semaine

```python
results['day_of_week'] = pd.to_datetime(results['date']).dt.day_name()
dow_stats = results.groupby('day_of_week')['pnl_points'].agg(['count', 'mean', 'sum'])
print(dow_stats)
```

### 3. Séries de Gains/Pertes

```python
results['win'] = results['pnl_points'] > 0
results['streak'] = results['win'].ne(results['win'].shift()).cumsum()
streaks = results.groupby('streak')['win'].agg(['first', 'count'])
max_win_streak = streaks[streaks['first'] == True]['count'].max()
max_loss_streak = streaks[streaks['first'] == False]['count'].max()
print(f"Plus longue série de gains: {max_win_streak}")
print(f"Plus longue série de pertes: {max_loss_streak}")
```

### 4. Distribution des R-Multiples

```python
results['r_multiple'] = results['pnl_points'] / results['risk_points']
print("\nDistribution R-Multiple:")
print(results['r_multiple'].describe())
print("\nHistogramme:")
print(results['r_multiple'].value_counts(bins=10).sort_index())
```

## ⚠️ Points d'Attention

### Qualité des Données

✅ **Vérifiez** :
- Pas de données manquantes dans la fenêtre 08:30-09:00 NY
- Pas de gaps importants dans les données
- Prix cohérents (High ≥ Open, Close et Low ≤ Open, Close)

❌ **Évitez** :
- Données avec slippage déjà inclus
- Données ajustées pour dividendes/splits (NQ n'en a pas)
- Mélanger différentes sources de données

### Interprétation des Résultats

1. **Win Rate > 60%** : Excellente stratégie
2. **Win Rate 50-60%** : Bonne stratégie (grâce au R:R favorable)
3. **Win Rate < 50%** : Réviser la stratégie ou les paramètres

**Profit Factor** :
- \> 2.0 : Excellent
- 1.5-2.0 : Bon
- 1.0-1.5 : Acceptable
- < 1.0 : Non profitable

**R-Multiple Moyen** :
- \> 1.5R : Excellent (actuel)
- 1.0-1.5R : Bon
- 0.5-1.0R : Acceptable
- < 0.5R : Faible

### Biais de Backtest

⚠️ **Attention aux biais** :
- **Look-ahead bias** : Évité (stratégie basée sur données passées uniquement)
- **Survivorship bias** : N/A (NQ toujours actif)
- **Overfitting** : Tester sur out-of-sample data
- **Data mining** : Ne pas ajuster paramètres trop souvent

## 🎯 Validation Robuste

### Walk-Forward Analysis

1. **In-Sample** : 2018 (développement)
2. **Out-of-Sample** : 2019 (validation)
3. **Comparer** : Les performances doivent être similaires

```python
# In-sample
backtester_2018 = FVGBacktester(data_path='nq_2018_1min.csv')
results_2018 = backtester_2018.run_backtest()
stats_2018 = backtester_2018.calculate_statistics()

# Out-of-sample
backtester_2019 = FVGBacktester(data_path='nq_2019_1min.csv')
results_2019 = backtester_2019.run_backtest()
stats_2019 = backtester_2019.calculate_statistics()

# Comparer
print(f"Win Rate 2018: {stats_2018['win_rate_overall']:.1f}%")
print(f"Win Rate 2019: {stats_2019['win_rate_overall']:.1f}%")
print(f"Différence: {abs(stats_2018['win_rate_overall'] - stats_2019['win_rate_overall']):.1f}%")

# Différence < 10% = Robuste
```

### Monte Carlo Simulation

```python
import numpy as np

# Prendre les R-multiples des trades
r_multiples = results['r_multiple'].values

# Simuler 1000 séquences aléatoires
simulations = []
for _ in range(1000):
    shuffled = np.random.choice(r_multiples, len(r_multiples), replace=True)
    cumulative = np.cumsum(shuffled * results['risk_points'].mean())
    simulations.append(cumulative[-1])

# Analyser distribution
print(f"PnL médian simulé: {np.median(simulations):.2f}")
print(f"5e percentile: {np.percentile(simulations, 5):.2f}")
print(f"95e percentile: {np.percentile(simulations, 95):.2f}")
```

## 📝 Checklist Avant Trading Réel

Avant de trader cette stratégie en réel :

- [ ] Backtest sur minimum 2 ans de données
- [ ] Win Rate > 50% sur out-of-sample
- [ ] Profit Factor > 1.5
- [ ] Max Drawdown acceptable (< 20% du capital)
- [ ] Performance consistante entre années
- [ ] Walk-forward validation réussie
- [ ] Paper trading pendant 1-2 mois
- [ ] Plan de gestion de capital défini
- [ ] Slippage et commissions calculés
- [ ] Stop loss et money management clairs

## 🆘 Support

Si vous rencontrez des problèmes :

1. **Vérifiez le format des données** : `DateTime,Open,High,Low,Close`
2. **Vérifiez la timezone** : Doit être UTC (pas déjà en NY time)
3. **Vérifiez la période** : Inclut bien 08:30-09:00 NY (13:30-14:00 UTC)
4. **Consultez les logs** : Le script affiche des messages détaillés

Pour des questions spécifiques, consultez :
- `QUICKSTART.md` - Guide de démarrage
- `FVG_STRATEGY_README.md` - Documentation complète
- `ANALYSE_STRATEGIE_FVG.md` - Exemple d'analyse

---

**Bonne chance avec vos backtests ! 📈**
