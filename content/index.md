# BDI 199/593 - Advanced Analytics Applications in Business

- University of Illinois Urbana-Champaign
- **Instructor**: Ye Joo Park ([ypark32@illinois.edu](mailto:ypark32@illinois.edu))

This course builds on the data analytics foundations from BDI 475: Introduction to Data Analytics Applications in Business. It focuses on the analytics work that real business problems demand:

1. handling data that is messy, nested, or too large for a spreadsheet,
2. building, evaluating, and questioning predictive models, and
3. communicating findings to people who make decisions.

```{image} ../site_images/favicon.svg
:alt: BDI 199/593 Circle
:width: 320px
:align: center
```

&nbsp;

## How this book is organized

The book is organized around case studies. Each case study starts with an overview page that describes the business context and the dataset, followed by one or more notebooks that work through the analysis step by step.

| Case study | Business question | Main methods and tools |
| --- | --- | --- |
| Cleaning Airbnb Listings | What does it take to turn raw listing data into an analysis-ready table? | pandas, data cleaning, missing values, type conversion |
| Credit Card Transactions | How do we explore tens of millions of transactions and flag suspicious activity? | Polars, DuckDB, SQL, window functions, Parquet |
| Kickstarter Projects | Which crowdfunding projects succeed, and what can a model honestly predict? | Polars preprocessing, binary classification, XGBoost, data leakage |
| Data Job Postings | What do data roles pay, where are they, and which skills are in demand? | Polars, exploratory data analysis, HR analytics |
| Amazon On-time Delivery | Which deliveries are likely to arrive late? | classification, XGBoost, evaluation metrics, threshold tuning |
| Australian Rental Market | What drives weekly rent, and how much can feature engineering help? | regression, XGBoost, target encoding, cross-validation |
| Conference Calls | How can text become structured data for business decisions? | NLP preprocessing, spaCy, text classification, topic modeling |
| CU+Savoy Zillow Properties | How do prices differ across Champaign, Urbana, and Savoy? | exploratory analysis, real estate metrics, Plotly |
| Foundation Cosmetics Products | How do competing products position themselves on Amazon? | JSON parsing, competitive analysis |
| Instacart | How do customers shop for groceries online? | exploratory analysis, market basket analysis, segmentation |
| Walmart Sales Forecasting | How much will each store and department sell in the coming weeks? | time-series features, forecasting baselines, XGBoost |
| Financial Data Analysis with LLMs | How can an LLM help analyze a company's annual report, and how do we check its answers? | SEC EDGAR, edgartools, LLM APIs, structured outputs |
| Campustown Zillow Listings | Where are the best single-family home opportunities across campus towns? | end-to-end analysis, price modeling, spaCy features, price history |

## Learning objectives

By the end of this course, you will be able to:

- clean and reshape real-world data from CSV, JSON, and Parquet sources using pandas and Polars
- explain how Polars and DuckDB speed up work on large datasets compared with a traditional pandas workflow, and write SQL queries, including window functions, with DuckDB
- build classification, regression, and forecasting models with scikit-learn and XGBoost, and evaluate them against simple baselines on properly held-out data
- recognize data leakage and other evaluation mistakes, and explain how they inflate reported performance
- turn unstructured text into features with NLP techniques, and use an LLM API to extract structured information while verifying its outputs
- create clear, interactive visualizations with Plotly that support a business argument
- communicate analytical findings and their limitations to a non-technical audience

## Prerequisites

- BDI 475 or equivalent experience with Python and pandas (loading data, filtering, grouping, and plotting).
- Basic statistics: distributions, averages and medians, correlation, and the idea of a training and test split.

## Setup

All notebooks run with the Python packages listed in `requirements.txt` at the root of the textbook repository. Create a virtual environment with Python 3.13, then install the packages once:

```bash
python -m pip install -r requirements.txt
```

Most notebooks download their data from a public URL when they run. Each case overview explains where its data comes from and any extra setup it needs, such as an API key for the LLM chapter.
