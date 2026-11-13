# Amazon Delivery Case Overview

```{figure} images/amazon-hero3.jpg
:label: Amazon Delivery
:alt: Amazon Delivery
:align: center

Amazon Delivery - Photo from [Amazon News](https://www.aboutamazon.com/news/amazon-prime/amazon-same-day-delivery)
```

## Business Context

As a business analyst working for a company in the logistics sector, you have the following tasks:

1. Analyze the delivery data that has been prepared for you.
2. Build a first model and analyze its prediction score.
3. Improve the accuracy of your delivery predictions.

A model that flags likely delays ahead of time lets the company act before customers are affected: reroute or split loads, add capacity, or warn customers.

The target is to correctly predict package delivery on-time status for your customers with an accuracy of **80% or better**.

### Evaluation

This dataset comes from a tutorial and does not have a formal evaluation metric. The working goal is an accuracy of 80% or better when predicting on-time delivery status, while also tracking complementary metrics such as precision, recall, F1, and ROC-AUC.

:::{attention} Check the goal against a baseline

An accuracy target only means something next to a baseline. The notebooks show that a single rule on one column, `total_items`, already reaches about 81% accuracy, because of how the "Delayed" label is defined. Keep this in mind when you judge any model built on this data.

:::

## Learning Objectives

After working through this case study, you will be able to:

- Run a structured exploratory data analysis: data types, missing values, duplicates, constant columns, skewness, outliers, and correlations with the target.
- Keep notebooks small by aggregating data (counts, bins, or quartiles) before plotting with Plotly.
- Train an XGBoost binary classifier and evaluate it with a confusion matrix, accuracy, precision, recall, F1, and ROC-AUC.
- Compare a model against a majority-class baseline and a one-feature baseline, and recognize when a feature is built into the label.
- Use a validation set correctly for early stopping and threshold tuning, and compare several improvement techniques on one test set.

## Dataset

This case study uses an Amazon delivery dataset of 45,000 samples collected over a period of three months. A delivery is labeled **Delayed** when, on a specific day, at least 10 items from a single truck arrived late.

- **Columns:** 16
- **Rows:** 45,000

### Data Dictionary

| Column                  | Description                                                                                                  |
| ----------------------- | ------------------------------------------------------------------------------------------------------------ |
| `zipcode`               | US ZIP code of the delivery, stored as an integer (so leading zeros are dropped). An identifier, not a quantity. |
| `total_items`           | Number of items on the delivery truck.                                                                       |
| `precipitation_rate`    | Precipitation rate. It is 0 in every row of this file.                                                       |
| `water_runoff`          | Water runoff.                                                                                                |
| `snow_depth`            | Snow depth.                                                                                                  |
| `temperature`           | Air temperature, in °C.                                                                                      |
| `temperature_at_1500m`  | Air temperature at 1,500 m.                                                                                  |
| `min_temperature`       | Minimum temperature.                                                                                         |
| `max_temperature`       | Maximum temperature.                                                                                         |
| `pressure`              | Air pressure.                                                                                                |
| `wind_gust_speed`       | Wind gust speed.                                                                                             |
| `total_cloud_cover`     | Total cloud cover.                                                                                           |
| `dew_point_temperature` | Dew point temperature.                                                                                       |
| `relative_humidity`     | Relative humidity, in %.                                                                                     |
| `wind_speed`            | Wind speed.                                                                                                  |
| `classification_ontime` | Target: `"Delayed"` or `"On time"`.                                                                          |

The source documents units only for temperature and relative humidity. It does not say where or when the weather was measured, and the file has no date, truck, or route column.

### Source and Licence

The data comes from [AI Package Tracker](https://aipackagetracker.awsplayer.com/), an interactive AWS demo for Amazon SageMaker Canvas, a no-code machine learning tool. The demo describes it as a real Amazon delivery dataset and gives the label definition above. In this case study we work with the same data in Python, so you do not need Canvas or an AWS account. The course hosts a copy in the [datasets repository](https://github.com/bdi593/datasets/tree/main/amazon-on-time-delivery-data). Check the source page for terms of use.

## Notebooks in This Case Study

| Notebook                                                     | What it covers                                                                                                                                                                                                                  |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Exploratory Data Analysis](./eda.ipynb)                     | Data types, missing values, the target balance, distributions and box plots of every numeric feature, correlations, duplicates, constant columns, outliers, and skewness.                                                       |
| [Build a Binary Classification Model](./build-a-classifier.ipynb) | Prepares features, trains an XGBoost classifier, explains the confusion matrix and each metric, and shows why `total_items` dominates feature importance with a one-feature baseline.                                     |
| [Improve the Classifier](./improve-classifier.ipynb)         | Tries random search, early stopping, feature engineering, class weights, and threshold tuning, estimates variability with cross-validation, and compares every technique with the baseline on the same test set.               |

## Setup

Install the packages used across the book from the root of the repository:

```bash
python -m pip install -r requirements.txt
```

All three notebooks download the data from the course datasets repository, so you need an internet connection. No other setup is needed.

## Gradient Boosted Trees

A **gradient boosted tree** is a machine learning model that builds many small decision trees sequentially, where each new tree is trained to correct the mistakes of the previous ones.

It combines two ideas:

1. Decision trees
2. Gradient boosting

### Decision Tree (the base learner)

A decision tree:

- Splits data into regions using if-then rules
- Makes predictions at the leaves
- Is easy to interpret
- Can capture nonlinear relationships

But a single tree often:

- **Overfits** if it is allowed to grow too deep, or
- **Underfits** if it is too shallow

### Boosting

Boosting means:

> Build models sequentially, where each new model focuses on fixing the errors of the previous model.

Unlike random forests (which build trees independently), boosting builds trees one after another.

:::{seealso} Where does "Gradient" come from?

The word _gradient_ comes from calculus.

In gradient boosting:

- We define a loss function (e.g., log loss for classification).
- We compute the gradient (slope) of that loss.
- Each new tree is trained to predict the negative gradient (the direction that reduces error).

So each new tree moves the model in the direction that most reduces the loss.

That's why it's called _Gradient Boosted_ Decision Trees.

:::

### Step-by-step Intuition

For binary classification:

#### Step 1: Start simple

Begin with a very basic prediction (like predicting the average probability).

#### Step 2: Measure mistakes

Calculate how wrong those predictions are (using log loss).

#### Step 3: Fit a small tree

Train a shallow tree to predict the errors.

#### Step 4: Update predictions

Add that tree's predictions (scaled by learning rate).

#### Step 5: Repeat

Build another tree to fix the new residual errors.

Do this hundreds of times. The final prediction is the sum of all the trees' predictions.
