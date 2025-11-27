import pandas as pd
import numpy as np

# Charger le fichier CSV dans un DataFrame
df = pd.read_csv('owid-energy-data.csv')

# Afficher les 5 premières lignes
print("=" * 80)
print("LES 5 PREMIÈRES LIGNES DU DATAFRAME")
print("=" * 80)
print(df.head())
print("\n")

# Afficher les informations sur les colonnes (types et valeurs manquantes)
print("=" * 80)
print("INFORMATIONS SUR LES COLONNES")
print("=" * 80)
print(df.info())
print("\n")

# Afficher un résumé des valeurs manquantes par colonne
print("=" * 80)
print("RÉSUMÉ DES VALEURS MANQUANTES PAR COLONNE")
print("=" * 80)
missing_values = df.isnull().sum()
missing_percentage = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Colonne': missing_values.index,
    'Valeurs manquantes': missing_values.values,
    'Pourcentage (%)': missing_percentage.values
})
print(missing_df.to_string(index=False))
print("\n")

# Filtrer les données pour la période 2004-2019
print("=" * 80)
print("FILTRAGE DES DONNÉES (2004-2019)")
print("=" * 80)

if 'year' in df.columns:
    df_filtered = df[(df['year'] >= 2004) & (df['year'] <= 2019)]
    print(f"Nombre total d'entrées dans le dataset complet: {len(df)}")
    print(f"Nombre d'entrées pour la période 2004-2019: {len(df_filtered)}")
    print(f"Années disponibles: {sorted(df_filtered['year'].unique())}")
    print("\n")
else:
    print("⚠ ATTENTION: La colonne 'year' n'existe pas!")
    df_filtered = df

# Vérifier le nombre de valeurs non nulles pour 'greenhouse_gas_emissions'
# pour les années 2019 et 2020
print("=" * 80)
print("ANALYSE DE LA COLONNE 'greenhouse_gas_emissions'")
print("=" * 80)

# Vérifier si la colonne existe
if 'greenhouse_gas_emissions' in df.columns:
    # Analyse pour chaque année de 2004 à 2019
    print("\nNombre de valeurs non nulles par année (2004-2019):")
    print("-" * 60)
    
    yearly_stats = []
    for year in range(2004, 2020):
        df_year = df_filtered[df_filtered['year'] == year] if 'year' in df_filtered.columns else pd.DataFrame()
        non_null = df_year['greenhouse_gas_emissions'].notna().sum()
        total = len(df_year)
        null_count = total - non_null
        percentage = (non_null/total)*100 if total > 0 else 0
        
        yearly_stats.append({
            'Année': year,
            'Total entrées': total,
            'Valeurs non nulles': non_null,
            'Valeurs manquantes': null_count,
            'Pourcentage disponible': f"{percentage:.2f}%"
        })
        
        print(f"{year}: {non_null}/{total} valeurs disponibles ({percentage:.2f}%)")
    
    # Créer un DataFrame avec les statistiques annuelles
    stats_df = pd.DataFrame(yearly_stats)
    print("\n")
    print("=" * 80)
    print("TABLEAU RÉCAPITULATIF")
    print("=" * 80)
    print(stats_df.to_string(index=False))
    print("\n")
    
    # Analyse spécifique pour 2019 (année de fin)
    df_2019 = df_filtered[df_filtered['year'] == 2019] if 'year' in df_filtered.columns else pd.DataFrame()
    non_null_2019 = df_2019['greenhouse_gas_emissions'].notna().sum()
    total_2019 = len(df_2019)
    
    print("=" * 80)
    print("ANALYSE DÉTAILLÉE POUR L'ANNÉE 2019 (année de fin)")
    print("=" * 80)
    print(f"Nombre total d'entrées: {total_2019}")
    print(f"Valeurs non nulles: {non_null_2019}")
    print(f"Valeurs manquantes: {total_2019 - non_null_2019}")
    if total_2019 > 0:
        print(f"Pourcentage de données disponibles: {(non_null_2019/total_2019)*100:.2f}%")
    print()
    
    # Statistiques par pays pour la période complète
    if 'country' in df_filtered.columns:
        print("=" * 80)
        print("NOMBRE DE PAYS AVEC DONNÉES PAR ANNÉE")
        print("=" * 80)
        for year in range(2004, 2020):
            df_year = df_filtered[df_filtered['year'] == year]
            countries_with_data = df_year[df_year['greenhouse_gas_emissions'].notna()]['country'].nunique()
            total_countries = df_year['country'].nunique()
            print(f"{year}: {countries_with_data}/{total_countries} pays avec données")
        print("\n")
    
    # Afficher les statistiques descriptives pour toute la période
    print("=" * 80)
    print("STATISTIQUES DESCRIPTIVES DES ÉMISSIONS GES (2004-2019)")
    print("=" * 80)
    print(df_filtered['greenhouse_gas_emissions'].describe())
    print("\n")
    
    # Top 10 des pays avec les émissions moyennes les plus élevées (2004-2019)
    if 'country' in df_filtered.columns:
        print("=" * 80)
        print("TOP 10 DES PAYS - ÉMISSIONS MOYENNES GES (2004-2019)")
        print("=" * 80)
        avg_emissions = df_filtered.groupby('country')['greenhouse_gas_emissions'].mean().sort_values(ascending=False).head(10)
        for i, (country, emission) in enumerate(avg_emissions.items(), 1):
            print(f"{i:2d}. {country}: {emission:.2f}")
        print("\n")
    
    # Recommandation
    print("=" * 80)
    print("RECOMMANDATION")
    print("=" * 80)
    print(f"✓ Période d'analyse recommandée: 2004-2019")
    print(f"✓ Colonne à utiliser: 'greenhouse_gas_emissions'")
    print(f"✓ Nombre total d'observations: {len(df_filtered)}")
    print(f"✓ Données disponibles pour les émissions: {df_filtered['greenhouse_gas_emissions'].notna().sum()}")
    
else:
    print("⚠ ATTENTION: La colonne 'greenhouse_gas_emissions' n'existe pas dans le DataFrame!")
    print("\nColonnes disponibles:")
    for col in df.columns:
        print(f"  - {col}")
    
    # Recherche de colonnes similaires
    print("\n" + "=" * 80)
    print("RECHERCHE DE COLONNES LIÉES AUX ÉMISSIONS")
    print("=" * 80)
    emission_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['emission', 'co2', 'greenhouse', 'gas'])]
    if emission_columns:
        print("Colonnes liées aux émissions trouvées:")
        for col in emission_columns:
            print(f"  - {col}")
    else:
        print("Aucune colonne liée aux émissions trouvée.")
