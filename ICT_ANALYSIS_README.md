# ICT Midnight Open Analysis - Documentation

## Vue d'ensemble

Ce script Python analyse une statistique ICT (Inner Circle Trader) importante : la probabilité que le prix du Nasdaq (NQ) revienne toucher son prix d'ouverture de minuit (Midnight Open) durant la session de Londres (London Killzone).

## Concepts Clés

### Midnight Open (MO)
- **Définition** : Prix d'ouverture (Open) de la bougie à 23:00 heure de Chicago
- **Importance** : Niveau clé utilisé par les traders ICT comme point de référence

### London Killzone (KZ)
- **Période** : 01:00 - 05:00 heure de Chicago (1h du matin à 5h du matin)
- **Objectif** : Période où l'on analyse si le prix revient toucher le MO

### Logique de "Touche"
Une touche est validée quand, pour une bougie de 1 minute donnée :
```
Low <= Midnight Open <= High
```

## Prérequis

### Dépendances Python
```bash
pip install pandas numpy matplotlib
```

### Format des Données
Le fichier CSV doit contenir les colonnes suivantes :
- `Date` : Date de la bougie (format : YYYY-MM-DD ou similaire)
- `Time` : Heure de la bougie (format : HH:MM:SS ou HH:MM)
- `Open` : Prix d'ouverture
- `High` : Prix le plus haut
- `Low` : Prix le plus bas
- `Close` : Prix de clôture

**Important** : Les données doivent être en horaire de Chicago (US/Central timezone)

### Exemple de Format CSV
```csv
Date,Time,Open,High,Low,Close
2024-01-02,00:00,15234.50,15236.25,15232.75,15235.00
2024-01-02,00:01,15235.00,15237.50,15234.00,15236.75
...
```

## Installation et Utilisation

### 1. Installation des Dépendances
```bash
pip install pandas numpy matplotlib
```

### 2. Préparer vos Données
- Assurez-vous que votre fichier CSV suit le format décrit ci-dessus
- Vérifiez que les données sont en horaire de Chicago
- Les données doivent être en résolution de 1 minute (M1)

### 3. Exécuter le Script

#### Méthode 1 : Ligne de commande avec argument
```bash
python ict_midnight_open_analysis.py /chemin/vers/votre/NQ_data.csv
```

#### Méthode 2 : Modification du script
Éditez le script et modifiez la ligne suivante :
```python
csv_path = "NQ_M1_data.csv"  # Remplacez par le chemin de votre fichier
```
Puis exécutez :
```bash
python ict_midnight_open_analysis.py
```

## Sorties du Script

### 1. Affichage Console
Le script affiche dans la console :
- Informations de chargement des données
- Nombre de jours analysés
- Nombre de jours avec touche du MO
- Taux de réussite global (pourcentage)
- Statistiques détaillées par jour de la semaine

### 2. Fichier CSV de Résultats
**Fichier** : `ict_midnight_open_results.csv`

Contient pour chaque jour :
- Date
- Prix du Midnight Open
- Si le MO a été touché (True/False)
- Jour de la semaine
- Nombre de bougies dans la Killzone

### 3. Graphique Visuel
**Fichier** : `ict_midnight_open_analysis.png`

Le graphique contient 4 sous-graphiques :
1. **Taux de Réussite Global** (Pie Chart)
   - Proportion de jours avec touche vs sans touche
   
2. **Touches par Jour de la Semaine** (Bar Chart)
   - Nombre de touches pour chaque jour (Lundi à Dimanche)
   
3. **Taux de Réussite par Jour** (Line Chart)
   - Pourcentage de réussite pour chaque jour de la semaine
   - Comparé à la moyenne globale
   
4. **Série Temporelle** (Scatter Plot)
   - Touches sur les 100 derniers jours
   - Moyenne mobile pour identifier les tendances

## Exemple de Résultats

```
============================================================
STATISTICAL RESULTS
============================================================

Total Trading Days Analyzed: 1247
Days where MO was touched during KZ: 856
Days where MO was NOT touched during KZ: 391

Success Rate (MO Touch): 68.64%

------------------------------------------------------------
BREAKDOWN BY DAY OF WEEK
------------------------------------------------------------

Day of Week Statistics:
Monday      : 178/249 touches (71.49%)
Tuesday     : 172/251 touches (68.53%)
Wednesday   : 165/250 touches (66.00%)
Thursday    : 169/248 touches (68.15%)
Friday      : 172/249 touches (69.08%)
```

## Interprétation des Résultats

### Taux de Réussite Élevé (>60%)
Indique une forte probabilité de retour au Midnight Open durant la Killzone. Peut être utilisé comme base pour des stratégies de trading.

### Variations par Jour de la Semaine
Certains jours peuvent montrer des taux plus élevés que d'autres. Ces informations peuvent aider à :
- Identifier les meilleurs jours pour trader cette configuration
- Ajuster la taille de position selon le jour
- Éviter certains jours avec des taux plus faibles

### Tendances Temporelles
La série temporelle peut révéler :
- Périodes de forte cohérence (clustering de touches)
- Changements de comportement du marché au fil du temps
- Validation de la robustesse de la statistique

## Personnalisation du Script

### Modifier la Killzone
Pour changer les heures de la Killzone, modifiez dans la fonction `analyze_killzone_touches` :
```python
kz_start = pd.Timestamp(next_day.date()).replace(hour=1, minute=0, tzinfo=df.index.tz)
kz_end = pd.Timestamp(next_day.date()).replace(hour=5, minute=0, tzinfo=df.index.tz)
```

### Modifier le Midnight Open
Pour changer l'heure du Midnight Open, modifiez dans la fonction `identify_midnight_open` :
```python
midnight_opens = df[df.index.time == time(23, 0)]  # 23:00 Chicago time
```

### Ajouter d'Autres Analyses
Le script est modulaire. Vous pouvez facilement ajouter :
- Analyse de la distance moyenne jusqu'à la touche
- Temps moyen avant la touche
- Corrélations avec d'autres indicateurs
- Filtres de volatilité ou de volume

## Résolution de Problèmes

### Erreur : "Could not find date/time columns in CSV"
- Vérifiez que votre CSV contient bien les colonnes `Date` et `Time`
- Les noms de colonnes peuvent varier (date/Date, time/Time)
- Le script tente de gérer différentes variations

### Erreur : "Missing required columns"
- Assurez-vous que les colonnes OHLC sont présentes
- Les noms peuvent être en majuscules ou minuscules

### Pas de Données de Killzone
- Vérifiez que vos données couvrent bien la période 01:00-05:00
- Confirmez que le timezone est correctement configuré (Chicago/US/Central)

### Graphique ne s'affiche pas
- Vérifiez que matplotlib est installé
- Le graphique est également sauvegardé comme fichier PNG

## Support et Contributions

Ce script est conçu pour être :
- **Facile à utiliser** : Interface simple avec documentation claire
- **Robuste** : Gestion des erreurs et validation des données
- **Flexible** : Facilement personnalisable pour d'autres analyses
- **Complet** : Sorties multiples (console, CSV, graphiques)

Pour toute question ou amélioration, n'hésitez pas à contribuer !

## Licence

Script open-source pour l'analyse de données de trading.

## Avertissement

Ce script est fourni à des fins éducatives et d'analyse. Les résultats passés ne garantissent pas les performances futures. Utilisez ces informations à vos propres risques dans vos décisions de trading.
