# BDI 199/593: Advanced Analytics Applications in Business

[![Jupyter Book](https://img.shields.io/badge/Jupyter%20Book-v2-blue)](https://jupyterbook.org)

An online textbook for **BDI 199/593: Advanced Analytics Applications in Business** at the **University of Illinois Urbana-Champaign**.

- **Instructor**: Ye Joo Park ([ypark32@illinois.edu](mailto:ypark32@illinois.edu))

This course builds upon the data analytics foundations from BDI 475 and equips students with advanced skills in business analytics, focusing on handling large-scale data, performing sophisticated analyses, and creating impactful visualizations.

---

## 📚 Case Studies

The textbook is organized around real-world business analytics case studies:

| Case Study | Topics |
|---|---|
| **Cleaning Airbnb Listings** | Data cleaning, pandas, missing values, type conversion |
| **Credit Card Transactions** | Polars, DuckDB, SQL window functions, large-scale data processing, fraud flags |
| **Kickstarter Projects** | Polars preprocessing, binary classification, data leakage |
| **Data Job Postings** | EDA, HR analytics |
| **Amazon On-time Delivery** | Classification, model improvement, threshold tuning |
| **Australian Rental Market** | Regression, feature engineering, target encoding |
| **Conference Calls** | NLP preprocessing, text analytics |
| **CU+Savoy Zillow Properties** | Real estate data analysis |
| **Foundation Cosmetics Products** | JSON parsing, competitive analysis |
| **Instacart** | Customer behavior analysis, EDA, market basket analysis |
| **Walmart Sales Forecasting** | Time-series forecasting, baselines, XGBoost |
| **Financial Data Analysis with LLMs** | SEC EDGAR filings, LLM APIs, structured outputs, output verification |
| **Campustown Zillow Listings** | End-to-end final case study: EDA, price modeling, NLP features, price history |

---

## 🗂️ Repository Structure

```
textbook/
├── myst.yml                   # Book configuration and table of contents
├── requirements.txt           # Pinned Python packages for all notebooks
├── content/                   # Textbook chapters and case studies
│   ├── index.md               # Book landing page
│   ├── airbnb-barcelona-listings/
│   ├── credit-card-transactions/
│   ├── kickstarter-projects/
│   ├── data-job-postings/
│   ├── amazon-delivery/
│   ├── australian-rental-market/
│   ├── conference-calls/
│   ├── cu-zillow-listings/
│   ├── foundation-products/
│   ├── instacart/
│   ├── walmart-sales-forecasting/
│   ├── financial-data-with-llms/
│   └── campustown-zillow-listings/
├── docs/                      # Maintainer notes (not part of the book)
├── site_images/               # Logo and favicon assets
└── media/                     # Custom CSS and media assets
```

Each case study folder typically contains:
- A `case-overview.md` introducing the business problem and dataset
- One or more teaching notebooks (`.ipynb`) with hands-on exercises

---

## 🛠️ Authoring Stack

This project uses **[Jupyter Book v2](https://jupyterbook.org)** with **[MyST Markdown](https://mystmd.org)**. The book configuration and table of contents are defined in `myst.yml`.

### Python environment

All notebooks run with the packages pinned in `requirements.txt` (tested with Python 3.13):

```bash
python -m pip install -r requirements.txt
```

### Building the Book

```bash
jupyter-book build --html
```

> **Note**: The build requires access to the MyST template API. In restricted network environments, the build may fail if the API cannot be reached.

Notebooks are not executed during the build. The published pages show the outputs saved in each notebook, so re-run a notebook top to bottom before committing changes to it.

### Checks

Every pull request runs `.github/workflows/check.yml`, which builds the book and runs `.github/scripts/check_notebooks.py`. The script fails if a notebook is larger than 5 MB, contains a saved error, or shows a local file path in its outputs. Run it locally with:

```bash
python .github/scripts/check_notebooks.py
```

---

## 🎯 Learning Objectives

By the end of this course, students will be able to:

- Clean and reshape real-world data from CSV, JSON, and Parquet sources using pandas and Polars
- Explain how Polars and DuckDB speed up work on large datasets compared with pandas, and write SQL queries with DuckDB
- Build classification, regression, and forecasting models and evaluate them against simple baselines on held-out data
- Recognize data leakage and other evaluation mistakes
- Turn unstructured text into features with NLP, and use an LLM API while verifying its outputs
- Create clear, interactive Plotly visualizations and communicate findings to a non-technical audience

---

## 📄 License

Course materials are intended for educational use at the University of Illinois Urbana-Champaign.
