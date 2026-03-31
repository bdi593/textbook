# Case Overview

## 📖 Scenario

You are a marketing analyst at [MAC Cosmetics](https://www.maccosmetics.com/), a globally recognized brand known for its professional-grade makeup and strong presence in both retail and online channels.

&nbsp;

```{figure} images/MAC_Cosmetics_logo.png
:alt: MAC Cosmetics Logo
:width: 300px
:align: center
```

While MAC has long been a leader in artistry and brand prestige, the company is facing increasing pressure specifically in the foundation category—especially among younger consumers (Gen Z and Millennials). Emerging brands and digitally native competitors are rapidly gaining traction through:

- Strong Amazon visibility
- Influencer-driven marketing
- Competitive pricing
- High review volumes and social proof

&nbsp;

```{figure} images/mac_studio_fix.png
:alt: MAC Studio Fix Fluid Foundation
:width: 500px
:align: center

MAC Cosmetics Studio Fix Fluid Foundation
```

&nbsp;

---

## ⚠️ Marketing Challenges

Your team has identified several key challenges:

- **Declining visibility on Amazon**: MAC foundation products are not consistently appearing in top "Best Selling" positions
- **Price competition**: Lower-priced foundation brands with strong reviews are outperforming premium offerings
- **Shifting preferences**: Younger consumers favor attributes like "lightweight", "natural finish", "hydrating", and "skin-first" formulations
- **Review-driven purchasing**: Foundation products with high ratings and thousands of reviews dominate conversion
- **Brand perception gap**: MAC is seen as professional and high-quality, but not always as trendy or accessible in everyday foundation use

To better understand the competitive landscape, your team has collected data from Amazon’s search results for "foundation", sorted by Best Selling, across the first five pages.

This dataset represents a snapshot of the top-performing foundation products currently capturing consumer demand.

---

## 🎯 Objective

The goal of this analysis is twofold:

### 1. Technical Skills

- Understand the structure of JSON data
- Learn how to parse and navigate nested JSON objects
- Extract and transform data into usable formats (e.g., CSV, tables)

### 2. Business Insights

- Analyze competing foundation products in the marketplace
- Identify patterns in:
  - Pricing
  - Ratings and reviews
  - Product positioning (e.g., "full coverage", "natural finish", "hydrating")

- Evaluate how competitors are appealing to younger audiences
- Generate insights to inform foundation-specific marketing and product strategy

---

## 📊 Dataset Overview

The dataset ([available on GitHub](https://github.com/bdi593/datasets/tree/main/amazon-makeup-foundation-products)) consists of two main components focused on foundation products:

### 1. Search Results (`search-results/`)

- Contains JSON files representing Amazon search result pages for **"foundation"**
- Results are sorted by **Best Selling**
- Covers the **first five pages of results**
- File naming pattern:
  - `foundation-page-01.json`
  - `foundation-page-02.json`
  - etc.

Each file includes:

- `requestMetadata`: Information about the search request
- `productResults`: A list of foundation products returned on that page

Each product entry may contain:

- `asin`: Unique product identifier
- `title`: Product name and description
- `price`: Current and previous price
- `reviews`: Rating and number of reviews
- `badges`: Indicators such as "Best Seller" or "Amazon’s Choice"
- `deliveryInfo`: Shipping details

---

### 2. Product Details (`product-results/`)

- Contains one JSON file per foundation product (`{asin}.json`)
- Provides more detailed product-level information
- Can be used to enrich and validate insights from search results

---

### 3. Flattened Dataset (`products.csv`)

- A simplified dataset containing:
  - `asin`
  - `title`

This file can be used as a starting point for:

- Joining datasets
- Indexing foundation products
- Building structured analyses

---

## 🧠 Key Questions to Explore

As a marketing analyst at MAC Cosmetics, consider:

- What price range dominates top-selling foundation products?
- How do MAC foundation products compare to competitors in price and ratings?
- Do higher-rated foundations also have significantly more reviews?
- What keywords appear frequently in top-performing foundation titles?
- Are certain brands consistently dominating the foundation category?
- How are foundations positioned (e.g., "matte", "dewy", "long-wear", "hydrating")?
- What signals might appeal specifically to younger consumers shopping for foundation?

---

## 🔍 Working with JSON

The dataset is stored in **JSON format**, which means:

- Data is structured as nested key-value pairs
- Some fields are optional or missing
- Many values are embedded within nested objects

### Example Access Pattern

```python
product["price"]["currentPrice"]
product["reviews"]["rating"]
```

To safely handle missing data:

```python
product.get("price", {}).get("currentPrice")
```

---

## 📐 Why JSON Matters

JSON is widely used in:

- APIs
- Web applications
- Data pipelines

Understanding how to work with JSON enables you to:

- Extract structured insights from raw data
- Build scalable data workflows
- Integrate multiple data sources

---

## 🚀 Outcome

By the end of this case study, you should be able to:

- Navigate and parse complex JSON datasets
- Transform raw data into structured formats
- Perform exploratory analysis on foundation product data
- Generate insights relevant to marketing and competitive strategy
