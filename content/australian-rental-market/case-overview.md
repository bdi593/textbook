# Case Overview

Predicting Weekly Rental Prices in the Australian Housing Market

```{figure} images/photoholgic-jK9dT34TfuI-unsplash.jpg
:label: Sydney Opera House
:alt: Sydney Opera House
:align: center

Sydney Opera House - [Unsplash](https://unsplash.com/photos/sydney-opera-house-australia-jK9dT34TfuI)
```

- Dataset Source: [Kaggle - Australian Rental Market Data 2026](https://www.kaggle.com/datasets/kanchana1990/australian-rental-market-data-2026)

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

## Business Problem

### Objective

Develop a predictive model that estimates the weekly rental price (price_display) for residential properties using structured, geospatial, and textual data.

### Target Variable

- `price_display` (weekly rent in AUD)

### Core Business Question

> Given a property's features, location, and description, what is its expected weekly rental price?

## Dataset Overview

The dataset includes:

- 6,700+ unique, cleaned listings
- Coverage across NSW, VIC, QLD, WA, SA, ACT, TAS, NT
- Precise latitude and longitude
- Sanitized text descriptions
- Structured property attributes

### Data Dictionary

| Column             | Data Type                    | Description                                                                    | Example                                           |
| ------------------ | ---------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------- |
| **title**          | Text (String)                | Marketing headline of the property listing.                                    | "Modern 2BR Apartment with City Views"            |
| **price_display**  | Numeric (Float/Integer)      | Weekly rental price in Australian Dollars (AUD), cleaned for numeric analysis. | 650                                               |
| **description**    | Text (String)                | Detailed property description with PII removed.                                | "Spacious home close to schools and transport..." |
| **propertyType**   | Categorical                  | Type of dwelling (House, Apartment, Townhouse, Studio, etc.).                  | Apartment                                         |
| **locality**       | Categorical                  | Broader administrative region associated with the property.                    | Greater Sydney                                    |
| **latitude**       | Numeric (Float)              | Geographic Y-coordinate for spatial modeling.                                  | -33.8688                                          |
| **longitude**      | Numeric (Float)              | Geographic X-coordinate for spatial modeling.                                  | 151.2093                                          |
| **postcode**       | Categorical (String/Integer) | Four-digit Australian postal code.                                             | 2000                                              |
| **state**          | Categorical                  | State or territory abbreviation (NSW, VIC, QLD, WA, SA, ACT, TAS, NT).         | NSW                                               |
| **street_address** | Text (String)                | Street-level property address.                                                 | 15 George St                                      |
| **suburb**         | Categorical                  | Residential suburb name.                                                       | Parramatta                                        |
| **bathrooms**      | Numeric (Integer)            | Number of bathrooms in the property.                                           | 2                                                 |
| **bedrooms**       | Numeric (Integer)            | Number of bedrooms in the property.                                            | 3                                                 |
| **parking_spaces** | Numeric (Integer)            | Number of dedicated parking or garage spaces.                                  | 1                                                 |
| **agency_name**    | Categorical                  | Real estate agency managing the listing.                                       | Ray White                                         |
| **amenities**      | Text / Semi-Structured       | Consolidated list of key features (e.g., Air Conditioning, Balcony).           | "Air Conditioning, Balcony, Dishwasher"           |

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

## Modeling Approach

Gradient Boosted Trees (XGBoost)

Why XGBoost is ideal here:

- Handles nonlinear relationships
- Automatically captures feature interactions
- Works well with structured/tabular data
- Robust to outliers
- Handles missing values
- Strong performance benchmark for Kaggle-style datasets

For business communication:

- **MAE**: "Average pricing error"
- **RMSE**: Penalizes large mispricing
- **R²**: % of rent variation explained
