# Phase 2: Exploratory Data Analysis (EDA) Findings

## Overview

The objective of Phase 2 was to explore Florida's climate-risk environment, understand long-term housing-market dynamics, and investigate whether preliminary relationships exist between climate risk and housing values.

The analysis utilized the final engineered Zillow–FEMA county-level panel dataset containing 11,963 observations across 67 Florida counties between 2011 and 2025.

---

# 1. Florida Climate Risk Findings

Two climate hazards were examined using FEMA National Risk Index data:

- Coastal Flood Risk (`CFLD_RISKS`)
- Hurricane Risk (`HRCN_RISKS`)

## Key Findings

### Flood Risk

- Coastal flood risk exhibited substantial variation across Florida counties.
- Higher flood-risk counties were concentrated along Florida's coastlines.
- Several inland counties exhibited little or no coastal flood exposure.
- Flood risk displayed strong geographic heterogeneity.

### Hurricane Risk

- Hurricane risk remained consistently high throughout most of Florida.
- Both coastal and inland counties exhibited elevated hurricane-risk scores.
- Hurricane-risk variation was considerably smaller than flood-risk variation.
- Hurricane exposure appeared to be a statewide phenomenon rather than a localized coastal risk.

## Main Takeaway

Different climate hazards exhibit distinct spatial patterns across Florida. Flood risk varies substantially between counties, whereas hurricane risk affects most of the state relatively uniformly. This suggests that different hazards may influence housing markets in different ways.

---

# 2. Florida Housing Market Findings

Average county-level housing prices were examined between 2011 and 2025.

## Key Findings

### Post-Crisis Adjustment (2011–2012)

- Housing prices declined slightly during the early years of the study period.
- This likely reflects continued adjustment following the 2008 housing-market collapse.

### Sustained Appreciation (2012–2020)

- Housing prices increased steadily across Florida throughout the decade.
- Long-term appreciation was observed across most counties.

### COVID-Era Housing Boom (2020–2022)

- Housing prices accelerated rapidly after 2020.
- This period produced the strongest appreciation observed during the study period.

### Market Moderation (2023–2025)

- Price growth slowed following the COVID housing boom.
- Housing values remained historically elevated despite the slowdown.

## Main Takeaway

Florida experienced substantial housing-price appreciation between 2011 and 2025, increasing from approximately \$130,000 to more than \$320,000 on average. Temporal market dynamics therefore represent an important component of any housing-valuation model.

---

# 3. Climate Risk and Housing Market Findings

The relationship between climate risk and housing-market outcomes was explored using risk-group comparisons, risk-bucket analysis, county-level appreciation analysis, and correlation analysis.

## Key Findings

### High-Risk vs Low-Risk Counties

- High-flood-risk counties consistently exhibited higher average housing prices than low-risk counties.
- Both groups experienced substantial appreciation throughout the study period.
- High-risk counties appreciated more rapidly than low-risk counties.

### Risk-Bucket Analysis

| Risk Group | Appreciation |
|------------|-------------|
| Low Risk | 138.7% |
| Medium Risk | 142.3% |
| High Risk | 165.7% |

The results suggest stronger long-term housing-price growth in higher-risk counties.

### County-Level Analysis

- County-level appreciation exhibited substantial variation across Florida.
- The correlation between flood risk and appreciation was approximately 0.066.
- Flood risk alone explained very little of the variation in county-level appreciation.

### Correlation Analysis

| Variable | Correlation with HousingPrice |
|-----------|-----------|
| CFLD_RISKS | 0.361 |
| HRCN_RISKS | 0.294 |
| POPULATION | 0.219 |

Additional findings:

- Flood risk and hurricane risk exhibited a moderate positive correlation (0.50).
- Population exhibited moderate positive correlations with both climate-risk variables.
- No pair of variables exhibited extremely high correlations.

## Main Takeaway

Climate risk appears related to housing-market outcomes, but the relationship is neither simple nor deterministic. Higher-risk counties generally exhibited stronger housing-market performance, yet climate risk alone explains only a small portion of county-level variation.

---

# 4. Implications for Modeling

The EDA findings provide several important motivations for the modeling phase.

## Climate Risk Contains Potentially Useful Information

- Flood risk exhibited meaningful relationships with housing prices.
- Climate-risk variables appear to capture information beyond traditional demographic characteristics.

## Climate Risk Alone Is Insufficient

- County-level relationships were relatively weak.
- Housing prices are influenced by multiple interacting factors.

## Need for Multivariate Modeling

The EDA suggests that evaluating climate risk in isolation is unlikely to fully explain housing-market outcomes. More sophisticated models are required to simultaneously account for:

- Housing-market dynamics
- Temporal effects
- Demographic characteristics
- Climate-risk exposure

## Motivation for Machine Learning

Machine-learning models provide a flexible framework for capturing nonlinear relationships and complex interactions among predictors. These methods are therefore well suited for evaluating whether climate-risk variables improve housing-valuation performance.

---

# Overall Phase 2 Conclusion

The exploratory analysis revealed substantial variation in both climate-risk exposure and housing-market outcomes across Florida counties.

While higher-risk counties generally exhibited stronger housing-price growth and higher average housing values, climate risk alone explained only a limited portion of observed housing-market variation.

These findings provide preliminary evidence that climate-risk variables may contribute useful information for housing valuation. However, formal evaluation requires multivariate predictive modeling.

The next phase of the project therefore focuses on determining whether climate-risk variables improve housing-valuation performance when incorporated into traditional and machine-learning-based valuation models.

