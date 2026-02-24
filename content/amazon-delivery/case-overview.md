# Case Overview

```{figure} images/amazon-hero3.jpg
:label: Amazon Delivery
:alt: Amazon Delivery
:align: center

Amazon Delivery - Photo from [Amazon News](https://www.aboutamazon.com/news/amazon-prime/amazon-same-day-delivery)
```

## Dataset

This is a real Amazon delivery dataset of 45k samples taken over a period of 3 months. Delayed means that on a specific day, at least 10 items from one truck were delayed.

- Source: [AWS SageMaker Canvas Tutorial - AI Package Tracker](https://aipackagetracker.awsplayer.com/)
- 16 Columns
- 45,000 Rows

## Objective

As a business analyst working for a company in the logistics sector, you have the following tasks:

1. Analyze the data we already prepared for this demo.
2. Build your first model and analyze its prediction score.
3. Improve the accuracy of your delivery predictions.

Correctly predict package delivery on-time status for your customers with an accuracy of 80% or better.

## Dataset Description

In this demo, we are using a real Amazon delivery dataset of 45k samples taken over a period of 3 months. Delayed means that on a specific day, at least 10 items from one truck were delayed.

## Evaluation

This dataset is used for a tutorial and does not have a formal evaluation metric. However, the goal is to achieve an accuracy of 80% or better in predicting on-time delivery status.

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

- Overfits (if deep), or
- Underfits (if shallow)

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
