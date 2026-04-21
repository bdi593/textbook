# Improve the Classifier

In the previous notebook, we trained an XGBoost classifier on the Amazon on-time delivery dataset and evaluated it with accuracy, precision, recall, F1-score, ROC-AUC, and the confusion matrix. The baseline model reached roughly **83% accuracy** and **0.91 ROC-AUC**.

This page describes the techniques most commonly used in industry to push those numbers higher — and, just as importantly, to make the model more robust and useful for the business.

:::{important} What "better" means
Before optimizing, decide which metric matters most for the **business decision** the model supports. For on-time prediction, recall on the "Delayed" class might be more valuable than overall accuracy if the cost of a missed delay (an unhappy customer) is higher than the cost of a false alarm (an unnecessary intervention).
:::

## A Map of the Techniques

```{list-table}
:header-rows: 1

* - Approach
  - When to try it
  - Likely effect on metrics
* - Hyperparameter tuning
  - You have a working model and want to squeeze out more performance
  - Modest, broad improvements to accuracy / AUC / F1
* - Feature engineering
  - You suspect important business signal is hidden in the raw columns
  - Often the largest single gain
* - Handling class imbalance
  - One class is much rarer than the other
  - Improves recall on the minority class
* - Threshold tuning
  - Cost of false positives ≠ cost of false negatives
  - Trades precision against recall without retraining
* - Cross-validation
  - You want a more reliable estimate of generalization
  - Reduces variance of reported metrics
* - Regularization & early stopping
  - The model overfits the training data
  - Smaller train–test gap, better held-out AUC
* - Ensembling / model stacking
  - You have several decent models with different strengths
  - Small but consistent gains in F1 / AUC
```

## 1. Hyperparameter Tuning

XGBoost exposes many hyperparameters, and the defaults are rarely optimal for a specific dataset. The hyperparameters with the largest practical impact are usually:

- `n_estimators` — number of boosting rounds
- `learning_rate` — shrinkage applied to each new tree
- `max_depth` — depth of each tree
- `min_child_weight` — minimum sum of instance weight in a leaf
- `subsample` — fraction of rows sampled per tree
- `colsample_bytree` — fraction of columns sampled per tree
- `reg_alpha` (L1) and `reg_lambda` (L2) — regularization

There are three search strategies you will see in practice:

1. **Grid search** — exhaustive over a small, hand-picked grid. Simple, but expensive.
2. **Random search** — sample combinations randomly. Usually finds a near-optimal point much faster than grid search.
3. **Bayesian / sequential search** (e.g., Optuna, Hyperopt) — uses past trials to choose the next combination intelligently. State of the art for tabular models.

:::{tip} Pair tuning with cross-validation
Tune hyperparameters using cross-validated scores rather than a single train/test split. Otherwise you risk picking parameters that overfit the validation fold.
:::

```python
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBClassifier

param_dist = {
    "n_estimators":     [200, 400, 600, 800],
    "learning_rate":    [0.01, 0.03, 0.05, 0.1],
    "max_depth":        [3, 4, 5, 6, 8],
    "min_child_weight": [1, 3, 5, 10],
    "subsample":        [0.6, 0.8, 1.0],
    "colsample_bytree": [0.6, 0.8, 1.0],
    "reg_lambda":       [0.5, 1.0, 2.0, 5.0],
}

search = RandomizedSearchCV(
    estimator=XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=42,
    ),
    param_distributions=param_dist,
    n_iter=40,
    scoring="roc_auc",
    cv=5,
    n_jobs=-1,
    random_state=42,
)

search.fit(X_train, y_train)
print("Best ROC-AUC:", search.best_score_)
print("Best params:", search.best_params_)
```

## 2. Early Stopping

Rather than fixing `n_estimators` ahead of time, you can let XGBoost stop adding trees when validation performance plateaus. This usually gives a better-regularized model and saves training time.

```python
xgb_model = XGBClassifier(
    n_estimators=2000,
    learning_rate=0.03,
    max_depth=5,
    early_stopping_rounds=50,
    eval_metric="auc",
    random_state=42,
)

xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False,
)
```

## 3. Feature Engineering

Feature engineering is typically the single highest-leverage thing you can do for a tabular model. A few patterns that work well on operational data like Amazon deliveries:

- **Interaction features** — combine related columns (e.g., `temperature × precipitation`, `total_items / number_of_trucks`).
- **Aggregations** — group-level statistics (e.g., the average delay rate for each `zipcode` over the last 30 days).
- **Calendar features** — day of week, month, "is holiday", "is end of month" flags. Logistics performance is highly seasonal.
- **Weather binning** — convert continuous temperature into business-meaningful bins (freezing / cold / mild / hot).
- **Log or square-root transforms** of skewed numeric features (e.g., `log1p(total_items)`).
- **Target encoding** for high-cardinality categoricals such as `zipcode`. Use cross-fold target encoding to avoid leakage.

:::{caution} Avoid leakage
Any feature you build must be computable using **only information available at prediction time**. For example, an "average delay rate per zipcode" must be calculated from past data only — never from the test set.
:::

## 4. Handling Class Imbalance

Our target is moderately imbalanced (~58% Delayed / ~42% On time). For more skewed problems, three techniques are common:

1. **`scale_pos_weight`** in XGBoost — re-weights the positive class. A reasonable starting value is `count(negatives) / count(positives)`.
2. **Resampling** — oversample the minority class (e.g., `imblearn.SMOTE`) or undersample the majority class.
3. **Cost-sensitive learning** — pass `sample_weight` to `.fit()` so that misclassifying the rare class incurs a larger penalty.

```python
from collections import Counter

counts = Counter(y_train)
spw = counts[0] / counts[1]

xgb_model = XGBClassifier(
    scale_pos_weight=spw,
    objective="binary:logistic",
    eval_metric="aucpr",  # PR-AUC is more informative for imbalanced data
    random_state=42,
)
```

## 5. Threshold Tuning

`predict()` uses a default decision threshold of 0.5. Moving the threshold lets you trade precision for recall **without retraining**.

```python
import numpy as np
from sklearn.metrics import precision_recall_curve, f1_score

y_proba = xgb_model.predict_proba(X_test)[:, 1]
prec, rec, thr = precision_recall_curve(y_test, y_proba)

f1 = 2 * prec * rec / (prec + rec + 1e-12)
best_idx = np.nanargmax(f1)
print(f"Best threshold for F1: {thr[best_idx]:.3f}, F1={f1[best_idx]:.3f}")
```

:::{tip} Pick a threshold that reflects business cost
If a missed delay costs the company 10× more than a false alarm, choose the threshold that minimizes `10 * FN + 1 * FP` rather than the one that maximizes F1.
:::

## 6. Cross-Validation

A single 80/20 split gives one estimate of model quality. **Stratified k-fold cross-validation** gives `k` estimates and reports their mean and variance, which is much more reliable.

```python
from sklearn.model_selection import cross_val_score, StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(xgb_model, X, y, cv=cv, scoring="roc_auc")
print(f"ROC-AUC: {scores.mean():.3f} ± {scores.std():.3f}")
```

## 7. Try a Different Model Family

XGBoost is an excellent default for tabular data, but it is worth comparing against:

- **LightGBM** — often faster than XGBoost, with comparable accuracy.
- **CatBoost** — handles categorical features natively, useful when you have many high-cardinality columns like `zipcode`.
- **Logistic regression** with engineered features — a strong, interpretable baseline.
- **Random forest** — less prone to overfitting than a single tree, useful as a sanity check.

A quick comparison table on the same train/test split is often the fastest way to see whether you are on the right track.

## 8. Ensembling

Once you have several reasonable models, you can combine them:

- **Soft voting** — average the predicted probabilities of multiple models.
- **Stacking** — train a "meta-model" (often logistic regression) on the out-of-fold predictions of base learners.

Ensembles rarely produce dramatic gains, but they often add 1–3% AUC on top of the best single model and reduce variance.

## A Suggested Workflow

For most tabular projects, a productive order of operations is:

1. Lock in a clean train/validation/test split (or cross-validation scheme).
2. Get a simple model (logistic regression or default XGBoost) working end to end.
3. Invest in **feature engineering** until improvements taper off.
4. Address **class imbalance** if relevant.
5. Run **hyperparameter search** with **early stopping** and cross-validation.
6. **Tune the decision threshold** to match the business cost structure.
7. Compare against alternative model families and consider **ensembling** the best two or three.

## How Classifiers Are Used in the Real World

Binary and multi-class classifiers are among the most widely deployed machine-learning systems at large companies. A few well-documented examples:

:::{seealso} Real-world classifier examples

**Amazon — Fulfillment, fraud, and recommendations**
: Amazon uses classifiers throughout its operations. Within fulfillment, models predict whether a shipment will arrive on time so the company can proactively reroute orders or notify customers. Amazon's [Fraud Detector](https://aws.amazon.com/fraud-detector/) service productizes the same underlying technology — gradient-boosted classifiers that score events as fraudulent or legitimate in real time.

**Netflix — Personalization**
: Netflix uses classifiers to decide which artwork to show for a given title, which row of recommendations to surface, and whether a user is likely to abandon a session. The company has [written extensively](https://netflixtechblog.com/) about how small classification gains translate into large engagement and retention improvements.

**Google — Spam and abuse detection**
: Gmail uses deep neural-network classifiers to filter spam and phishing, [blocking more than 99.9% of spam, phishing, and malware](https://workspace.google.com/blog/identity-and-security/improving-spam-filter-with-tensorflow). Similar models power abuse detection across YouTube and Google Ads.

**Meta — Content moderation and ad ranking**
: Meta runs classifiers that flag potentially policy-violating content (hate speech, graphic violence, misinformation) at the scale of billions of posts per day. Separate classifier stacks predict the probability that a user will click, like, or comment on a piece of content, which directly drives ad and feed ranking.

**Uber — ETA confidence and fraud**
: Uber uses gradient-boosted classifiers to predict whether a trip's actual arrival time will deviate significantly from the estimate, and to flag suspicious driver or rider accounts. The [Michelangelo platform](https://www.uber.com/blog/michelangelo-machine-learning-platform/) provides shared infrastructure for training and serving these models.

**Airbnb — Trust and search ranking**
: Airbnb uses classifiers to estimate the probability that a booking is fraudulent, that a host will accept a request, and that a guest will book a given listing. These signals feed both the trust system and the [search ranking model](https://medium.com/airbnb-engineering/).

**Capital One and JPMorgan Chase — Credit and fraud**
: Major US banks use classifiers to decide whether to approve a credit application and to score every card transaction in real time for fraud. Modern stacks combine gradient-boosted trees with deep learning, evaluated primarily on precision–recall metrics rather than accuracy because fraud is highly imbalanced.

**UPS and FedEx — Logistics**
: Shipping companies use on-time-delivery classifiers very similar to the model in this case study to forecast service exceptions, reroute parcels, and staff distribution centers ahead of weather events.

:::

The common thread across these examples is that the **business decision drives the metric**. None of these companies optimize raw accuracy; they optimize a composite that reflects the dollar cost of false positives versus false negatives, the latency budget of the serving system, and how the model's output will be acted on. As you improve the Amazon delivery classifier, frame each change the same way: which metric does it move, and why does that matter for the customer or the business?
