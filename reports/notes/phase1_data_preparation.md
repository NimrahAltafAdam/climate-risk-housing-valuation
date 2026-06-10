# Phase 1: Data Collection, Cleaning, Merging, and Feature Engineering

## Overview

The objective of Phase 1 was to construct a clean, validated, and modeling-ready county-level panel dataset for the Florida housing valuation project.

This phase combined monthly county-level housing prices from Zillow with county-level climate-risk indicators from FEMA's National Risk Index. The final output is an engineered Zillow-FEMA panel dataset that supports the project's main research question:

> Does climate risk improve county-level housing valuation models?

The final engineered dataset contains:

- 11,963 observations
- 67 Florida counties
- Monthly observations from January 2011 to December 2025
- 25 variables
- Zillow housing-price features
- FEMA climate-risk variables
- Engineered temporal, lag, metro, and climate-time interaction features

Final output:

```text
data/processed/engineered_zillow_fema_data.csv
```

---

# 1. Zillow Housing Dataset Processing

## Objective

The Zillow Home Value Index (ZHVI) dataset serves as the primary housing-price source for this project. The goal of the Zillow preprocessing stage was to create a clean Florida county-level housing-price panel that could later be merged with FEMA climate-risk data.

## Initial Dataset Structure

The raw Zillow dataset contained:

- County identifiers
- Geographic information
- Housing-market metadata
- Monthly ZHVI observations from January 2010 to December 2025

Relevant columns were retained to support identification, filtering, merging, and later feature engineering.

## Variables Retained

Identifier and metadata variables:

- `RegionID`
- `SizeRank`
- `RegionName`
- `State`
- `Metro`
- `StateCodeFIPS`
- `MunicipalCodeFIPS`

Housing-price variables:

- Monthly Zillow Home Value Index observations from 2010 to 2025

## Florida Subsetting

The Zillow dataset was filtered to Florida before reshaping.

This was done because:

- The project focuses on Florida counties.
- Filtering before reshaping reduces memory usage.
- It improves computational efficiency.
- The workflow remains scalable to additional states if needed.

After filtering:

- 67 Florida counties remained.

## Wide-to-Long Transformation

The Zillow dataset was originally stored in wide format, with each monthly ZHVI value stored as a separate column. It was reshaped into long format so that each row represented one county-month observation.

This long panel format is required for:

- Time-series analysis
- Lag feature creation
- Panel modeling
- Merging with county-level FEMA variables

After reshaping:

- 12,864 observations
- 67 counties
- Monthly observations from January 2010 to December 2025

## Missing Housing-Price Investigation

Missing values were examined before cleaning.

Housing-price missing values:

- Total missing values: 98

Missing values by county:

| County | Missing Values |
|---|---:|
| Monroe County | 73 |
| Liberty County | 12 |
| Washington County | 12 |
| Dixie County | 1 |

The `Metro` variable also contained missing values, but these were not treated as data errors. Missing `Metro` values indicate counties that are not assigned to a metropolitan area and were later used to create the `is_metro` feature.

## Missing Data Treatment

Missing housing prices were handled based on the structure of missingness.

For Monroe County, Liberty County, and Washington County, missing values occurred at the beginning of the time series. These were treated as leading missing blocks rather than isolated gaps. Observations before each county's first valid housing-price value were removed.

For Dixie County, only one internal missing value remained after removing leading missing blocks. This missing value occurred between valid observations and was linearly interpolated.

This strategy avoided creating artificial historical values for long periods where Zillow had not reported data, while still preserving a reasonable isolated internal observation.

## Zillow Validation Results

After cleaning:

- Duplicate rows: 0
- Invalid housing prices: 0
- Missing `HousingPrice` values: 0
- Unique Florida counties: 67
- Final Zillow observations: 12,767
- Final Zillow variables: 9

Final cleaned Zillow columns:

- `RegionID`
- `SizeRank`
- `RegionName`
- `State`
- `Metro`
- `StateCodeFIPS`
- `MunicipalCodeFIPS`
- `Date`
- `HousingPrice`

---

# 2. FEMA Climate-Risk Dataset Processing

## Objective

The FEMA National Risk Index dataset serves as the primary source of climate-risk information for the project. The goal of the FEMA preprocessing stage was to extract and clean county-level hazard, vulnerability, resilience, and population variables relevant to housing valuation.

## Initial Dataset Structure

The raw FEMA dataset contained:

- 3,232 county-level observations
- 465 variables
- Multiple hazard-specific risk metrics
- County identifiers
- Vulnerability and resilience measures

Unlike the Zillow dataset, the FEMA dataset was already in county-level tabular format and did not require reshaping.

## Variables Retained

Identifier variables:

- `STATE`
- `STATEABBRV`
- `COUNTY`
- `STCOFIPS`

Baseline control variable:

- `POPULATION`

Climate-risk and vulnerability variables:

- `CFLD_RISKS`
- `HRCN_RISKS`
- `SOVI_SCORE`
- `RESL_SCORE`

## Variable Rationale

`POPULATION` was retained as a baseline county characteristic because it captures county size and potential housing demand.

`CFLD_RISKS` was retained because coastal flooding is a central climate-related hazard for Florida and is directly relevant to housing-market risk.

`HRCN_RISKS` was retained because hurricanes are among Florida's most important and economically significant hazards.

`SOVI_SCORE` was retained because social vulnerability may affect how climate exposure translates into local housing-market risk.

`RESL_SCORE` was retained because community resilience may influence how counties respond to and recover from climate-related hazards.

## Florida Subsetting

The FEMA dataset was filtered to Florida counties.

After filtering:

- 67 counties remained.
- County coverage matched the Zillow dataset.

## Missing Coastal Flood Risk Investigation

Initial missing-value checks showed:

| Variable | Missing Values |
|---|---:|
| POPULATION | 0 |
| CFLD_RISKS | 8 |
| HRCN_RISKS | 0 |
| SOVI_SCORE | 0 |
| RESL_SCORE | 0 |

The eight counties with missing `CFLD_RISKS` values were:

- Gadsden
- Hamilton
- Highlands
- Jackson
- Madison
- Osceola
- Polk
- Sumter

These missing values were investigated using additional FEMA coastal-flood variables, including coastal flood event, frequency, exposure, expected annual loss, and risk rating fields.

The investigation showed that all related coastal-flood variables were missing for these counties and that FEMA classified them as not applicable for coastal flooding. This suggested that the missing values did not represent incomplete data collection but rather the absence of meaningful coastal flood exposure.

## Treatment of Missing Coastal Flood Risk Values

The missing `CFLD_RISKS` values were replaced with 0.

Rationale:

- FEMA classified the affected counties as not applicable for coastal flooding.
- Several inland Florida counties already had valid `CFLD_RISKS = 0`.
- A value of 0 consistently represents negligible or absent coastal flood exposure.
- This approach preserves all 67 Florida counties.

## FEMA Validation Results

After cleaning:

- Duplicate rows: 0
- Invalid population values: 0
- Missing selected FEMA variables: 0
- Unique Florida counties: 67
- Final FEMA observations: 67
- Final FEMA variables: 9

Final cleaned FEMA columns:

- `STATE`
- `STATEABBRV`
- `COUNTY`
- `STCOFIPS`
- `POPULATION`
- `CFLD_RISKS`
- `HRCN_RISKS`
- `SOVI_SCORE`
- `RESL_SCORE`

Cleaned FEMA output:

```text
data/processed/cleaned_fema_data.csv
```

---

# 3. Zillow-FEMA Dataset Merging

## Objective

The objective of the merging stage was to combine monthly county-level Zillow housing prices with county-level FEMA climate-risk indicators.

The merged dataset represents a county-month panel where each monthly housing-price observation is linked to static county-level climate-risk measures.

## Merge Key Construction

The FEMA dataset already contained `STCOFIPS`, a five-digit county FIPS identifier.

The cleaned Zillow dataset contained:

- `StateCodeFIPS`
- `MunicipalCodeFIPS`

A matching `STCOFIPS` variable was constructed in the Zillow dataset using:

```text
STCOFIPS = StateCodeFIPS * 1000 + MunicipalCodeFIPS
```

Examples:

| County | StateCodeFIPS | MunicipalCodeFIPS | STCOFIPS |
|---|---:|---:|---:|
| Bay County | 12 | 5 | 12005 |
| Lee County | 12 | 71 | 12071 |
| Clay County | 12 | 19 | 12019 |

## Merge Key Validation

Before merging:

- Zillow unique `STCOFIPS` values: 67
- FEMA unique `STCOFIPS` values: 67
- FIPS codes in Zillow but not FEMA: 0
- FIPS codes in FEMA but not Zillow: 0

This confirmed that all Florida counties matched successfully and no county-name reconciliation was required.

## Merge Procedure

The datasets were merged using `STCOFIPS`.

The merge structure was:

```text
Zillow monthly county panel
+
FEMA county-level risk data
=
Zillow-FEMA county-month panel
```

A left join was used to preserve all Zillow housing-price observations.

## Post-Merge Validation

After merging:

- Total observations: 12,767
- Unique counties: 67
- Duplicate county-month rows: 0
- Missing FEMA climate variables after merge: 0
- No Zillow housing-price observations were lost.

Merged dataset output:

```text
data/processed/merged_zillow_fema_data.csv
```

---

# 4. Feature Engineering

## Objective

The goal of feature engineering was to transform the merged Zillow-FEMA dataset into a modeling-ready panel dataset.

The engineered features were designed to capture:

- Time trends
- Seasonality
- Housing-price persistence
- Metropolitan versus non-metropolitan differences
- Dynamic climate-risk effects over time

## Basic Time Features

### Month

A `Month` variable was extracted from the `Date` column.

Purpose:

- Captures seasonal housing-market patterns.
- Allows models to learn recurring monthly effects.

Validation:

- Missing `Month` values: 0

### TimeIndex

A continuous `TimeIndex` variable was created to represent the passage of time.

Construction:

```text
January 2010 = 0
February 2010 = 1
...
December 2025 = 191
```

Purpose:

- Captures long-run housing-market trends.
- Represents temporal movement separately from seasonal effects.

Validation:

- Missing `TimeIndex` values: 0

## Metropolitan Indicator

A binary `is_metro` variable was created from Zillow's `Metro` field.

Construction:

```text
is_metro = 1 if Metro is available
is_metro = 0 if Metro is missing
```

Purpose:

- Provides a simple metropolitan versus non-metropolitan classification.
- Helps distinguish urban and rural housing-market differences.

Validation:

| is_metro | Count |
|---|---:|
| 1 | 9,719 |
| 0 | 3,048 |

Missing `is_metro` values: 0

## Housing-Price Lag Features

Housing-price lag features were created separately within each county using `groupby(STCOFIPS)`.

### HousingPrice_lag1

Represents the previous month's housing price.

Purpose:

- Captures short-term housing-market momentum.
- Reflects the persistence of housing prices over time.

Initial missing values:

- 67 missing values
- One missing first-month observation per county

### HousingPrice_lag12

Represents the housing price from the same month in the previous year.

Purpose:

- Captures year-over-year housing-market dynamics.
- Helps account for seasonality and annual persistence.

Initial missing values:

- 804 missing values
- 67 counties × 12 months

## Treatment of Missing Lag Values

Rows with missing lag features were removed.

Rationale:

- The first 12 months cannot have valid `HousingPrice_lag12` values.
- Removing these rows preserves the meaning of lag features.
- It avoids introducing artificial historical values.
- This is consistent with common forecasting and panel time-series practice.

After removing lag-missing rows:

- Observations: 11,963
- Date range: January 2011 to December 2025
- Unique counties: 67
- Missing lag values: 0

## Climate-Time Interaction Features

The FEMA National Risk Index provides static county-level risk scores. Since climate-risk awareness and market pricing may change over time, interaction features were created between risk scores and `TimeIndex`.

### CFLD_RISKS_x_Time

Construction:

```text
CFLD_RISKS_x_Time = CFLD_RISKS × TimeIndex
```

Purpose:

- Allows the model to learn whether coastal flood risk becomes more influential over time.

### HRCN_RISKS_x_Time

Construction:

```text
HRCN_RISKS_x_Time = HRCN_RISKS × TimeIndex
```

Purpose:

- Allows the model to learn whether hurricane risk becomes more influential over time.

Validation:

- Missing `CFLD_RISKS_x_Time` values: 0
- Missing `HRCN_RISKS_x_Time` values: 0

---

# 5. Final Engineered Dataset

## Final Dataset Characteristics

The final engineered dataset contains:

| Metric | Value |
|---|---:|
| Observations | 11,963 |
| Variables | 25 |
| Counties | 67 |
| Start Date | 2011-01-31 |
| End Date | 2025-12-31 |
| Duplicate county-month rows | 0 |

## Final Variable Groups

### Identifier Variables

- `RegionID`
- `SizeRank`
- `RegionName`
- `State`
- `Metro`
- `StateCodeFIPS`
- `MunicipalCodeFIPS`
- `STCOFIPS`
- `Date`

### Zillow Housing Features

- `HousingPrice`
- `Month`
- `TimeIndex`
- `is_metro`
- `HousingPrice_lag1`
- `HousingPrice_lag12`

### FEMA Features

- `STATE`
- `STATEABBRV`
- `COUNTY`
- `POPULATION`
- `CFLD_RISKS`
- `HRCN_RISKS`
- `SOVI_SCORE`
- `RESL_SCORE`

### Climate-Time Interaction Features

- `CFLD_RISKS_x_Time`
- `HRCN_RISKS_x_Time`

Final engineered dataset output:

```text
data/processed/engineered_zillow_fema_data.csv
```

---

# 6. Modeling Implications

Phase 1 produced the final analytical dataset required for both exploratory analysis and predictive modeling.

## Baseline Model Features

The baseline housing valuation models can use traditional housing-market and county-level characteristics such as:

- `TimeIndex`
- `Month`
- `SizeRank`
- `is_metro`
- `HousingPrice_lag1`
- `HousingPrice_lag12`
- `POPULATION`

## Climate-Enhanced Model Features

The climate-enhanced models can extend the baseline specification by adding:

- `CFLD_RISKS`
- `HRCN_RISKS`
- `SOVI_SCORE`
- `RESL_SCORE`
- `CFLD_RISKS_x_Time`
- `HRCN_RISKS_x_Time`

## Key Modeling Rationale

The engineered dataset directly supports the project's research design:

- Zillow provides the housing-value outcome.
- FEMA provides county-level climate-risk and resilience characteristics.
- Lag features capture housing-market persistence.
- Time and month features capture long-run trends and seasonality.
- Metro and population variables provide traditional county-level controls.
- Climate-time interactions allow static FEMA risk scores to have dynamic effects over the study period.

---

# Overall Phase 1 Conclusion

Phase 1 successfully transformed raw Zillow and FEMA datasets into a clean, validated, and modeling-ready county-level panel dataset for Florida.

The final dataset preserves complete county coverage, contains no missing values in key analytical variables, and includes engineered features that capture temporal dynamics, housing-price persistence, metropolitan status, and evolving climate-risk effects.

This dataset serves as the foundation for Phase 2 exploratory data analysis and the later modeling phase, where baseline and climate-enhanced housing valuation models will be compared.
