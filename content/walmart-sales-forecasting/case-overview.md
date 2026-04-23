# Walmart Sales Forecasting Case Overview

Walmart is the largest retailer in the world and operates thousands of stores
across the United States. Like every retailer, Walmart needs accurate sales
forecasts to plan inventory, schedule staff, run promotions, and negotiate
with suppliers. Forecasting _too high_ leaves shelves overstocked and ties up
working capital; forecasting _too low_ leads to empty shelves, lost sales,
and unhappy customers. In this case study we step into the role of a
business analyst who has been asked to build a weekly sales forecast for a
collection of Walmart stores and departments.

## Dataset

We will use the public **Walmart Recruiting — Store Sales Forecasting**
dataset originally released by Walmart on Kaggle. It contains historical
weekly sales for 45 Walmart stores located in different regions of the U.S.,
along with store-level attributes and a number of contextual features such
as temperature, fuel price, and promotional markdowns.

- **Source:** [Walmart Recruiting — Store Sales Forecasting (Kaggle)](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting)
- **Mirror used in this book:** [`bdi593/datasets/walmart-store-sales-forecasting`](https://github.com/bdi593/datasets/tree/main/walmart-store-sales-forecasting)
- **Time range:** February 2010 — November 2012 (weekly observations)
- **Granularity:** one row per `(Store, Department, Week)`

The data ships in three files:

| File           | Grain                             | Description                                                                                                 |
| -------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `stores.csv`   | one row per store                 | Store **type** (`A`, `B`, `C`) and **size** in square feet for each of the 45 stores.                       |
| `features.csv` | one row per `(Store, Week)`       | Weekly store-level context: `Temperature`, `Fuel_Price`, `MarkDown1-5`, `CPI`, `Unemployment`, `IsHoliday`. |
| `train.csv`    | one row per `(Store, Dept, Week)` | The target series: `Weekly_Sales` for each department, plus a holiday flag.                                 |

## Learning Objectives

By the end of this case study you should be comfortable:

1. **Loading, joining, and cleaning** multi-table retail data with `pandas`.
2. **Exploring time-series data** with `plotly express` — distributions,
   trends, seasonality, holiday effects, and store/department mix.
3. **Engineering time-series features** such as calendar parts, lagged
   sales, and rolling means.
4. **Splitting time-series data correctly** (no random shuffles!) and
   choosing a sensible **baseline** to beat.
5. **Training and tuning forecasting models**, ranging from simple
   **linear regression** all the way to **gradient-boosted trees** with
   `scikit-learn` and `xgboost`.
6. **Evaluating regression forecasts** using **MAE**, **RMSE**, and
   Walmart's competition metric, **WMAE** (weighted MAE that triples the
   weight of holiday weeks).
7. **Interpreting feature importance** and translating model output into
   actionable business recommendations.

## Algorithms You Can Practice with This Dataset

The dataset is unusually rich for a teaching example because it supports
several _families_ of forecasting techniques:

- **Classical statistical forecasting** — naive / seasonal-naive baselines,
  exponential smoothing (ETS), ARIMA / SARIMA at the store-department
  level.
- **Regression-based forecasting** — linear regression, ridge / lasso, and
  generalized linear models with calendar and lag features.
- **Tree-based machine learning** — random forests, gradient-boosted trees
  (`xgboost`, `lightgbm`), which excel on tabular retail data and naturally
  handle categorical features and non-linear interactions.
- **Hierarchical forecasting** — combining store-level, department-level,
  and chain-level forecasts for consistency.
- **Deep learning (advanced)** — sequence models such as LSTMs or temporal
  fusion transformers, useful when you have many related series.

In this book we will focus on the **regression** and **tree-based** routes
because they translate most directly to the kinds of tabular forecasting
problems analysts encounter in industry.

## Real-World Applications

The techniques you practice here are reused — almost unchanged — in many
parts of the economy:

- **Retail demand planning.** Grocery, fashion, and big-box retailers all
  forecast weekly or daily sales by store and SKU to drive replenishment.
- **Supply chain and inventory.** Warehouses and distribution centers use
  forecasts to decide how much stock to hold and when to reorder, balancing
  carrying cost against stock-out risk.
- **Workforce planning.** Sales forecasts feed staffing models for
  cashiers, stockers, baristas, and call-center agents.
- **Promotions and pricing.** The MarkDown columns in this dataset are a
  direct analogue to the promotional calendars retailers use today;
  forecasting the _uplift_ of a markdown is a multibillion-dollar problem.
- **Energy and utilities.** Weekly load forecasting uses the same
  combination of weather, calendar, and lag features.
- **Financial services.** Branch-level transaction volume forecasts and
  ATM cash-replenishment models share the same structure.

## How This Case Study is Organized

1. **Exploratory Data Analysis (EDA)** — load each file, profile the
   columns, look at distributions and time trends, and uncover the holiday
   and seasonality patterns we will need to model.
2. **Build a Forecasting Model** — engineer features, do a proper
   time-based train/test split, train a baseline and an ML model, evaluate
   with MAE / RMSE / WMAE, and discuss how to improve the results.

:::{tip} A note on scope
A full production forecasting system would also cover hierarchical
reconciliation, prediction intervals, retraining cadence, and monitoring.
We touch on these only briefly; the goal of this case is to ground the
fundamentals.
:::
