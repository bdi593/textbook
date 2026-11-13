# Case Overview

## 📖 Scenario

You are a marketing analyst at [MAC Cosmetics](https://www.maccosmetics.com/), a globally recognized brand known for its professional-grade makeup and strong presence in both retail and online channels.

&nbsp;

```{figure} images/MAC_Cosmetics_logo.png
:alt: MAC Cosmetics Logo
:width: 300px
:align: center
```

While MAC has long been a leader in artistry and brand prestige, the company is facing increasing pressure in the foundation category, especially among younger consumers (Gen Z and Millennials). Emerging brands and digitally native competitors are rapidly gaining traction through:

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

To better understand the competitive landscape, your team has collected data from Amazon's search results for "foundation", sorted by Best Selling, across the first five pages.

This dataset is a single snapshot of the products that ranked highest at the time of collection. It cannot show trends over time.

---

## 🎯 Learning Objectives

### 1. Technical Skills

By the end of this case study, you should be able to:

- Understand the structure of JSON data
- Parse and navigate nested JSON objects in Python, handling missing keys safely
- Extract and transform data into usable formats (e.g., tables and CSV files)
- Check scraped data before analysis, for example by confirming that every product is relevant and that every price is in the same currency

### 2. Business Insights

Using the parsed data, you will:

- Analyze competing foundation products in the marketplace
- Identify patterns in:
  - Pricing
  - Ratings and reviews
  - Product positioning (e.g., "full coverage", "natural finish", "hydrating")

- Describe how competitors present their products, including the attributes often linked to younger shoppers
- Generate insights to inform foundation-specific marketing and product strategy

---

## 📊 Dataset Overview

The dataset ([available on GitHub](https://github.com/bdi593/datasets/tree/main/amazon-makeup-foundation-products)) consists of three components focused on foundation products. The `parse-json` notebook reads them directly from that repository.

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
- `productResults`: A list of products returned on that page
- `pagination`: Links to the other result pages

Each product entry may contain:

- `asin`: Unique product identifier
- `title`: Product name and description
- `price`: Current and previous price, plus a currency `symbol`
- `reviews`: Rating and number of reviews
- `badges`: Indicators such as "Best Seller" or "Amazon's Choice"
- `deliveryInfo`: Shipping details

---

### 2. Product Details (`product-results/`)

- Contains one JSON file per product (`{asin}.json`), 227 files in total
- Provides more detailed product-level information under a `product` key, including `price`, `reviewsInfo`, `badges`, `featureBullets`, `description`, `breadcrumbs` (Amazon's category path), and `specification` (a list of key-value pairs that includes `Brand Name`)
- Can be used to enrich and validate insights from search results

A copy of these 227 files is stored in this chapter's `product-results/` folder, so the analysis can run without downloading them.

---

### 3. Flattened Dataset (`products.csv`)

- A simplified dataset containing:
  - `asin`
  - `title`

This file can be used as a starting point for:

- Joining datasets
- Indexing foundation products
- Building structured analyses

:::{warning} Not every result is a makeup foundation

A search for "foundation" also returns books (Asimov's *Foundation* series, a study Bible), mattress box springs, hair care, and nail products. A few prices are also in other currencies (for example, `PYG`, `ARS`, `MXN`, `CAD`, `GBP`), and some products have no price at all. Check each product's category (`breadcrumbs`) and the price `symbol` before comparing prices.

:::

### Source and licence

The files were collected from Amazon.com search results and product pages. According to the [dataset's README](https://github.com/bdi593/datasets/tree/main/amazon-makeup-foundation-products), they were gathered through [HasData](https://www.hasdata.com) and are "provided for educational and research purposes". The delivery estimates in the product files (for example, "Tomorrow, April 1") suggest the pages were collected at the end of March 2026. Check the source page for terms of use.

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

:::{caution} Know the limits of the data

- Only two MAC listings appear in these results, so any comparison with MAC rests on very few products.
- The data has no information about who buys each product. You can describe how listings are *marketed* to younger shoppers, but not who actually buys them.
- "Bought in past month" is Amazon's rounded label (for example, "2K+"), so treat it as a lower bound, not a sales figure.

:::

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

## 📚 Notebooks in This Case Study

| Notebook           | What it covers |
| ------------------ | -------------- |
| `parse-json.ipynb` | Fetches a search results page as JSON, inspects its keys and value types, extracts each product's ASIN and title into a table, loads `products.csv`, and opens one product detail file to show the richer fields it contains. |

Parsing all 227 product detail files and analyzing them is the work of this case study.

---

## 🧰 Setup

Install the course environment from the repository root:

```bash
python -m pip install -r requirements.txt
```

The `parse-json` notebook downloads its JSON and CSV files from `raw.githubusercontent.com`, so it needs an internet connection.
