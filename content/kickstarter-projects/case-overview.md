# Kickstarter Projects Case Overview

[Kickstarter](https://www.kickstarter.com/) is a popular crowdfunding platform that allows creators to raise funds for their projects by soliciting contributions from a large number of people. The dataset we will be working with contains information about various Kickstarter projects, including their categories, funding goals, amounts pledged, and other relevant details.

```{figure} images/kickstarter-screenshot.jpg
:label: Kickstarter
:alt: Kickstarter
:align: center

Kickstarter Wearable Projects
```

## Business Context

Creators, backers, and the platform itself all want to know which projects are likely to reach their funding goal. A creator can adjust the goal or the pitch before launch. A platform can decide which projects to promote. A backer can decide where to put their money. In this case study, we prepare a sample of Kickstarter projects for analysis and ask a focused question: **using only what is known on launch day, can we predict whether a project will succeed?**

Answering that question well also means spotting the ways a model can look better than it is. This case study is built around two of them: a feature that leaks the outcome, and a sample that is not representative of the platform.

## Learning Objectives

After working through this case study, you will be able to:

- Read a messy CSV export with Polars, handling `"null"` strings and duplicate records.
- Convert epoch timestamps to datetimes and extract fields from JSON strings with regular expressions or a JSON parser.
- Engineer simple date, video, and category features for a classifier.
- Train an XGBoost classifier on a mix of numeric and categorical features.
- Compare a model against a majority-class baseline and a category-majority baseline.
- Recognize data leakage (`backers_count` and `spotlight`) and a sampling artifact, and measure their effect on the results.
- Interpret accuracy, precision, recall, F1, ROC AUC, and gain-based feature importance.

## Dataset

The raw sample contains 3,173 Kickstarter projects with 42 columns, such as project ID, name, category, currency, deadline, goal, pledged amount, state (e.g., successful, failed), and backers count. After removing duplicates and keeping only finished campaigns, 2,701 projects remain.

While the dataset is rich in information, it requires some preprocessing to make it suitable for analysis. This includes selecting relevant columns, filtering based on project state, checking the distribution of boolean columns, and converting epoch timestamps to datetime format.

Some columns contain nested JSON information, such as the `"video"` column, which needs parsing to extract details about the project's video. Similarly, the `"category"` column contains hierarchical information that can be parsed into a category and a parent category.

While parsing JSON columns is not a particularly difficult task, it can be time-consuming if you encounter malformed JSON data. Therefore, it is important to handle such cases gracefully, perhaps by using error handling techniques or alternative methods like regular expressions to extract relevant information without fully parsing the JSON.

### Key Columns

The preprocessing notebook keeps these 15 of the 42 raw columns.

| Column             | Description                                                                                                    |
| ------------------ | -------------------------------------------------------------------------------------------------------------- |
| `name`             | Project name.                                                                                                  |
| `state`            | Campaign status. The raw file also has `canceled`, `live`, `started`, and `submitted`; we keep `successful` and `failed`. |
| `backers_count`    | Number of backers when the data was collected. For a finished campaign this is the final count.               |
| `usd_pledged`      | Amount pledged, converted to US dollars.                                                                       |
| `goal`             | Funding goal, in the project's own currency.                                                                   |
| `percent_funded`   | Amount pledged as a percentage of the goal.                                                                    |
| `launched_at`      | Launch time as a Unix timestamp (seconds).                                                                     |
| `state_changed_at` | Time of the last change of `state`, as a Unix timestamp (seconds).                                             |
| `country`          | Country code of the project.                                                                                   |
| `currency`         | Currency of the campaign.                                                                                      |
| `staff_pick`       | Whether the project was selected as a staff pick by Kickstarter.                                               |
| `spotlight`        | Boolean flag. In this sample it matches the outcome exactly, so it is a label, not a feature.                  |
| `category`         | JSON string with the category name and its parent category.                                                    |
| `video`            | JSON string with details of the pitch video, or null if there is no video.                                     |
| `blurb`            | Short description of the project.                                                                              |

### Source and Licence

The raw data comes from the [Kickstarter datasets published by Web Robots](https://webrobots.io/kickstarter-datasets/). Web Robots runs a scraper that crawls Kickstarter projects and publishes the results in CSV and JSON formats. This case study uses a small sample hosted in the course [datasets repository](https://github.com/bdi593/datasets/tree/main/kickstarter-projects). Check the source page for terms of use.

:::{caution} This is not a random sample

The sample is good practice material for data preparation, but it does not represent all Kickstarter projects. More than half of its categories contain only successful projects or only failed projects. The classification notebook shows how this inflates model accuracy, so treat category-level results from this sample with care.

:::

## Notebooks in This Case Study

| Notebook                                                          | What it covers                                                                                                                                                                                  |
| ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Preprocessing Kickstarter Data with Polars](./preprocess-data.ipynb) | Reads the raw CSV with Polars, removes duplicate projects, keeps finished campaigns, converts timestamps, parses the JSON columns, and saves the result as Parquet.                              |
| [Predicting Kickstarter Project Success](./binary-classification.ipynb) | Builds two baselines and XGBoost classifiers, measures the effect of the leaky `backers_count` feature and of the category artifact, and interprets the metrics and feature importance. |

## Setup

Install the packages used across the book from the root of the repository:

```bash
python -m pip install -r requirements.txt
```

Both notebooks download their data from the course datasets repository, so you need an internet connection. No other setup is needed.

## Questions to Explore

The notebooks focus on data preparation and on a classifier. The preprocessed sample can also answer descriptive questions like the ones below. They are left for you to explore. Keep the sampling caveat above in mind when you interpret category-level results.

### Overall Success Rates

- What is the overall success rate?
- What is the mean and median pledged amount for successful vs failed projects?

### Category

- Which categories have the highest success rates?
- Which parent categories perform the best?
- Are some categories high funding but low success?

### Geography

- Which countries have the highest success rates?
- Does average pledged amount differ by country?
- Is the US materially different?

### Staff Pick

- What is the success rate for staff picks vs non-staff picks?
- Why is the `spotlight` flag not a useful question here? (Compare it with `state`.)

### Videos

- Do projects with videos have higher success rates?
- Do higher resolution videos correlate with higher success rates?
