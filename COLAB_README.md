# 🌐 Utilisation avec Google Colab

## 🚀 Démarrage Rapide

### Méthode 1: Ouvrir Directement (Le Plus Simple)

Cliquez sur ce badge pour ouvrir le notebook dans Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/rhhureau-max/RSB/blob/copilot/analyze-pdf-files/NVIDIA_Analysis_Colab.ipynb)

### Méthode 2: Import Manuel

1. Téléchargez le fichier `NVIDIA_Analysis_Colab.ipynb`
2. Allez sur [Google Colab](https://colab.research.google.com/)
3. Menu: **Fichier** → **Importer le notebook**
4. Sélectionnez l'onglet **Importer**
5. Cliquez sur **Choisir un fichier** et sélectionnez le `.ipynb`

---

## 📊 Contenu du Notebook

Le notebook Colab contient **tous les 3 projets** dans un seul fichier:

### 1️⃣ Projet 1: Analyse d'Investissement IA
- Calcul VAN, TRI, Payback, Profitability Index
- Simulation Monte Carlo (10,000 scénarios)
- Visualisations interactives

### 2️⃣ Projet 2: Séries Temporelles
- Modèle ARIMA pour prévisions de prix
- Modèle GARCH pour volatilité
- Tests de stationnarité

### 3️⃣ Projet 3: Time Value of Money
- Calculs PV/FV
- Analyse des annuités
- Valorisation d'obligations

---

## ▶️ Comment Exécuter

### Option A: Exécuter Tout d'Un Coup

1. Ouvrez le notebook dans Colab
2. Menu: **Exécution** → **Tout exécuter**
3. Attendez 5-10 minutes
4. Les résultats s'affichent automatiquement

### Option B: Exécuter Cellule par Cellule

1. Cliquez sur une cellule de code
2. Appuyez sur **Shift + Enter** ou cliquez sur le bouton ▶️
3. Passez à la cellule suivante
4. Répétez pour chaque cellule

---

## ✅ Avantages de Google Colab

- **✅ Gratuit** - Pas besoin de payer pour du calcul cloud
- **✅ Aucune Installation** - Tout fonctionne dans le navigateur
- **✅ GPU Disponible** - Accélération possible si nécessaire
- **✅ Sauvegarde Automatique** - Dans Google Drive
- **✅ Partage Facile** - Partagez le lien avec d'autres
- **✅ Visualisations Intégrées** - Graphiques affichés directement

---

## 📝 Instructions Détaillées

### Première Utilisation

1. **Connexion Google**: Vous devez avoir un compte Google
2. **Ouvrir Colab**: Utilisez le lien ou importez le notebook
3. **Installer les Packages**: La première cellule installe automatiquement tout
4. **Exécuter**: Lancez l'exécution cellule par cellule ou tout d'un coup

### Installation Automatique

La première cellule du notebook installe automatiquement:
```python
!pip install -q yfinance pandas numpy matplotlib seaborn scipy statsmodels arch numpy-financial
```

Cela prend ~1-2 minutes la première fois.

### Téléchargement des Données

Les données NVIDIA sont téléchargées automatiquement depuis Yahoo Finance:
- Pas besoin de fichiers locaux
- Données toujours à jour
- Gratuit et légal

---

## 🎯 Résultats Attendus

Après exécution complète, vous obtenez:

### Projet 1
```
VAN: $117.75M ✅
TRI: 22.11% ✅
Probabilité Succès: 75% ✅
```

### Projet 2
```
ARIMA: Prévisions de prix
GARCH: Modèle de volatilité
Tests: Stationnarité confirmée
```

### Projet 3
```
PV/FV: Exemples calculés
Obligations: Prix = $926.40
Annuités: Épargne retraite modélisée
```

### Visualisations
- Graphique Monte Carlo (distribution VAN)
- Prévisions ARIMA vs Prix réels
- Autres graphiques financiers

---

## ⚠️ Notes Importantes

### Limite de Temps
- Google Colab peut se déconnecter après 90 minutes d'inactivité
- Sauvegardez vos résultats avant de fermer

### Performance
- L'exécution complète prend 5-10 minutes
- La simulation Monte Carlo (10,000 itérations) prend ~30 secondes
- Le téléchargement de données peut varier selon la connexion

### Données
- Les données sont téléchargées en temps réel depuis Yahoo Finance
- Les résultats peuvent varier légèrement selon la date d'exécution
- Les calculs utilisent les dernières données disponibles

---

## 🔧 Dépannage

### Erreur: "Module not found"
**Solution**: Réexécutez la première cellule d'installation

### Erreur de Connexion
**Solution**: Vérifiez votre connexion Internet, Yahoo Finance doit être accessible

### Notebook ne Répond Plus
**Solution**: 
1. Menu: **Exécution** → **Redémarrer l'exécution**
2. Réexécutez toutes les cellules

### Graphiques ne s'Affichent Pas
**Solution**: Assurez-vous que `%matplotlib inline` est exécuté dans la cellule d'imports

---

## 💾 Sauvegarder les Résultats

### Sauvegarder le Notebook
1. Menu: **Fichier** → **Enregistrer une copie dans Drive**
2. Le notebook est sauvegardé dans votre Google Drive

### Télécharger les Graphiques
1. Clic droit sur un graphique
2. **Enregistrer l'image sous...**

### Exporter les Résultats
```python
# Dans une cellule, ajoutez:
# Pour sauvegarder les résultats dans un fichier
with open('resultats_nvidia.txt', 'w') as f:
    f.write(f"VAN: ${npv/1e6:.2f}M\\n")
    f.write(f"TRI: {irr:.2%}\\n")

# Télécharger le fichier
from google.colab import files
files.download('resultats_nvidia.txt')
```

---

## 📚 Ressources

- **Documentation Colab**: [colab.research.google.com](https://colab.research.google.com/)
- **Guide Colab**: [Guide Officiel](https://colab.research.google.com/notebooks/intro.ipynb)
- **Support**: Voir `START_HERE.md` et `EXECUTION_GUIDE.md`

---

## ✨ Pourquoi Colab?

Google Colab est **parfait** pour ce projet car:

1. **Simplicité**: Pas d'installation Python locale nécessaire
2. **Accessibilité**: Fonctionne sur n'importe quel ordinateur avec navigateur
3. **Partage**: Facile à partager avec collègues ou professeurs
4. **Gratuit**: Calcul cloud gratuit avec Google Account
5. **Interactif**: Modifiez et réexécutez facilement

---

**Version**: 1.0  
**Date**: Décembre 2025  
**Status**: ✅ Testé et Fonctionnel
