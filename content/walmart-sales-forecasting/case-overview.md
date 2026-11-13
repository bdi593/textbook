# Walmart Sales Forecasting Case Overview

Walmart is the largest retailer in the world and operates thousands of stores
across the United States. Like every retailer, Walmart needs accurate sales
forecasts to plan inventory, schedule staff, run promotions, and negotiate
with suppliers. Forecasting _too high_ leaves shelves overstocked and ties up
working capital; forecasting _too low_ leads to empty shelves, lost sales,
and unhappy customers. In this case study we step into the role of a
business analyst who has been asked to build a weekly sales forecast for a
collection of Walmart stores and departments, 12 weeks ahead.

## Real-World Applications

The techniques you practice here are reused (almost unchanged) in many
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

## Learning Objectives

By the end of this case study you should be comfortable:

1. **Loading, joining, and cleaning** multi-table retail data with `pandas`.
2. **Exploring time-series data** with `plotly express`: distributions,
   trends, seasonality, holiday effects, and store/department mix, and
   aggregating large tables before plotting them.
3. **Defining a forecast horizon** and **engineering time-series features**
   (calendar parts, lagged sales, rolling means) that use only information
   available when the forecast is made.
4. **Splitting time-series data correctly** (no random shuffles!) and
   comparing models with **naive baselines**: seasonal naive and
   persistence.
5. **Training forecasting models**, from a regularized linear model
   (Ridge) to **gradient-boosted trees**, with `scikit-learn` and
   `xgboost`.
6. **Evaluating regression forecasts** using **MAE**, **RMSE**, and
   Walmart's competition metric, **WMAE** (weighted MAE that gives holiday
   weeks five times the weight of other weeks), overall and by weeks ahead.
7. **Interpreting feature importance and residuals**, and relating forecast
   error to inventory and staffing decisions.

## Dataset

We will use the public **Walmart Recruiting: Store Sales Forecasting**
dataset originally released by Walmart on Kaggle. It contains historical
weekly sales for 45 Walmart stores located in different regions of the U.S.,
along with store-level attributes and a number of contextual features such
as temperature, fuel price, and promotional markdowns.

- **Time range:** weekly sales from February 2010 to October 2012
  (`train.csv`). The store-level context in `features.csv` continues to
  July 2013.
- **Granularity:** one row per `(Store, Department, Week)`

The notebooks use three files:

| File           | Grain                             | Description                                                                                                 |
| -------------- | --------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `stores.csv`   | one row per store                 | Store **type** (`A`, `B`, `C`) and **size** in square feet for each of the 45 stores.                       |
| `features.csv` | one row per `(Store, Week)`       | Weekly store-level context: `Temperature`, `Fuel_Price`, `MarkDown1-5`, `CPI`, `Unemployment`, `IsHoliday`. |
| `train.csv`    | one row per `(Store, Dept, Week)` | The target series: `Weekly_Sales` for each department, plus a holiday flag.                                 |

`IsHoliday` marks the weeks of four holidays: the Super Bowl, Labor Day,
Thanksgiving, and Christmas. The `MarkDown` columns are recorded only from
November 2011 onward. The competition's `test.csv` has no sales, so we do
not use it. Instead, the modeling notebook holds out the last 12 weeks of
`train.csv` as its test set.

:::{caution} Only one holiday in the test window

The 12 held-out weeks run from 10 August to 26 October 2012. The only
holiday week among them is Labor Day, so the model is never tested on
Thanksgiving or Christmas, the weeks with the largest sales swings.

:::

### Source and licence

The data comes from the Kaggle competition
[Walmart Recruiting - Store Sales Forecasting](https://www.kaggle.com/competitions/walmart-recruiting-store-sales-forecasting).
The course hosts a copy in the
[`bdi593/datasets` repository](https://github.com/bdi593/datasets/tree/main/walmart-store-sales-forecasting),
whose README reproduces the competition's data description. Check the
source page for terms of use.

## Notebooks in This Case Study

| Notebook                                                       | What it covers                                                                                                                                                                                                                                       |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Exploratory Data Analysis](./eda.ipynb)                       | Loads and profiles the three files, checks missing values, looks at the distribution and time trend of weekly sales, compares the four holidays, stores, and departments, and explores temperature, fuel price, CPI, unemployment, and markdowns. |
| [Build a Forecasting Model](./build-a-forecasting-model.ipynb) | Defines a 12-week forecast horizon, builds calendar and lag features that respect it, compares seasonal naive and persistence baselines with Ridge regression and XGBoost on MAE, RMSE, and WMAE, and examines error by weeks ahead, feature importance, and residuals. |

Read the EDA first. The modeling notebook loads the data again, so it also
runs on its own.

## Setup

Install the packages used across the book from the root of the repository:

```bash
python -m pip install -r requirements.txt
```

Both notebooks download the data from the course datasets repository, so
you need an internet connection. No other setup is needed.

## Algorithms You Can Practice with This Dataset

The dataset is unusually rich for a teaching example because it supports
several _families_ of forecasting techniques:

- **Classical statistical forecasting**: naive / seasonal-naive baselines,
  exponential smoothing (ETS), ARIMA / SARIMA at the store-department
  level.
- **Regression-based forecasting**: linear regression, ridge / lasso, and
  generalized linear models with calendar and lag features.
- **Tree-based machine learning**: random forests, gradient-boosted trees
  (`xgboost`, `lightgbm`), which excel on tabular retail data and naturally
  handle categorical features and non-linear interactions.
- **Hierarchical forecasting**: combining store-level, department-level,
  and chain-level forecasts for consistency.
- **Deep learning (advanced)**: sequence models such as LSTMs or temporal
  fusion transformers, useful when you have many related series.

In this book we focus on naive baselines and the **regression** and
**tree-based** routes, because they translate most directly to the kinds of
tabular forecasting problems analysts encounter in industry.

:::{tip} A note on scope
A full production forecasting system would also cover hierarchical
reconciliation, prediction intervals, retraining cadence, and monitoring.
We touch on these only briefly; the goal of this case is to ground the
fundamentals.
:::
