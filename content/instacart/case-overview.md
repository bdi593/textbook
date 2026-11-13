# Instacart Case Overview

## 1. Introduction

### Background

Instacart is an American grocery delivery and pick-up service that connects consumers with personal shoppers who fulfil orders from local supermarkets. In May 2017, Instacart released an anonymized snapshot of its transaction history, one of the largest publicly available retail datasets, to support research in machine learning, consumer behaviour, and operations analytics.

The dataset captures **over 3 million grocery orders** placed by **more than 200,000 unique users**, with the timing of every order (day of week, hour of day, and days elapsed since the previous order). For a subset of orders it also records every product purchased, the sequence in which items were added to the cart, and whether each item was a reorder. The files used in this case study contain item-level detail for 131,209 orders, **one per customer and always that customer's most recent order** (see [What the train split means](#instacart-train-split) below).

### Why This Dataset Matters for Business Analytics

Grocery retail operates on thin margins and intense competition. The ability to understand _what_ customers buy, _when_ they buy it, _how often_ they return, and _which products they consistently reorder_ translates directly into revenue-generating decisions:

- **Personalised recommendations**: surfacing products a customer is likely to buy next.
- **Assortment optimisation**: knowing which aisles drive the most volume and loyalty.
- **Promotional targeting**: identifying moments in a customer's lifecycle where intervention (e.g., a coupon) is most effective.
- **Demand forecasting**: predicting order volume by time of day and day of week to staff and stock efficiently.

### Types of Analyses This Dataset Supports

The table below maps analytical techniques to the business questions they address. The notebooks in this case study cover EDA, temporal analysis, product performance, reorder analysis, segmentation by order frequency, market basket analysis, and cart behaviour.

| Analysis Type                       | Technique                                                    | Business Question Addressed                                                      |
| ----------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **Exploratory Data Analysis (EDA)** | Descriptive statistics, histograms, bar charts               | What does the data look like? Are there anomalies or patterns at a glance?       |
| **Temporal Analysis**               | Aggregation by day of week and hour, heatmaps                | When do customers shop? Are there peak hours or days?                            |
| **Product Performance Analysis**    | Value counts, ranked lists                                   | Which products, aisles, and departments are most popular?                        |
| **Reorder / Loyalty Analysis**      | Reorder rate by product, aisle, department, and segment      | Which products and categories drive repeat purchases?                            |
| **Customer Segmentation**           | Rule-based segments, RFM-style scoring, k-means clustering   | Which customer groups exist based on purchasing behaviour?                       |
| **Market Basket Analysis**          | Co-occurrence counting, Apriori algorithm, association rules | Which products are frequently bought together? How can this drive cross-selling? |
| **Cart Behaviour Analysis**         | Add-to-cart position, basket size distribution               | How do customers build their carts? What is bought first vs. last?               |
| **Predictive Modelling** \*         | Logistic regression, gradient boosting, neural networks      | Can we predict whether a customer will reorder a specific product?               |
| **Recommendation Systems** \*       | Collaborative filtering, word2vec on item sequences          | How can personalised product recommendations be generated?                       |
| **Loyalty Over Time** \*            | Cohort analysis, per-customer order sequences                | How does a customer's loyalty evolve from their first order to their last?       |

\* These analyses need each customer's earlier baskets, which are in the `order_products__prior` file of the full Instacart release. That file is not part of the mirror used here. The dataset also has no calendar dates, so demand can be studied by day of week and hour of day but not forecast over calendar time.

---

## 2. Learning Objectives

By completing this case study, students will be able to:

1. **Load and merge** a multi-table relational dataset using `pandas` and reason about entity relationships and foreign keys.
2. **Perform a structured EDA**, including univariate, bivariate, and temporal analysis, on a dataset with millions of rows, aggregating before plotting so that charts stay light.
3. **Quantify customer loyalty** by calculating reorder rates and interpreting them at the product, aisle, and department level.
4. **Segment customers** by order frequency and profile each segment, while recognising what a one-basket-per-customer, cross-sectional view can and cannot show.
5. **Apply market basket analysis** (co-occurrence counts and Apriori association rules) to identify product affinities and translate findings into concrete cross-selling or promotional ideas.
6. **Communicate analytical findings** through well-labelled visualisations and concise written takeaways.
7. **Evaluate the limitations** of the dataset (a biased sample, one basket per customer, capped and undocumented fields, no pricing or demographics) and discuss how those limitations affect business conclusions.

---

## 3. Dataset

### Scale

| Dimension                            | Value         |
| ------------------------------------ | ------------- |
| Total orders                         | ~3.4 million  |
| Unique users                         | ~206,000      |
| Orders with item detail (train set)  | 131,209       |
| Products in catalogue                | ~50,000       |
| Aisles                               | 134           |
| Departments                          | 21            |
| Order–product rows (train set)       | ~1.38 million |

### Files Used

All five files are read directly from the mirror described under [Source and Licence](#instacart-source).

| File                       | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `orders.csv.zip`           | One row per order (user ID, timing, and sequence info), zipped    |
| `order_products_train.csv` | One row per item in a train-split order (each user's last order)  |
| `products.csv`             | Product catalogue with aisle and department linkage               |
| `aisles.csv`               | Aisle ID → aisle name lookup                                      |
| `departments.csv`          | Department ID → department name lookup                            |

### Data Dictionary

#### `orders`

| Column                   | Type   | Description                                                                                       |
| ------------------------ | ------ | ------------------------------------------------------------------------------------------------- |
| `order_id`               | int    | Unique order identifier                                                                           |
| `user_id`                | int    | Unique user (customer) identifier                                                                 |
| `eval_set`               | string | Which split this order belongs to (`prior`, `train`, or `test`)                                   |
| `order_number`           | int    | Sequence number for this user (1 = first order, n = nth order)                                    |
| `order_dow`              | int    | Day of the week the order was placed, coded 0 to 6 (which code is which day is not documented)    |
| `order_hour_of_day`      | int    | Hour of the day the order was placed (0–23)                                                       |
| `days_since_prior_order` | float  | Days elapsed since the user's previous order; capped at 30 (so 30 means 30 or more); NaN for `order_number = 1` |

:::{caution} Which day is `order_dow = 0`?

Instacart's data dictionary describes `order_dow` only as "the day of the week the order was placed on". It does not say which code is which day. The notebooks label the codes with a common community assumption, **0 = Saturday, 1 = Sunday, ..., 6 = Friday**. Treat those day names as an assumption, not a fact, and say so when you report day-of-week findings.

:::

#### `order_products_train`

| Column              | Type | Description                                                          |
| ------------------- | ---- | -------------------------------------------------------------------- |
| `order_id`          | int  | Foreign key → `orders.order_id`                                      |
| `product_id`        | int  | Foreign key → `products.product_id`                                  |
| `add_to_cart_order` | int  | Position in which the product was added to the cart (1 = first)      |
| `reordered`         | int  | 1 if this product was previously purchased by this user; 0 otherwise |

#### `products`

| Column          | Type   | Description                               |
| --------------- | ------ | ----------------------------------------- |
| `product_id`    | int    | Unique product identifier                 |
| `product_name`  | string | Human-readable product name               |
| `aisle_id`      | int    | Foreign key → `aisles.aisle_id`           |
| `department_id` | int    | Foreign key → `departments.department_id` |

#### `aisles`

| Column     | Type   | Description                                 |
| ---------- | ------ | ------------------------------------------- |
| `aisle_id` | int    | Unique aisle identifier                     |
| `aisle`    | string | Aisle name (e.g., "fresh fruits", "yogurt") |

#### `departments`

| Column          | Type   | Description                                     |
| --------------- | ------ | ----------------------------------------------- |
| `department_id` | int    | Unique department identifier                    |
| `department`    | string | Department name (e.g., "produce", "dairy eggs") |

### Table Relationships

```
departments ──┐
              ├──► products ──► order_products_train ──► orders
aisles  ───────┘
```

`orders` is the central fact table. `order_products_train` is a many-to-many bridge between orders and products. `products`, `aisles`, and `departments` are dimension/lookup tables that enrich item-level records with human-readable names and hierarchical categorisation.

(instacart-train-split)=
### What the Train Split Means

:::{important} One basket per customer

`orders` lists every order for every user, but `order_products_train` contains the items of only 131,209 orders: the **train** split. Each user in it has exactly **one** order there, and it is always that user's **most recent** order. Every user has at least 4 orders, so this order is always order number 4 or later. The other 75,000 users' most recent orders are in the `test` split, whose items are not included.

This shapes every customer-level result in the case study:

- A customer's "basket size" and "reorder rate" describe their **most recent order only**, not an average over their history.
- Order counts and gaps between orders come from `orders`, so they cover every order the dataset includes for each customer (between 4 and 100).
- Comparing customers with different numbers of earlier orders is a **cross-sectional** comparison of different people at one point in time. It does not follow the same customers as they gain experience.

A true lifetime analysis, such as how one customer's reorder rate changes from order to order, needs the `order_products__prior` file from the full Instacart release, which lists the items in every earlier order. That file is not in the mirror this book uses.

:::

(instacart-source)=
### Source and Licence

The data is "The Instacart Online Grocery Shopping Dataset 2017", released by Instacart in May 2017 (see the [dataset release note](blog-post.md)). Instacart's original download page is no longer online. The notebooks read the files from a public mirror on GitHub, [subwaymatch/instacart-dataset-2017](https://github.com/subwaymatch/instacart-dataset-2017).

The mirror's README states that the dataset "is provided as-is for non-commercial use" and links to Instacart's [Dataset Usage Terms and Conditions](https://gist.github.com/jeremystan/582eba13d6ee27ed465c43dc78934700). Read those terms before you use or share the data.

Instacart asks users to cite the dataset as: _"The Instacart Online Grocery Shopping Dataset 2017", Accessed from `https://www.instacart.com/datasets/grocery-shopping-2017` on \<date\>_. The page in that citation no longer loads, so you may add the mirror's URL when you cite it.

---

## 4. Notebooks in This Case Study

Work through the pages in this order, then answer the questions in Section 6 in your own notebook.

| Page                               | What it covers                                                                                                                                                                         |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `blog-post.md`                     | A copy of Instacart's 2017 blog post announcing the dataset, with its notes on privacy and sample bias.                                                                                |
| `eda.ipynb`                        | Loading the five tables, data types, missing values, table relationships, univariate distributions, merging, value counts, reorder ratios, cart position, time patterns, correlation. |
| `analysis.ipynb`                   | A gallery of polished charts: orders by day and hour, top products, departments and aisles, reorder ratios, basket sizes, days between orders, add-to-cart position.                  |
| `customer_behavior_analysis.ipynb` | Part A: product and aisle co-occurrence and Apriori association rules at the aisle level. Part B: customer profiles and order-frequency segments based on each customer's most recent order. |

---

## 5. Setup

Install the packages used across the book from the root of the repository:

```bash
python -m pip install -r requirements.txt
```

The notebooks download the data from the mirror, so you need an internet connection. A few practical notes:

1. **No unzipping needed.** `pd.read_csv(url, compression="zip")` reads `orders.csv.zip` directly.
2. **Mind memory usage.** `orders` has about 3.4 million rows and the enriched item table about 1.4 million. A typical laptop handles this, but avoid storing redundant copies of large DataFrames.
3. **Keep the raw tables intact.** Assign transformed frames to new variables so you can always go back to the original data.
4. **Aggregate before plotting.** Plotly histograms and box plots store every input value. Count or summarise first, as the notebooks do, so your notebook stays small.

---

## 6. Questions to Answer

Complete all questions in a single Jupyter notebook. For each question, include:

- The Python code used to compute the answer.
- At least one supporting visualisation (where relevant).
- A 1–3 sentence written interpretation of the result.

---

### Part A: Exploratory Data Analysis

**A1.** How many unique users, orders, and products are captured in the dataset? What is the average number of orders per user, and how does that distribution look?

**A2.** What percentage of items in `order_products_train` are reorders (i.e., `reordered == 1`)? What does this tell you about the typical Instacart customer?

**A3.** Identify the top 10 most-ordered products. Are any of these products surprising? What do the top products suggest about Instacart's primary customer base?

**A4.** Plot the distribution of `days_since_prior_order`. What are the most common shopping cadences? What might explain the spike at 30 days?

**A5.** Create a heatmap of order volume by day of week and hour of day. Identify the two peak ordering windows and hypothesise why they occur at those times. State which `order_dow` mapping you assume.

---

### Part B: Product and Category Analysis

**B1.** Rank all 21 departments by total number of items ordered _and_ by reorder rate. Which departments rank highly on both metrics? Which departments have low reorder rates despite high volume, and what might explain this?

**B2.** Within the **produce** department, compare the reorder rates of the top 10 aisles. Which produce aisles are most "sticky" (highest reorder rate), and what business implication does this carry for a loyalty programme?

**B3.** The `add_to_cart_order` column records where in the shopping session each item was added. Compute the average cart position for each department. Which departments are added first, and which are added last? Propose a hypothesis about customer shopping intent that explains this ordering.

**B4.** Select any one department and perform a deep-dive: show its top 10 products, its reorder rate trend, and its peak ordering hours. Write a brief profile of the "typical buyer" in this department.

---

### Part C: Customer Segmentation

**C1.** Build a customer-level summary table for the 131,209 customers whose most recent order is in the train split, with these features per customer:

- Total number of orders placed (from `orders`)
- Average days between orders (from `orders`)
- Basket size of the most recent order (items in that order)
- Reorder rate of the most recent order (share of its items with `reordered == 1`)

Report the mean, median, and standard deviation of each feature. Which features describe the customer's whole history, and which describe a single order?

**C2.** Segment customers into at least three groups based on **order frequency** (total orders placed). Every customer has at least 4 orders, so label each group with its actual range (e.g., Light (4-5 orders), Regular, Frequent, Power). For each segment, report the average basket size and reorder rate of the most recent order, and the average days between orders. What are the defining behavioural characteristics of each segment?

**C3.** For each customer's most recent order, compute how many orders they had placed before it (`order_number - 1`). Visualise how the reorder rate of the most recent order varies with this number. Does the reorder rate rise with the number of earlier orders? Explain why this cross-sectional chart cannot show how a single customer's loyalty changes over time, and name two effects other than growing loyalty that could make the curve rise.

**C4.** Using each customer's most recent order, identify the top 3 departments by share of items for each customer segment. How do product preferences differ between Light and Power users? What does this imply for how Instacart should communicate with each segment?

---

### Part D: Market Basket Analysis

**D1.** Find the 10 most frequently co-purchased product pairs (products that appear together in the same order). For each pair, report the co-occurrence count and suggest a practical cross-selling or placement strategy.

**D2.** Using the Apriori algorithm (`mlxtend`), mine association rules from the dataset at the **aisle** level (each order is a basket of aisles). Filter to rules with **support ≥ 0.05** and **confidence ≥ 0.4**. Report the top 5 rules by lift and explain what each rule means in plain language.

**D3.** Choose one high-lift rule from D2. Describe a concrete promotional tactic (e.g., a bundled discount, a recommendation widget, a targeted push notification) that Instacart could implement to capitalise on this product affinity.

---

### Part E: Critical Evaluation

**E1.** This dataset is described by Instacart as "a heavily biased subset" of its production data. Identify at least **three specific ways** the sample may be biased and explain how each bias could lead an analyst to draw incorrect conclusions.

**E2.** The dataset contains no pricing, demographic, or geographic information. Pick **two business questions** that you were unable to fully answer because of these absences. For each, describe what additional data you would need and how you would collect or acquire it.

**E3.** Suppose Instacart wanted to use the insights from this case study to redesign their homepage for first-time users. What analytical findings from your work are directly applicable, and what additional research (e.g., A/B testing, user surveys) would be required before making the change?

---

## 7. Grading Rubric

| Component                      | Weight | Criteria                                                                          |
| ------------------------------ | ------ | --------------------------------------------------------------------------------- |
| Code quality & reproducibility | 30%    | Notebook runs top-to-bottom without errors; code is readable and well-commented   |
| Analytical depth               | 40%    | Questions are answered completely; methodology is sound and clearly explained     |
| Visualisation quality          | 30%    | Charts are appropriately chosen, labelled, and support the written interpretation |
