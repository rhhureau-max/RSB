# RSB

## Shifting Perspectives: From Static Status to Transition Velocity

### Introduction & Research Question

Rather than merely assessing current sustainability levels ('Who is green today?'), this project aims to identify the momentum of change. Our central research question is:

> **Can clustering algorithms effectively distinguish between 'Legacy Green' nations—those with historically high reliance on hydro or biomass but stagnating growth—and 'Accelerating Adopters'—nations aggressively deploying new solar and wind capacity?**

### Problem Statement & Justification

This approach addresses a common limitation in standard clustering, where countries with vastly different energy trajectories (e.g., Norway, with established hydro infrastructure, vs. Germany, with active transition policies) are often grouped together. By focusing on dynamic rates of change rather than static snapshots, we isolate the current political and economic effort toward decarbonization.

### Methodology (Feature Engineering)

To capture these temporal dynamics, we moved beyond raw metrics and performed Feature Engineering to calculate the 'slope' of change over a decade:

| Feature | Formula | Description |
|---------|---------|-------------|
| **10-Year Renewable Delta** | $Value_{2020} - Value_{2010}$ | Measures adoption acceleration |
| **Decarbonization Rate** | 10-year change in CO2 intensity | Tracks carbon intensity reduction |
| **GDP-Adjusted Growth** | Used as a control variable | Contextualizes energy demand |

### Data Sources

This analysis utilizes the following datasets:
- `co2-emissions-and-gdp.csv` - CO2 emissions and GDP data by country and year
- `global-data-on-sustainable-energy (1).csv` - Comprehensive sustainable energy metrics including renewable capacity, electricity generation, and energy consumption