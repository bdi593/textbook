# Data Job Postings

In this case, we will use a real-world job postings dataset focused on data science and analytics roles. Luke Barousse collected the postings from 2023 with a bot that scraped Google job search results, which come from many job boards.

```{image} images/undraw_searching-everywhere_tffi.svg
:alt: Searching Everwhere - Undraw
:width: 360px
:align: center
```

&nbsp;

## 💼 Business Context

The market for data and analytics talent has matured rapidly over the last few years. Roles that barely existed a decade ago, such as _data engineer_, _machine learning engineer_, and _analytics engineer_, now appear in tens of thousands of postings each month. For job seekers, recruiters, hiring managers, and educators, this creates several questions:

- **Job seekers** want to know which titles are growing, which skills get the strongest premium, and how compensation differs by location and industry.
- **Recruiters and hiring managers** need to benchmark salary ranges, identify in-demand skills, and decide where to focus sourcing efforts.
- **Educators and bootcamps** use the data to keep curricula aligned with the skills employers actually request.
- **Workforce researchers** track how remote work, the rise of generative AI, and macroeconomic conditions reshape the labor market.

Real online postings give us a window into all of these questions. Each row tells us _what_ a company is hiring for, _where_, _under what conditions_, and increasingly, _for how much_.

## 🎯 Learning Objectives

By the end of this case study you should be able to:

1. Load and inspect a moderately large (~786,000 row) Parquet file with [Polars](https://pola.rs/).
2. Diagnose missing values and decide which columns are usable.
3. Parse "messy" string columns that look like Python lists or dictionaries into proper structured types (`List`, `Struct`).
4. Spot a suspicious value (a country that should not be there), find its cause in another column, and correct it.
5. Run common exploratory analyses at scale, including value counts, group-by aggregations, time-series counts, and skill frequencies.
6. Translate exploratory findings into HR analytics workflows: salary benchmarking with percentiles, talent-market mapping, and tracking changes in skill demand.

## 📌 Dataset Information

We have already covered common preprocessing steps for tabular data in the previous chapters, but this dataset also includes list-like or dictionary-like string columns that require additional parsing and transformation.

For example, the `job_skills` column contains a string representation of a list of skills extracted from the job posting using NLP techniques.

Additionally, the `job_type_skills` contain a Python dictionary-like string that map skill types (e.g., 'cloud', 'libraries') to sets of skills.

We will need to parse these string representations into actual Python data structures (lists and dictionaries) to work with them effectively in our analysis.

- **Format:** Parquet (original CSV file converted to Parquet for compression - no other preprocessing applied)
- **Size:** ~30 MB (~786,000 rows)
  - The original CSV file is much larger (~230 MB) due to the large number of rows and text fields, but the Parquet format significantly reduces the file size while preserving all data.
- **Period:** postings dated January to December 2023.

:::{caution} A known data-quality issue

All 21,781 postings found by the bot's "Sudan" search have `job_country` set to Sudan, but their `job_location` values are U.S. cities and states, "Anywhere", or "United States". The EDA notebook shows the evidence and relabels them as United States.

:::

### 📘 Data Dictionary

| Column Name             | Description                                                               | Type        | Source           |
| ----------------------- | ------------------------------------------------------------------------- | ----------- | ---------------- |
| `job_title_short`       | Cleaned/standardized job title using BERT model (10-class classification) | Calculated  | From `job_title` |
| `job_title`             | Full original job title as scraped                                        | Raw         | Scraped          |
| `job_location`          | Location string shown in job posting                                      | Raw         | Scraped          |
| `job_via`               | Platform the job was posted on (e.g., LinkedIn, Jobijoba)                 | Raw         | Scraped          |
| `job_schedule_type`     | Type of schedule (Full-time, Part-time, Contractor, etc.)                 | Raw         | Scraped          |
| `job_work_from_home`    | Whether the job is remote (`true`/`false`)                                | Boolean     | Parsed           |
| `search_location`       | Location used by the bot to generate search queries                       | Generated   | Bot logic        |
| `job_posted_date`       | Date and time when job was posted                                         | Raw         | Scraped          |
| `job_no_degree_mention` | Whether the posting explicitly mentions no degree is required             | Boolean     | Parsed           |
| `job_health_insurance`  | Whether the job mentions health insurance                                 | Boolean     | Parsed           |
| `job_country`           | Country extracted from job location                                       | Calculated  | Parsed           |
| `salary_rate`           | Indicates if salary is annual or hourly                                   | Raw         | Scraped          |
| `salary_year_avg`       | Average yearly salary (calculated from salary ranges when available)      | Calculated  | Derived          |
| `salary_hour_avg`       | Average hourly salary (same logic as yearly)                              | Calculated  | Derived          |
| `company_name`          | Company name listed in job posting                                        | Raw         | Scraped          |
| `job_skills`            | List of relevant skills extracted from job posting using PySpark          | Parsed List | NLP Extracted    |
| `job_type_skills`       | Dictionary mapping skill types (e.g., 'cloud', 'libraries') to skill sets | Parsed Dict | NLP Extracted    |

### Source and licence

The data is the [`lukebarousse/data_jobs`](https://huggingface.co/datasets/lukebarousse/data_jobs) dataset on Hugging Face, collected and processed by Luke Barousse. Its dataset card lists the licence as Apache-2.0. The course uses a Parquet copy in the [`bdi593/datasets` repository](https://github.com/bdi593/datasets/tree/main/data-jobs).

## 📚 Notebooks in This Case Study

| Notebook                                       | What it covers                                                                                                                                                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`eda.ipynb`](./eda.ipynb)                     | Exploratory data analysis. Loads the data, checks missing values, parses the messy columns, fixes the mislabeled "Sudan" country, saves a cleaned Parquet file, and explores titles, locations, platforms, salaries, skills, and remote work. |
| [`hr-analytics.ipynb`](./hr-analytics.ipynb)   | Applied HR analytics on the cleaned data: **competitive compensation benchmarking**, **talent scouting / market mapping**, and **skill demand and retention signals**.                                                          |

:::{tip} Working with the same dataset twice
A common pattern in industry is to do EDA _once_ on a dataset and then reuse the cleaned version across multiple downstream analyses. We follow that pattern here: the EDA notebook persists a cleaned Parquet file, and the HR analytics notebook loads it without repeating the preprocessing. If you open the HR analytics notebook first, it rebuilds the columns it needs from the raw data.
:::

## 🧰 Setup

Install the course environment from the repository root:

```bash
python -m pip install -r requirements.txt
```

No manual download is needed. `eda.ipynb` reads the raw data over the internet from the course datasets repository and writes `data_jobs_preprocessed.parquet` next to the notebook. `hr-analytics.ipynb` loads that file, or downloads the raw data and rebuilds the columns it needs if the file is missing. The cleaned file is listed in the repository's `.gitignore`, so it is not committed.
