# Case Overview

Predicting Weekly Rental Prices in the Australian Housing Market

## 1️⃣ Business Context

Australia's 2026 rental market is characterized by:

- High interstate migration
- Urban--regional demand shifts
- Affordability pressures in major metro areas
- Significant variation across states and territories

A national property analytics firm wants to develop a **data-driven rental pricing engine** to:

- Improve pricing recommendations for landlords
- Identify high-demand suburbs
- Support investment decision-making
- Benchmark agency competitiveness

They have obtained a cleaned dataset of **6,700+ rental listings across all eight Australian states and territories**, including geospatial coordinates and detailed property descriptions.

## 2️⃣ Business Problem

### Objective

Develop a predictive model that estimates the **weekly rental price (price_display)** for residential properties using structured, geospatial, and textual data.

### Target Variable

- `price_display` (weekly rent in AUD)

### Core Business Question

> Given a property's features, location, and description, what is its expected weekly rental price?

## 3️⃣ Dataset Overview (2026 National Snapshot)

The dataset includes:

- 6,700+ unique, cleaned listings
- Coverage across NSW, VIC, QLD, WA, SA, ACT, TAS, NT
- Precise latitude and longitude
- Sanitized text descriptions
- Structured property attributes

### Key Feature Categories

#### 🏠 Property Characteristics

- `bedrooms`
- `bathrooms`
- `parking_spaces`
- `propertyType`
- `amenities`

#### 📍 Geographic Variables

- `latitude`
- `longitude`
- `postcode`
- `suburb`
- `locality`
- `state`

#### 🏢 Market & Agency Information

- `agency_name`

#### 📝 Textual Data

- `title`
- `description`
- `amenities`

This multi-modal structure allows for:

- Regression modeling
- Geospatial modeling
- NLP feature extraction
- Market segmentation analysis

## 4️⃣ Analytical Framing

### Problem Type

Supervised Learning - Regression

### Modeling Approach

Gradient Boosted Trees (XGBoost)

Why XGBoost is ideal here:

- Handles nonlinear relationships
- Automatically captures feature interactions
- Works well with structured/tabular data
- Robust to outliers
- Handles missing values
- Strong performance benchmark for Kaggle-style datasets

## 5️⃣ Proposed Modeling Strategy

Step 1 - Data Preparation

### A. Feature Engineering

#### Numeric Enhancements

- Rent per bedroom
- Rent per bathroom
- Geospatial clusters (via K-means on lat/long)
- Distance to CBD (if engineered externally)

#### Categorical Encoding

- One-hot encode `propertyType`, `state`
- Target encoding for `suburb` or `agency_name`
- Postcode grouping

#### Text Processing (Optional but Powerful)

- TF-IDF on `description`
- Keyword flags (e.g., "waterfront", "renovated", "near transport")
- Sentiment score

Step 2 - Exploratory Analysis

Suggested visualizations:

- Rent distribution (likely right-skewed)
- Median rent by state
- Rent heatmap (latitude/longitude)
- Rent by propertyType
- Correlation heatmap (numeric variables)

If skewed, consider:

👉 Log-transforming `price_display`

Step 3 - Baseline Model

Start with:

- Linear Regression

Purpose:

- Benchmark performance
- Provide interpretability
- Establish baseline RMSE and MAE

Step 4 - XGBoost Model (Primary Model)

Train:

XGBRegressor

With:

- Cross-validation
- Early stopping
- Hyperparameter tuning:
  - max_depth
  - learning_rate
  - n_estimators
  - subsample
  - colsample_bytree

## 6️⃣ Evaluation Metrics

For business communication:

- **MAE** → "Average pricing error"
- **RMSE** → Penalizes large mispricing
- **R²** → % of rent variation explained

Example executive statement:

> "Our XGBoost model predicts weekly rental prices within ±$38 on average across Australia."

## 7️⃣ Advanced: Geospatial Modeling

Because this dataset includes latitude and longitude, you can:

- Identify pricing clusters
- Visualize demand hotspots
- Use spatial interactions within XGBoost
- Create geo-cluster features

This significantly strengthens the case compared to a typical regression dataset.

## 8️⃣ Advanced: NLP Integration

Using:

- TF-IDF features
- Keyword flags
- Amenities parsing

You can answer questions like:

- Does "air conditioning" command a rental premium?
- Do luxury keywords significantly increase predicted rent?
- Which amenities provide the highest ROI?

## 9️⃣ Model Interpretation

After training XGBoost:

Use:

- Feature importance
- SHAP values
