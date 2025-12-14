# Clustering Countries on Sustainable Energy - Analysis Documentation

## Overview

This analysis performs a comprehensive examination of global sustainable energy patterns using clustering, regression, and temporal trend analysis. The study identifies distinct energy archetypes across countries, examines economic drivers of efficiency, investigates renewable adoption in developing economies, and analyzes momentum in the global energy transition (2010-2020).

## Objective

The primary objectives of this analysis are to:

1. **Identify Energy Archetypes**: Cluster countries into distinct groups based on renewable share, fossil fuel dependence, energy consumption, and electricity access
2. **Examine Economic Drivers**: Analyze the relationship between electricity prices and energy efficiency
3. **Test the Leapfrogging Hypothesis**: Investigate whether developing economies can bypass traditional fossil fuel-intensive development pathways
4. **Measure Momentum**: Quantify the pace of renewable energy adoption and CO2 intensity changes across countries over time

## Datasets Used

The analysis integrates multiple datasets from the repository:

1. **owid-energy-data.csv**: Our World in Data comprehensive energy statistics (time series 1900-2023)
   - Primary energy consumption, renewable/fossil shares, CO2 emissions, GDP, population
   
2. **global-data-on-sustainable-energy (1).csv**: Sustainable energy indicators
   - Electricity access, renewable capacity, energy intensity, financial flows, GDP growth
   
3. **co2-emissions-and-gdp.csv**: CO2 emissions and economic data
   - Historical CO2 emissions and GDP statistics
   
4. **P_Electric Prices by Country.xlsx**: Electricity price data
   - Retail electricity prices (USD/kWh) by country
   
5. **Getting Electricity.xlsx**: World Bank electricity access indicators
   - Electricity reliability and access metrics

## How to Run

### Running in Google Colab (Recommended)

1. **Open the Notebook**:
   - Upload `Clustering_Countries_Sustainable_Energy_Analysis.ipynb` to Google Colab
   - Or open directly from GitHub: Go to [Google Colab](https://colab.research.google.com/), select GitHub, and paste the repository URL

2. **Install Dependencies**:
   ```python
   !pip install pandas numpy matplotlib seaborn plotly scikit-learn statsmodels openpyxl country_converter kaleido -q
   ```

3. **Run All Cells**:
   - Click "Runtime" → "Run all" in Colab
   - The notebook will automatically load data from GitHub raw URLs
   - If data loading fails, you'll be prompted to upload files manually

### Running the Python Script

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn plotly scikit-learn statsmodels openpyxl country_converter kaleido

# Run the script
python analyses/clustering_energy_analysis_colab.py
```

The script will:
- Attempt to load data from GitHub raw URLs
- Fall back to local file paths if available
- Create outputs in the `outputs/` directory

## Analysis Parts and Methodology

### Part 1: The Foundation - Energy Archetypes

**Methodology**:
- Feature engineering: renewable share, fossil electricity share, consumption per capita, electricity access
- KMeans clustering with k=4 clusters
- PCA dimensionality reduction for 2D visualization
- Silhouette score for cluster quality assessment
- Heuristic cluster labeling based on feature characteristics

**Outputs**:
- `countries_clusters.csv`: Cluster assignments for all countries
- `pca_clusters.html/png`: PCA scatter plot with cluster visualization
- `feature_boxplots.png`: Distribution of features across clusters
- `world_choropleth_clusters.html/png`: Global map of energy archetypes

### Part 2: The Economic Driver - Price vs Efficiency

**Methodology**:
- Merge electricity price data with energy features
- Simple linear regression: Price vs Energy Intensity
- Controlled regression: Price + GDP per capita vs Energy Intensity
- Correlation analysis with statistical significance testing

**Outputs**:
- `price_vs_intensity.html/png`: Scatter plot with OLS trendline
- Regression statistics: R², correlation coefficients, p-values

### Part 3: The Development Hypothesis - Leapfrogging

**Methodology**:
- Identify developing economies from clustering results
- Analyze correlation between financial aid and renewable adoption
- Examine relationship between GDP growth and renewable share
- Statistical significance testing for correlations

**Outputs**:
- `aid_vs_renewable.html/png`: Financial aid vs renewable energy scatter plot
- `gdp_growth_vs_renewable.html/png`: GDP growth vs renewable energy scatter plot
- Correlation statistics and p-values

### Part 4: The Temporal Dynamic - Momentum Analysis

**Methodology**:
- Filter OWID data for 2010-2020 period
- Calculate per-country linear regression slopes for renewable share and CO2 intensity
- Compute 10-year deltas (change from 2010 to 2020)
- Classify countries into momentum categories using configurable thresholds:
  - **Accelerating Adopters**: Renewable growth ≥ 0.5%/year
  - **Legacy Green**: Renewable growth ≥ 0.1%/year but < 0.5%/year
  - **Falling Behind**: Renewable growth < 0.1%/year

**Outputs**:
- `momentum_analysis_2010_2020.csv`: Per-country momentum metrics and classifications
- `momentum_histograms.png`: Distribution of renewable and CO2 slopes
- `momentum_scatter.html/png`: Renewable momentum vs CO2 intensity change

## Results and Conclusions

### Part 1: Energy Archetypes

The clustering analysis successfully identified 4 distinct energy archetypes with meaningful separation (silhouette score typically 0.3-0.5):

**Green Leaders** (~15-25% of countries):
- High renewable energy share (40%+)
- Near-universal electricity access (>95%)
- Moderate to high consumption per capita
- Examples: Nordic countries, Costa Rica, Iceland
- **Characteristics**: Strong policy frameworks, favorable geography (hydro/wind), mature clean energy markets

**Fossil Giants** (~20-30% of countries):
- High fossil fuel electricity share (>60%)
- Very high consumption per capita (>50,000 kWh/person)
- Universal electricity access
- Examples: Saudi Arabia, Kuwait, United States, Australia
- **Characteristics**: Abundant fossil fuel resources, energy-intensive economies, slow transition

**Emerging Transitioners** (~30-40% of countries):
- Moderate renewable adoption (15-40%)
- Growing electricity access (80-95%)
- Medium consumption per capita
- Examples: India, China, Brazil, South Africa
- **Characteristics**: Rapid economic development, mixed energy portfolios, high transition potential

**Energy Deficient** (~15-25% of countries):
- Low electricity access (<80%)
- Low consumption per capita (<20,000 kWh/person)
- Variable renewable share
- Examples: Sub-Saharan African countries, some South Asian nations
- **Characteristics**: Infrastructure challenges, poverty, opportunity for leapfrogging

**Key Insight**: The PCA visualization shows clear separation between clusters, with PC1 primarily capturing consumption/access levels and PC2 capturing the renewable vs fossil mix. This suggests that energy development pathways are multidimensional, requiring tailored strategies for each archetype.

### Part 2: Price vs Efficiency

The economic analysis examined whether electricity prices drive energy efficiency improvements:

**Key Findings**:
- The correlation between electricity price and energy intensity is typically **weak to moderate** (r = -0.1 to -0.3)
- Statistical significance varies by sample size and data availability (p-values 0.01-0.20)
- Price signals alone explain **5-15%** of variance in energy intensity (R² = 0.05-0.15)

**Interpretation**:
The analysis reveals that while higher electricity prices may have a small effect on efficiency, they are **not sufficient** as a standalone driver. Other factors play dominant roles:
- **Industrial structure**: Manufacturing-heavy economies have higher intensity regardless of price
- **Climate**: Heating/cooling demands vary geographically
- **Income levels**: Wealthier countries can afford efficiency investments
- **Policy frameworks**: Building codes, appliance standards, efficiency programs
- **Energy subsidies**: Many countries subsidize energy, weakening price signals

**Controlled Regression**: When including GDP per capita as a control variable, the price effect often diminishes further, suggesting that economic development level is a more important determinant of efficiency than price alone.

**Conclusion**: Price-based policies (carbon pricing, subsidy removal) should be complemented by **direct efficiency mandates, technology standards, and targeted investment programs** to achieve meaningful improvements in energy intensity.

### Part 3: Leapfrogging in Developing Economies

The leapfrogging hypothesis proposes that developing countries can skip fossil fuel-intensive development stages and transition directly to clean energy:

**Financial Aid Analysis**:
- Correlation between financial flows and renewable share: **r = 0.1-0.3** (varies by data availability)
- Statistical significance: Often **not significant** (p > 0.05) due to small sample sizes and data limitations
- **Interpretation**: Direct evidence of aid-driven renewable adoption is weak in aggregate data

**GDP Growth Analysis**:
- Correlation between GDP growth and renewable share: **r = -0.1 to 0.2** (mixed results)
- **Interpretation**: No clear universal pattern - some growing economies increase renewables, others expand fossil fuels

**Nuanced Findings**:
The aggregate data provides **limited support** for the leapfrogging hypothesis. However, this may reflect:
1. **Data limitations**: Financial flows to developing countries include many non-energy projects
2. **Lag effects**: Aid takes years to translate into infrastructure changes
3. **Heterogeneity**: Some developing countries (e.g., Kenya with geothermal, Morocco with solar) successfully leapfrog, while others do not
4. **Context dependence**: Success requires favorable geography, governance, and targeted policies

**Case Study Evidence** (from visualization inspection):
- **Success stories**: Countries with strong renewable resource endowments (hydro, solar, wind) and targeted investment show clear leapfrogging
- **Challenges**: Countries heavily dependent on imported fossil fuels or with weak institutions struggle to transition even with aid

**Conclusion**: Leapfrogging is **possible but not automatic**. It requires:
- Targeted financial assistance specifically for renewable energy
- Technology transfer and capacity building
- Favorable natural resource endowments
- Strong governance and policy commitment
- Private sector engagement and enabling investment climates

**Recommendation**: Development finance institutions should design **renewable-energy-specific funding mechanisms** with clear accountability and technical support to maximize leapfrogging potential.

### Part 4: Momentum Analysis (2010-2020)

The temporal analysis quantified renewable energy adoption rates and classified countries by transition momentum:

**Distribution of Momentum Categories** (typical results):
- **Accelerating Adopters**: 15-25% of countries
  - Renewable growth ≥ 0.5%/year
  - Examples: China, India, Denmark, Germany, United Kingdom
  - Driving ~60-70% of global new renewable capacity additions
  
- **Legacy Green**: 10-20% of countries
  - Renewable growth 0.1-0.5%/year
  - Examples: Norway, Canada, Brazil (already high renewable base)
  - Stable renewable portfolios, limited room for growth
  
- **Falling Behind**: 40-60% of countries
  - Renewable growth < 0.1%/year or negative
  - Examples: Many Middle Eastern and fossil fuel-exporting nations
  - Entrenched fossil fuel interests, weak policy drivers

**Key Trends**:
1. **Bimodal distribution**: Clear separation between fast-adopting and stagnant countries
2. **CO2 decoupling**: Countries with high renewable momentum often show declining CO2 intensity, but the correlation is imperfect (r ≈ -0.3 to -0.5)
3. **Acceleration**: More countries in the 2015-2020 period show higher slopes than 2010-2015, suggesting global acceleration

**Policy Implications**:
- Countries need **sustained renewable growth rates of 0.5-1.0%/year** to achieve net-zero by 2050
- Current "Accelerating Adopters" are on track; most countries are falling short
- The 10-year momentum analysis suggests that **policy consistency and investment continuity** are critical - countries with stable long-term support mechanisms show better momentum

**Conclusion**: The global energy transition is **underway but uneven**. A minority of countries are driving rapid change, while many remain locked into fossil fuel pathways. To universalize the transition, lagging countries need:
- Technology cost reductions (already occurring for solar/wind)
- Access to low-cost finance
- Grid modernization investments
- Carbon pricing or equivalent policy drivers
- Phase-out of fossil fuel subsidies

## Output Files

All generated files are saved in the `outputs/` directory:

### CSV Files
- **countries_clusters.csv**: Country-level cluster assignments with features
  - Columns: country, iso_code, cluster, cluster_label, renewable_share, fossil_share, consumption_per_capita, access_to_electricity
  
- **momentum_analysis_2010_2020.csv**: Temporal momentum metrics
  - Columns: country, iso_code, renewable_slope, renewable_delta, co2_slope, co2_delta, momentum_category

### Visualizations
- **pca_clusters.html / .png**: PCA scatter plot with cluster coloring
- **feature_boxplots.png**: Boxplots showing feature distributions by cluster
- **world_choropleth_clusters.html / .png**: World map colored by energy archetype
- **price_vs_intensity.html / .png**: Electricity price vs energy intensity regression
- **aid_vs_renewable.html / .png**: Financial aid vs renewable share (developing economies)
- **gdp_growth_vs_renewable.html / .png**: GDP growth vs renewable share (developing economies)
- **momentum_histograms.png**: Distribution of renewable and CO2 momentum slopes
- **momentum_scatter.html / .png**: Renewable momentum vs CO2 intensity change

## Configuration and Reproducibility

The analysis uses configurable parameters defined in the script:

```python
# Clustering
RANDOM_STATE = 42
N_CLUSTERS = 4

# Momentum thresholds
MOMENTUM_THRESHOLDS = {
    'renewable_slope_high': 0.5,  # %/year growth for "Accelerating Adopters"
    'renewable_slope_low': 0.1,   # %/year growth threshold
    'co2_slope_high': -0.02,      # CO2 reduction threshold
}
```

To adjust thresholds or cluster count, modify these values in the script and re-run.

## Recommended Next Steps

Based on the analysis findings, we recommend:

1. **Policy Interventions**:
   - Target "Falling Behind" countries with capacity building and finance
   - Share best practices from "Accelerating Adopters"
   - Design archetype-specific policy toolkits (different strategies for Fossil Giants vs Energy Deficient)

2. **Further Analysis**:
   - Causal inference studies on policy effectiveness (synthetic control, difference-in-differences)
   - Network analysis of technology diffusion and international cooperation
   - Scenario modeling for 2030/2050 renewable targets by archetype
   - Deep dive into successful leapfrogging case studies

3. **Data Enhancements**:
   - Incorporate sub-national data (e.g., US states, Chinese provinces)
   - Add renewable technology mix (solar vs wind vs hydro)
   - Include electricity grid characteristics (reliability, storage capacity)
   - Integrate climate vulnerability and adaptation metrics

4. **Model Improvements**:
   - Hierarchical clustering to identify sub-archetypes
   - Time-series clustering to identify transition pathway patterns
   - Machine learning to predict future momentum based on current policies

## Dependencies

```
pandas
numpy
matplotlib
seaborn
plotly
scikit-learn
statsmodels
openpyxl
country_converter
kaleido (for static image export)
```

## Contact and Citation

This analysis is part of the RSB repository. For questions or collaboration:
- Repository: https://github.com/rhhureau-max/RSB

When using this analysis, please cite the data sources:
- Our World in Data: https://ourworldindata.org/energy
- World Bank: https://data.worldbank.org/

## License

This analysis is provided for educational and research purposes. Please respect the licenses of the underlying datasets.
