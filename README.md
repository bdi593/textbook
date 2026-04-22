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
| **Credit Card Transactions** | Polars, DuckDB, large-scale data processing, fraud detection |
| **Kickstarter Projects** | Binary classification, JSON parsing, preprocessing |
| **Data Job Postings** | EDA, HR analytics |
| **Amazon On-time Delivery** | Classification, model improvement |
| **Australian Rental Market** | Regression, model evaluation |
| **Conference Calls** | NLP preprocessing, text analytics |
| **CU+Savoy Zillow Properties** | Real estate data analysis |
| **Foundation Cosmetics Products** | JSON parsing, competitive analysis |
| **Instacart** | Customer behavior analysis, EDA |
| **Walmart Sales Forecasting** | Time-series forecasting, regression |

---

## 🗂️ Repository Structure

```
textbook/
├── myst.yml                   # Book configuration and table of contents
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
│   └── walmart-sales-forecasting/
├── site_images/               # Logo and favicon assets
└── media/                     # Custom CSS and media assets
```

Each case study folder typically contains:
- A `case-overview.md` introducing the business problem and dataset
- One or more teaching notebooks (`.ipynb`) with hands-on exercises

---

## 🛠️ Authoring Stack

This project uses **[Jupyter Book v2](https://jupyterbook.org)** with **[MyST Markdown](https://mystmd.org)**. The book configuration and table of contents are defined in `myst.yml`.

### Building the Book

```bash
jupyter-book build --html
```

> **Note**: The build requires access to the MyST template API. In restricted network environments, the build may fail if the API cannot be reached.

---

## 📖 Course Topics

1. **Load and Clean Data** — pandas, CSV/Excel/JSON/Parquet
2. **Handle Large-Scale Datasets** — Polars, out-of-memory operations, ETL
3. **Retrieve and Manage Data** — APIs, PostgreSQL, advanced SQL
4. **Natural Language Processing** — BERT, BERTopic, sentiment analysis
5. **Interactive Data Visualization** — Plotly, Dash, dashboards
6. **Cloud Computing for Analytics** — Serverless functions, cloud resources
7. **Applied Machine Learning** — Kaggle challenges, real-world ML projects
8. **Communicate Analytical Insights** — Storytelling, stakeholder presentations

---

## 🎯 Learning Objectives

By the end of this course, students will be able to:

- Explain how Polars and DuckDB enhance data processing performance compared to traditional pandas workflows
- Apply SQL queries in PostgreSQL to extract, filter, and join data from relational databases
- Analyze business scenarios using complex data manipulations and statistical modeling in Python
- Evaluate visualizations created with Plotly and Tableau for communicating business insights
- Design and present an interactive dashboard integrating findings from multiple analytical techniques

---

## 📄 License

Course materials are intended for educational use at the University of Illinois Urbana-Champaign.
