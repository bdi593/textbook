# 🏡 Champaign-Urbana Zillow Sold Properties Dataset

This dataset contains information about properties sold in the Champaign-Urbana area (including Savoy), as listed on Zillow. It includes details such as the sale price, property type, number of bedrooms and bathrooms, square footage, and the date of sale. The data has been collected through [HasData](https://hasdata.com/), a large-scale data collection platform.

## 🔍 Search Criteria

- Properties in Champaign, Urbana, and Savoy
- "Sold" listings on Zillow (properties that have been sold, not just listed)
- 55+ senior communities are excluded from the dataset
- The dataset includes properties sold in the last ~5 years
- Only "house" property type is included (no condos, apartments, etc.)

## 📊 Consulting Scenario: Champaign-Urbana Housing Market Analysis

### 🏢 Background

You are working as a data consultant for a regional real estate investment firm, _Kingfisher Residential Partners (KRP)_, which is looking to expand its portfolio in Champaign, Urbana, and Savoy, Illinois.

KRP specializes in acquiring single-family homes in college towns and mid-sized cities, targeting properties that can generate stable rental income and long-term appreciation.

---

### ⚠️ Business Problem

Over the past year, KRP has observed increased volatility in housing prices and longer listing times in certain Midwest markets. The firm is considering allocating $5-10 million toward property acquisitions in the Champaign-Urbana-Savoy area but lacks a clear, data-driven understanding of:

- Which neighborhoods or cities offer the best value
- What property features drive higher prices
- Whether the market is currently favoring buyers or sellers
- How quickly properties are selling

To support this decision, KRP has provided you with a dataset of recent Zillow listings in the region.

### 📦 Why This Data Matters

The dataset contains detailed listing-level information, including:

- Property characteristics (price, beds, baths, square footage, year built)
- Location data (latitude/longitude, city, ZIP code)
- Market activity (date posted, days on Zillow)
- Amenities (garage, basement, new construction, etc.)
- School information
- Listing descriptions

This data allows you to analyze both pricing dynamics and market liquidity, which are critical for identifying attractive investment opportunities.

### 🎯 Your Role

As a data consultant, your task is to analyze this dataset and provide actionable recommendations to KRP's investment team.

### ❓ Key Questions to Address

You are expected to structure your analysis around the following:

#### 🏙️ 1. Market Overview

- How do prices and inventory differ across Champaign, Urbana, and Savoy?

#### 💰 2. Pricing Drivers

- What property features (e.g., size, beds/baths, garage, new construction) most strongly influence price?
- What is the relationship between price and living area (price per square foot)?

#### ⏱️ 3. Market Liquidity

- How long do properties typically stay on the market?
- What factors are associated with faster sales?

#### 📈 4. Temporal Trends

- Are prices or listing activity changing over time?
- Is the market becoming more competitive?

#### 🗺️ 5. Geographic Insights

- Are there clusters of high-value or high-growth areas?
- Do certain neighborhoods offer better investment potential?

## 📑 Deliverables

You will present your findings in a Jupyter notebook that includes:

- Key insights supported by data visualizations
- A clear narrative explaining market conditions

## 🚀 Getting Started

Use the following code to load the dataset and begin your analysis. The dataset is in Parquet format and can be accessed directly from the provided URL.

```python
df = pd.read_parquet("https://github.com/bdi593/datasets/raw/refs/heads/main/zillow-properties/zillow_properties_champaign_urbana_savoy.parquet")
df.head(3)
```
