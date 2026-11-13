# Australian Rental Market Case Overview

Predicting Weekly Rental Prices in the Australian Housing Market

```{figure} images/photoholgic-jK9dT34TfuI-unsplash.jpg
:label: Sydney Opera House
:alt: Sydney Opera House
:align: center

Sydney Opera House - [Unsplash](https://unsplash.com/photos/sydney-opera-house-australia-jK9dT34TfuI)
```

## Business Context

Australia's rental market is characterized by:

- High interstate migration
- Urban-regional demand shifts
- Affordability pressures in major metro areas
- Significant variation across states and territories

A national property analytics firm wants to develop a data-driven rental pricing engine to:

- Improve pricing recommendations for landlords
- Identify high-demand suburbs
- Support investment decision-making
- Benchmark agency competitiveness

They have obtained a cleaned dataset of 6,700+ rental listings across all eight Australian states and territories, including geospatial coordinates and detailed property descriptions.

### Objective

Develop a predictive model that estimates the weekly rental price (`price_display`) for residential properties using structured, geospatial, and textual data.

### Target Variable

- `price_display` (weekly rent in AUD)

### Core Business Question

> Given a property's features, location, and description, what is its expected weekly rental price?

## Learning Objectives

After working through this case study, you will be able to:

- Explore a right-skewed target and map listing locations with Plotly.
- Train XGBoost regressors with native categorical features and evaluate them with MAE, RMSE, and R².
- Explain why choosing hyperparameters on the test set makes the test score optimistic.
- Engineer features from text (amenity flags, description length, TF-IDF) and from geography (distances to capital cities, suburb target encoding).
- Use out-of-fold target encoding inside a scikit-learn pipeline so that no training row sees its own target.
- Measure each modeling change on its own with an ablation, and tune hyperparameters with a cross-validated random search.

## Dataset Overview

The dataset includes:

- 6,767 cleaned listings
- Coverage across NSW, VIC, QLD, WA, SA, ACT, TAS, NT
- Latitude and longitude for every listing
- Text descriptions
- Structured property attributes

### Data Dictionary

| Column             | Data Type                    | Description                                                                    | Example                                           |
| ------------------ | ---------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------- |
| **title**          | Text (String)                | Marketing headline of the property listing.                                    | "Modern 2BR Apartment with City Views"            |
| **price_display**  | Numeric (Float/Integer)      | Weekly rental price in Australian Dollars (AUD), cleaned for numeric analysis. | 650                                               |
| **description**    | Text (String)                | Detailed property description.                                                 | "Spacious home close to schools and transport..." |
| **propertyType**   | Categorical                  | Type of dwelling (house, apartment, unit, townhouse, studio, etc.).            | apartment                                         |
| **locality**       | Categorical                  | Locality name. In this dataset it is identical to `suburb` in every row.       | Parramatta                                        |
| **latitude**       | Numeric (Float)              | Geographic Y-coordinate for spatial modeling.                                  | -33.8688                                          |
| **longitude**      | Numeric (Float)              | Geographic X-coordinate for spatial modeling.                                  | 151.2093                                          |
| **postcode**       | Categorical (String/Integer) | Four-digit Australian postal code.                                             | 2000                                              |
| **state**          | Categorical                  | State or territory, as written in the data: NSW, Vic, Qld, WA, SA, ACT, Tas, NT. | NSW                                             |
| **street_address** | Text (String)                | Street-level property address.                                                 | 15 George St                                      |
| **suburb**         | Categorical                  | Residential suburb name.                                                       | Parramatta                                        |
| **bathrooms**      | Numeric (Integer)            | Number of bathrooms in the property.                                           | 2                                                 |
| **bedrooms**       | Numeric (Integer)            | Number of bedrooms in the property.                                            | 3                                                 |
| **parking_spaces** | Numeric (Integer)            | Number of dedicated parking or garage spaces.                                  | 1                                                 |
| **agency_name**    | Categorical                  | Real estate agency managing the listing.                                       | Ray White                                         |
| **amenities**      | Text / Semi-Structured       | Comma-separated list of key features (e.g., Air Conditioning, Balcony). Missing for about 5% of listings. | "Air Conditioning, Balcony, Dishwasher" |

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
- `locality` (same values as `suburb`)
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

### Source and Licence

The dataset was published on Kaggle as [Australian Rental Market Data 2026](https://www.kaggle.com/datasets/kanchana1990/australian-rental-market-data-2026). The course hosts a copy in the [datasets repository](https://github.com/bdi593/datasets/tree/main/australian-rental-market-2026). Check the source page for terms of use.

## Notebooks in This Case Study

| Notebook                                              | What it covers                                                                                                                                                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Build a Regressor](./build-a-regressor.ipynb)        | Explores the rent distribution and listing locations, trains XGBoost regressors with default and hand-picked hyperparameters on structured features, and interprets MAE, RMSE, and R².                                         |
| [Improve the Model](./improve-the-model.ipynb)        | Adds a log target, amenity flags, TF-IDF text features, distances to capital cities, and out-of-fold suburb target encoding; measures each change on its own; tunes hyperparameters with random search; and discusses external data. |

## Setup

Install the packages used across the book from the root of the repository:

```bash
python -m pip install -r requirements.txt
```

Both notebooks download the data from the course datasets repository, so you need an internet connection. The hyperparameter searches in the second notebook take several minutes.

## Modeling Approach

Gradient Boosted Trees (XGBoost)

Why XGBoost is a good fit here:

- Handles nonlinear relationships
- Automatically captures feature interactions
- Works well with structured/tabular data
- Handles categorical features (suburb, postcode, agency) natively
- Handles missing values
- Strong performance benchmark for Kaggle-style datasets

:::{caution} Outliers in the target

Tree splits depend only on the order of feature values, so outliers in the *features* do little harm. Outliers in the *target* are different. With the default squared-error loss, a few very expensive listings dominate the loss, so XGBoost is not robust to them. The second notebook tries a log transform of rent to reduce their influence.

:::

For business communication:

- **MAE**: "Average pricing error"
- **RMSE**: Penalizes large mispricing
- **R²**: % of rent variation explained
