# 🏡 Champaign-Urbana Zillow Sold Properties Dataset

This dataset contains information about properties sold in the Champaign-Urbana area (including Savoy), as listed on Zillow. It includes details such as the sale price, number of bedrooms and bathrooms, square footage, location, school assignments, and the date each record was posted on Zillow. The data has been collected through [HasData](https://hasdata.com/), a large-scale data collection platform.

## 📈 Why Analytics Matters in Real Estate

Real estate is one of the oldest data-driven industries, but the *kinds* of analytics it relies on have evolved dramatically. Today, almost every decision in a real estate transaction is informed by data:

- **Pricing and valuation.** Comparative Market Analysis (CMA) used to be a manual exercise; today, automated valuation models (AVMs), such as Zillow's *Zestimate*, Redfin's *Estimate*, and Realtor.com's *RealEstimate*, combine hundreds of property features with neighborhood signals to produce price estimates in seconds.
- **Investment analysis.** Funds that buy single-family rentals (e.g. Invitation Homes, AMH) screen tens of thousands of listings per week with rules-based filters and predictive cap-rate models before a human ever looks at a property.
- **Market liquidity and timing.** Days-on-market, list-to-sale ratios, and inventory trends tell investors whether a market is shifting toward buyers or sellers and how aggressive their offer should be.
- **Geospatial and neighborhood analytics.** Latitude/longitude joined with school catchments, crime, walkability, transit, and amenity layers explain why two physically identical houses can differ by 30% in price across a single street.
- **Risk and underwriting.** Lenders, insurers, and short-term rental platforms (Airbnb, Vrbo) use the same property-level data for default-risk modeling, climate-risk assessment, and dynamic pricing.
- **Marketing and lead scoring.** Listing platforms predict which leads are most likely to transact, which homeowners are most likely to list soon, and which listings need a price drop.

The dataset in this case study is small by industry standards (a few thousand properties in one metro area), but it contains many of the fields a real Zillow analyst would work with: price, location, property attributes, school information, and listing text. That overlap lets us practice several of the analytics workflows above on a tractable scale. It does not include a sale date, so it cannot measure how quickly properties sell.

## 📊 Consulting Scenario: Champaign-Urbana Housing Market Analysis

### 🏢 Background

You are working as a data consultant for a regional real estate investment firm, _Kingfisher Residential Partners (KRP)_, which is looking to expand its portfolio in Champaign, Urbana, and Savoy, Illinois.

KRP specializes in acquiring single-family homes in college towns and mid-sized cities, targeting properties that can generate stable rental income and long-term appreciation.

---

### ⚠️ Business Problem

Over the past year, KRP has observed increased volatility in housing prices and longer listing times in certain Midwest markets. The firm is considering allocating $5-10 million toward property acquisitions in the Champaign-Urbana-Savoy area but lacks a clear, data-driven understanding of:

- Which neighborhoods or cities offer the best value
- What property features drive higher prices
- How prices are changing over time

To support this decision, KRP has provided you with a dataset of recent Zillow records of sold homes in the region.

### 📦 Why This Data Matters

The dataset contains detailed property-level information, including:

- Property characteristics (price, beds, baths, square footage, year built)
- Location data (latitude/longitude, city, ZIP code)
- Zillow activity fields (date posted, days on Zillow)
- Amenities (garage, basement, new construction, etc.)
- School information
- Listing descriptions

This data allows you to analyze pricing across cities, property features, time, and space, which is critical for identifying attractive investment opportunities.

### 🎯 Your Role

As a data consultant, your task is to analyze this dataset and provide actionable recommendations to KRP's investment team.

### ❓ Key Questions to Address

You are expected to structure your analysis around the following:

#### 🏙️ 1. Market Overview

- How do prices and inventory differ across Champaign, Urbana, and Savoy?

#### 💰 2. Pricing Drivers

- What property features (e.g., size, beds/baths, garage, new construction) most strongly influence price?
- What is the relationship between price and living area (price per square foot)?

#### 🔎 3. Data Check: Market Liquidity

- KRP would like to know how quickly properties sell. Before you answer, check what `days_on_zillow` measures. Is it the time from listing to sale?
- Can this dataset answer the liquidity question? If not, what data would you ask the vendor for?

:::{caution} No sale date

The dataset has no sale date. `days_on_zillow` behaves like the number of days since the record was posted, counted up to when the data was collected, so it cannot be used as time to sale.

:::

#### 📈 4. Temporal Trends

- Are prices or listing activity changing over time?

#### 🗺️ 5. Geographic Insights

- Are there clusters of high-value or high-growth areas?
- Do certain neighborhoods offer better investment potential?

## 🎯 Learning Objectives

By working through this case study, you will practice how to:

- Load a Parquet dataset from a URL with `pandas` and profile its columns
- Find and handle data problems (zero prices, zero living areas, missing dates) before analysis
- Compare markets with medians and price per square foot instead of means and raw prices
- Explore price drivers with correlations and charts without reading them as causal effects
- Check what a field actually measures before building an analysis on it
- Build time trends from monthly aggregates, leaving out months with too few records
- Map properties with Plotly and connect location and school catchments to price

## 🗂️ Dataset

### 🔍 Search Criteria

- Properties in Champaign, Urbana, and Savoy
- "Sold" listings on Zillow (properties that have been sold, not just listed)
- 55+ senior communities are excluded from the dataset
- Records were posted on Zillow between May 2022 and March 2026 (438 records have no posting date)
- Only "house" property type is included (no condos, apartments, etc.)

### Columns

The file has 3,737 rows (one per property) and 30 columns:

| Columns | Description |
| ------- | ----------- |
| `property_id` | Zillow property identifier |
| `price` | Sale price in US dollars. One row has a price of 0. |
| `date_posted` | Date the record was posted on Zillow. Missing for 438 rows. |
| `days_on_zillow` | Days the record has been on Zillow. Not time to sale (see above). |
| `description` | Listing description text |
| `beds`, `baths`, `year_built`, `living_area`, `lot_size` | Property size and age. Two rows have a `living_area` of 0. |
| `latitude`, `longitude`, `address_street`, `address_city`, `address_state`, `address_zipcode` | Location |
| `reso_has_garage`, `reso_has_attached_garage`, `reso_garage_parking_capacity`, `reso_parking_capacity`, `reso_attic`, `reso_stories`, `reso_basement_yn`, `reso_has_cooling`, `reso_has_heating`, `reso_is_new_construction` | Property facts and amenities |
| `reso_elementary_school`, `reso_middle_or_junior_school`, `reso_high_school` | Assigned schools, as typed into the listing. The same school can appear under several spellings. |
| `reso_tax_annual_amount` | Annual property tax |

### Source and licence

The data was collected from Zillow.com through [HasData](https://hasdata.com/) and is published in the [`bdi593/datasets` repository](https://github.com/bdi593/datasets/tree/main/zillow-properties). Check the source page for terms of use.

## 📚 Notebooks in This Case Study

There is no starter notebook for this case study. You build your own notebook, starting from the loading code in the Setup section below.

## 🚀 Setup

Install the course environment from the repository root:

```bash
python -m pip install -r requirements.txt
```

Use the following code to load the dataset and begin your analysis. The dataset is in Parquet format and can be read directly from the URL.

```python
import pandas as pd

df = pd.read_parquet(
    "https://media.githubusercontent.com/media/bdi593/datasets/main/zillow-properties/zillow_properties_champaign_urbana_savoy.parquet"
)
df.head(3)
```

## 📑 Deliverables

You will present your findings in a Jupyter notebook that includes:

- Key insights supported by data visualizations
- A clear narrative explaining market conditions
