# Hidden Climate Risk in Strong Housing Markets

This repository contains the reproducible analytical workflow for the M.Sc.
Major Research Project **Hidden Climate Risk in Strong Housing Markets:
Evidence from Florida County-Level Data**.

The study examines whether strong housing-market performance can coexist with
elevated climate-housing vulnerability and whether housing indicators alone
are sufficient to distinguish that vulnerability. It integrates housing,
physical-risk, disaster, socioeconomic, affordability, flood-insurance, and
spatial information for Florida's 67 counties from 2011 through 2025.

## Study design

- **Unit of analysis:** Florida county-year
- **Study period:** 2011-2025
- **Coverage:** 67 counties and 1,000 county-year observations
- **Integrated feature dataset:** 75 columns
- **Vulnerability dataset:** 123 columns
- **Vulnerability classes:** Low (334), Medium (333), and High (333)
- **Model-development period:** 2011-2022 (799 observations)
- **Later-period held-out evaluation:** 2023-2025 (201 observations)
- **Random seed:** 42

The vulnerability labels were constructed using the complete 2011-2025 panel.
Consequently, the later-period evaluation measures how reliably the constructed
classes can be reproduced; it is not a prospective forecast or an independent
external test.

## Data sources

| Source | Study use | Coverage used |
|---|---|---|
| [Zillow Home Value Index](https://www.zillow.com/research/data/) | Monthly county-level housing values and derived market indicators | 2010-2025; 2010 supplies the appreciation baseline |
| [FEMA National Risk Index](https://www.fema.gov/about/openfema/data-sets/national-risk-index-data) | Coastal-flood risk, hurricane risk, social vulnerability, resilience, and population | County-level source snapshot |
| [OpenFEMA Disaster Declarations Summaries](https://www.fema.gov/openfema-data-page/disaster-declarations-summaries-v2) | Annual, cumulative, recent, and hazard-specific disaster-history indicators | 2011-2025 |
| [American Community Survey 5-year estimates](https://www.census.gov/data/developers/data-sets/acs-5year.html) | Income, poverty, age, disability, tenure, and affordability indicators | 2011-2024; 2025 values are projected in Notebook 02 |
| [OpenFEMA data sets](https://www.fema.gov/about/openfema/data-sets) | National Flood Insurance Program claim counts and payments | 2011-2025 |
| [2025 TIGER/Line county boundaries](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) | County adjacency and final spatial outputs | 2025 county geometry |

Source data remain subject to their providers' terms, documentation, and
revision policies.

## Repository structure

| Path | Contents |
|---|---|
| `data/raw/` | Downloaded source files and fixed raw snapshots |
| `data/interim/source_preparation/` | Notebook 01 outputs |
| `data/interim/county_year/` | Notebook 02 staged outputs and reproducible caches |
| `data/processed/` | The two final analytical datasets |
| `notebooks/` | Ordered analytical workflow from Notebook 01 through Notebook 09 |
| `results/figures/` | Report-ready figures |
| `results/models/` | Fitted classification and clustering objects |
| `results/tables/` | Analytical, diagnostic, and validation exports |
| `src/config.py` | Shared years, random seed, and colour definitions |
| `src/visualization.py` | Reusable export and plotting helpers |

The two final processed datasets are:

```text
data/processed/florida_county_year_features_2011_2025.csv
data/processed/florida_county_year_vulnerability_2011_2025.csv
```

## Environment setup

The workflow was validated with Python 3.12.10. From the repository root:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies and register the notebook kernel:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name climate-risk-housing-valuation --display-name "Python (climate-risk-housing)"
```

Open the repository in VS Code or JupyterLab and select the newly registered
kernel.

## Required inputs and reproducible snapshots

Notebook 01 expects the two original source files below:

```text
data/raw/zillow/County_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv
data/raw/fema_nri/NRI_Table_Counties.csv
```

Notebook 02 also expects:

```text
data/raw/fema_disaster_declarations/DisasterDeclarationsSummaries.csv
data/raw/shapefiles/tl_2025_us_county/tl_2025_us_county.shp
data/raw/acs/acs_county_year_raw_2011_2024.csv
data/interim/county_year/florida_county_adjacency.csv
data/interim/county_year/nfip_county_year_claim_indicators.csv
```

The ACS, county-adjacency, and NFIP files are fixed study snapshots. Notebook 02
uses them by default so an ordinary rerun does not depend on API availability
or silently incorporate later source revisions:

```python
REFRESH_SPATIAL_ADJACENCY = False
REFRESH_ACS_DATA = False
REFRESH_NFIP_DATA = False
```

Set a flag to `True` only when intentionally refreshing that source. Refreshing
ACS data requires a Census API key, supplied through the `CENSUS_API_KEY`
environment variable or the notebook's secure prompt. Refreshed sources can
change the downstream results and should be treated as a new study version.

## Notebook workflow

Run the notebooks from the repository root in numerical order.

| Notebook | Purpose | Main output or dependency |
|---|---|---|
| `01_data_collection_cleaning_and_merging_clean.ipynb` | Clean and merge monthly Zillow and FEMA NRI data | `data/interim/source_preparation/merged_florida_zillow_fema_monthly.csv` |
| `02_county_year_feature_dataset_construction_clean.ipynb` | Construct housing, spatial, disaster, ACS, affordability, and NFIP indicators | `data/processed/florida_county_year_features_2011_2025.csv` |
| `03_exploratory_data_analysis_clean.ipynb` | Examine housing and broader climate-housing patterns | EDA tables and eight figures |
| `04_vulnerability_score_construction_clean.ipynb` | Construct eight sub-scores, the final score, and three classes | `data/processed/florida_county_year_vulnerability_2011_2025.csv` |
| `05_supervised_vulnerability_classification_clean.ipynb` | Compare classifiers using expanding-window validation and the later-period evaluation | Final Logistic Regression pipeline, predictions, coefficients, and model tables |
| `06_feature_group_comparison_clean.ipynb` | Test the information gained by cumulative feature groups | Feature-group tables and four figures |
| `07_unsupervised_vulnerability_profiles_clean.ipynb` | Identify four vulnerability profiles and screen for hidden risk | Cluster assignments, stability results, hidden-risk tables, and fitted objects |
| `08_explainable_ai_analysis_clean.ipynb` | Explain the fitted Logistic Regression model using coefficients and linear SHAP values | Global, grouped, and county-level explanations |
| `09_spatial_maps_and_final_synthesis_clean.ipynb` | Combine 2025 class severity, recent dominant profiles, and hidden-risk status spatially | Final county table, GeoPackage, and four maps |

Notebook 03 is exploratory and does not alter the processed dataset. Notebook
08 requires the saved outputs of Notebooks 05-07, while Notebook 09 requires
the vulnerability and clustering outputs of Notebooks 04 and 07.

## Hyperparameter search

Notebook 05 contains seeded, 25-trial Optuna searches for Random Forest and
XGBoost. The search uses only the five expanding-window validation folds; the
2023-2025 held-out observations are not used inside the Optuna objective.

```python
RUN_HYPERPARAMETER_SEARCH = False
N_OPTUNA_TRIALS = 25
```

With the search flag set to `False`, the notebook uses the stored winning
parameters from the original search for a faster deterministic rerun. Set it to
`True` to repeat both 25-trial searches. Small XGBoost differences can occur
across library versions, which is why the validated XGBoost version is pinned
in `requirements.txt`.

## Expected validation checkpoints

| Stage | Expected result |
|---|---|
| Notebook 01 final monthly panel | 12,767 rows, 18 columns, 67 counties, no duplicate county-months |
| Notebook 02 integrated dataset | 1,000 rows, 75 columns, 67 counties, 2011-2025 |
| Notebook 04 vulnerability dataset | 1,000 rows, 123 columns; class counts 334/333/333 |
| Notebook 05 split | 799 training and 201 later-period observations; 67 predictors |
| Selected classifier | Logistic Regression; accuracy 0.7761, macro F1 0.7687, weighted F1 0.7622 |
| Notebook 07 final profiles | Four profiles; 15 hidden-risk counties and six priority counties |
| Notebook 09 spatial audit | All 67 counties matched; mapping CRS EPSG:3086 |

The selected Logistic Regression confusion matrix is:

| Actual / predicted | Low | Medium | High |
|---|---:|---:|---:|
| Low | 53 | 0 | 0 |
| Medium | 33 | 38 | 8 |
| High | 0 | 4 | 65 |

## Main analytical outputs

- A multidimensional climate-housing vulnerability score and three severity
  classes for 1,000 county-year observations.
- A temporal classification comparison showing that housing indicators alone
  contain limited information about the constructed vulnerability classes.
- Four recurring vulnerability profiles: Lower-Stress Resilient Profile,
  Disaster-Loss Growth Pressure, High-Exposure Latent Risk, and Socioeconomic
  Resilience Stress.
- A sensitivity-tested hidden-risk screen identifying 15 counties, including
  six priority counties.
- Coefficient, SHAP, PCA, transition, stability, and spatial outputs supporting
  interpretation of the final framework.

## Interpretation limits

- The vulnerability score is a study-specific composite rather than an
  externally validated official risk index.
- The later-period evaluation measures class reproducibility, not prospective
  forecasting.
- Clusters are descriptive profiles and their names are interpretive labels.
- SHAP values explain the fitted model's score structure and associations; they
  do not establish causal effects.
- County-level aggregation can conceal within-county variation.

## Repository

Project repository:
[NimrahAltafAdam/climate-risk-housing-valuation](https://github.com/NimrahAltafAdam/climate-risk-housing-valuation)

When reusing the workflow or derived outputs, cite the project title and the
repository, and cite the original data providers separately.