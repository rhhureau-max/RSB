# Fair Value Gap (FVG) Backtest Strategy - Documentation

## Vue d'ensemble

Ce script Python implémente un système complet de backtesting pour une stratégie de trading basée sur les Fair Value Gaps (FVG) détectés pendant l'ouverture du marché de New York (08:30-09:00 EST/EDT).

## Stratégie

### 1. Configuration Temporelle
- Convertit automatiquement les horaires en heure de New York (EST/EDT)
- Fenêtre de recherche du setup : **08:30 à 09:00** (heure NY)
- Données en timeframe **1 minute** pour la précision

### 2. Détection du FVG (Fair Value Gap)

Le script identifie le **premier FVG** qui se forme après 08:30 :

**FVG Haussier (Bullish):**
- Condition : `High de la bougie (n-1) < Low de la bougie (n+1)`
- Zone du FVG : Entre ces deux prix
- Signal d'entrée : **SHORT** quand le prix casse en dessous

**FVG Baissier (Bearish):**
- Condition : `Low de la bougie (n-1) > High de la bougie (n+1)`
- Zone du FVG : Entre ces deux prix
- Signal d'entrée : **LONG** quand le prix casse au-dessus

### 3. Logique d'Entrée (Inversion/Cassure)

**Pour un SHORT (FVG Haussier):**
- Attendre qu'une bougie clôture **sous** la borne basse du FVG
- Entrée immédiate à la clôture de cette bougie ("Trigger Candle")

**Pour un LONG (FVG Baissier):**
- Attendre qu'une bougie clôture **au-dessus** de la borne haute du FVG
- Entrée immédiate à la clôture de cette bougie

### 4. Gestion du Risque (SL & TP)

**Stop Loss (SL):**
- **SHORT** : SL placé 0.5 point au-dessus du High de la "Trigger Candle"
- **LONG** : SL placé 0.5 point en-dessous du Low de la "Trigger Candle"

**Take Profit (TP):**
Le calcul est basé sur le Risque (distance entre Entrée et SL) :
- **TP1 = 1R** (1x le Risque) → Fermeture de **33%** de la position
- **TP2 = 1.5R** (1.5x le Risque) → Fermeture de **33%** de la position
- **TP3 = 2R** (2x le Risque) → Fermeture de **34%** de la position

## Installation

### Prérequis

```bash
pip install pandas numpy pytz
```

### Dépendances

- **pandas** : Manipulation des données
- **numpy** : Calculs numériques
- **pytz** : Gestion des fuseaux horaires

## Utilisation

### Méthode 1 : Avec un fichier CSV

```python
from fvg_backtest_strategy import FVGBacktester

# Charger les données depuis un CSV
backtester = FVGBacktester(data_path='nq_futures_1min_data.csv')

# Exécuter le backtest
results = backtester.run_backtest()

# Afficher les statistiques
backtester.print_statistics()

# Exporter les résultats
backtester.export_results('fvg_backtest_results.csv')
```

### Méthode 2 : Avec un DataFrame existant

```python
import pandas as pd
from fvg_backtest_strategy import FVGBacktester

# Charger vos données
df = pd.read_csv('your_data.csv')

# Créer le backtester
backtester = FVGBacktester(dataframe=df)

# Exécuter et analyser
results = backtester.run_backtest()
backtester.print_statistics()
```

## Format des Données

Le fichier CSV doit contenir les colonnes suivantes :

```
DateTime, Open, High, Low, Close
```

**Exemple :**
```
DateTime,Open,High,Low,Close
2024-01-01 08:30:00,16000.0,16010.5,15995.0,16005.0
2024-01-01 08:31:00,16005.0,16015.0,16003.0,16012.0
2024-01-01 08:32:00,16012.0,16020.0,16010.0,16018.0
...
```

**Notes :**
- Le format DateTime doit être parsable par pandas
- Si aucun fuseau horaire n'est spécifié, UTC est assumé
- La conversion en heure NY est automatique

## Résultats

### DataFrame de Résultats

Le backtest génère un DataFrame avec les colonnes suivantes :

| Colonne | Description |
|---------|-------------|
| `date` | Date du trade |
| `type` | Type de trade ('long' ou 'short') |
| `entry_price` | Prix d'entrée |
| `entry_time` | Heure d'entrée |
| `sl_price` | Prix du Stop Loss |
| `tp1_price` | Prix du Take Profit 1 |
| `tp2_price` | Prix du Take Profit 2 |
| `tp3_price` | Prix du Take Profit 3 |
| `tp1_hit` | TP1 atteint ? (True/False) |
| `tp2_hit` | TP2 atteint ? (True/False) |
| `tp3_hit` | TP3 atteint ? (True/False) |
| `sl_hit` | Stop Loss touché ? (True/False) |
| `pnl_points` | Profit/Perte en points |
| `risk_points` | Risque du trade en points |

### Statistiques Calculées

Le script calcule automatiquement :

**📊 Résumé des Trades**
- Nombre total de trades
- Trades gagnants / perdants
- Trades Long / Short

**🎯 Win Rates**
- Win Rate Global
- Taux d'atteinte TP1
- Taux d'atteinte TP2
- Taux d'atteinte TP3

**💰 Profit & Loss**
- PnL Total en points
- PnL Moyen par trade
- Profit Brut
- Perte Brute
- **Profit Factor** (Profit Brut / Perte Brute)

**📉 Métriques de Risque**
- **Maximum Drawdown** en points

## Exemple de Sortie

```
================================================================================
BACKTEST PERFORMANCE STATISTICS
================================================================================

📊 TRADE SUMMARY
  Total Trades:        45
  Winning Trades:      28
  Losing Trades:       17
  Long Trades:         22
  Short Trades:        23

🎯 WIN RATES
  Overall Win Rate:    62.22%
  TP1 Hit Rate:        55.56%
  TP2 Hit Rate:        40.00%
  TP3 Hit Rate:        22.22%

💰 PROFIT & LOSS
  Total PnL:           125.50 points
  Average PnL:         2.79 points
  Gross Profit:        185.25 points
  Gross Loss:          59.75 points
  Profit Factor:       3.10

📉 RISK METRICS
  Max Drawdown:        -15.25 points

================================================================================
```

## Architecture du Code

### Classe Principale : `FVGBacktester`

**Méthodes Principales :**

1. `__init__(data_path, dataframe)` - Initialisation avec données
2. `detect_fvg(candles, start_idx)` - Détecte un FVG
3. `find_first_fvg(day_data)` - Trouve le premier FVG du jour
4. `find_entry_signal(day_data, fvg, start_idx)` - Trouve le signal d'entrée
5. `calculate_risk_levels(entry)` - Calcule SL et TP
6. `simulate_trade(day_data, entry, levels)` - Simule l'exécution du trade
7. `run_backtest()` - Exécute le backtest complet
8. `calculate_statistics()` - Calcule les statistiques de performance
9. `print_statistics()` - Affiche les statistiques formatées
10. `export_results(output_path)` - Exporte les résultats en CSV

### Flux de Travail

```
1. Chargement des données
   ↓
2. Conversion fuseau horaire (NY)
   ↓
3. Pour chaque jour :
   a. Chercher FVG entre 08:30-09:00
   b. Si FVG trouvé → Chercher signal d'entrée
   c. Si signal → Calculer SL/TP
   d. Simuler le trade
   ↓
4. Agréger les résultats
   ↓
5. Calculer les statistiques
   ↓
6. Exporter les résultats
```

## Personnalisation

Vous pouvez facilement modifier les paramètres de la stratégie :

### Modifier la fenêtre de setup
```python
# Dans find_first_fvg()
setup_window = day_data[
    (day_data['Time'] >= time(8, 30)) &  # Modifier l'heure de début
    (day_data['Time'] < time(9, 0))      # Modifier l'heure de fin
]
```

### Modifier le Stop Loss
```python
# Dans calculate_risk_levels()
sl_price = entry['trigger_high'] + 0.5  # Modifier 0.5 pour SHORT
sl_price = entry['trigger_low'] - 0.5   # Modifier 0.5 pour LONG
```

### Modifier les Take Profits
```python
# Dans calculate_risk_levels()
tp1 = entry['entry_price'] - (1.0 * risk)   # Modifier 1.0 (1R)
tp2 = entry['entry_price'] - (1.5 * risk)   # Modifier 1.5 (1.5R)
tp3 = entry['entry_price'] - (2.0 * risk)   # Modifier 2.0 (2R)
```

### Modifier la répartition de position
```python
# Dans simulate_trade()
gain = (entry['entry_price'] - levels['tp3']) * 0.34  # Modifier 0.34 (34%)
gain = (entry['entry_price'] - levels['tp2']) * 0.33  # Modifier 0.33 (33%)
gain = (entry['entry_price'] - levels['tp1']) * 0.33  # Modifier 0.33 (33%)
```

## Limitations et Considérations

1. **Slippage** : Le script n'inclut pas de slippage. En trading réel, ajoutez un buffer.

2. **Commissions** : Les frais de transaction ne sont pas inclus dans le calcul du PnL.

3. **Liquidité** : Le script assume une liquidité parfaite pour tous les ordres.

4. **Données manquantes** : Assurez-vous que vos données sont complètes (pas de gaps).

5. **Multiple FVGs** : Seul le **premier** FVG de la fenêtre 08:30-09:00 est considéré.

6. **Fin de journée** : Les positions non fermées sont assumées touchées au SL.

## Conseils d'Optimisation

1. **Testez sur différentes périodes** : Séparez vos données en in-sample et out-of-sample.

2. **Walk-forward analysis** : Validez la robustesse de la stratégie.

3. **Paramètres variables** : Testez différentes valeurs de SL et TP.

4. **Filtres additionnels** : Ajoutez des conditions de marché (volatilité, trend, etc.).

5. **Money management** : Implémentez une gestion de capital adaptative.

## Support et Contribution

Pour toute question ou amélioration :
- Documentez vos modifications
- Testez avec des données réelles
- Partagez vos résultats et insights

## License

Ce script est fourni à des fins éducatives et de recherche. Utilisez-le à vos propres risques en trading réel.

---

**Auteur** : Développeur Quantitatif  
**Date** : 2025  
**Version** : 1.0
