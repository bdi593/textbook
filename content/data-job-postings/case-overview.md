# Case Overview

In this case, we will use a real-world job postings dataset focused on data science and analytics roles, collected from internet search results and job boards since 2023 by Luke Barousse.

```{image} images/undraw_searching-everywhere_tffi.svg
:alt: Searching Everwhere - Undraw
:width: 360px
:align: center
```

&nbsp;

## 💼 Business Context

The market for data and analytics talent has matured rapidly over the last few years. Roles that barely existed a decade ago — *data engineer*, *machine learning engineer*, *analytics engineer* — now appear in tens of thousands of postings each month. For job seekers, recruiters, hiring managers, and educators, this creates several questions:

- **Job seekers** want to know which titles are growing, which skills get the strongest premium, and how compensation differs by location and industry.
- **Recruiters and hiring managers** need to benchmark salary ranges, identify in-demand skills, and decide where to focus sourcing efforts.
- **Educators and bootcamps** use the data to keep curricula aligned with the skills employers actually request.
- **Workforce researchers** track how remote work, the rise of generative AI, and macroeconomic conditions reshape the labor market.

Real online postings give us a window into all of these questions. Each row tells us *what* a company is hiring for, *where*, *under what conditions*, and increasingly — *for how much*.

## 🎯 Learning Objectives

By the end of this case study you should be able to:

1. Load and inspect a moderately large (~786,000 row) Parquet file with [Polars](https://pola.rs/).
2. Diagnose missing values and decide which columns are usable.
3. Parse "messy" string columns that look like Python lists or dictionaries into proper structured types (`List`, `Struct`).
4. Run common exploratory analyses — value counts, group-by aggregations, time-series counts, and skill frequencies — at scale.
5. Translate exploratory findings into the kinds of questions a real HR analytics team would ask.

We have already covered common preprocessing steps for tabular data in the previous chapters, but this dataset also includes list-like or dictionary-like string columns that require additional parsing and transformation.

For example, the `job_skills` column contains a string representation of a list of skills extracted from the job posting using NLP techniques.

Additionally, the `job_type_skills` contain a Python dictionary-like string that map skill types (e.g., 'cloud', 'libraries') to sets of skills.

We will need to parse these string representations into actual Python data structures (lists and dictionaries) to work with them effectively in our analysis.

## 📚 Notebooks in This Case Study

This chapter is split across two complementary notebooks:

1. **[`eda.ipynb`](./eda.ipynb)** — exploratory data analysis. We load the data, parse the messy columns, and answer descriptive questions about job titles, locations, posting platforms, salaries, skills, and remote work.
2. **[`hr-analytics.ipynb`](./hr-analytics.ipynb)** — applied HR analytics. We reuse the cleaned dataset to walk through three workflows that real talent and people-analytics teams run: **competitive compensation benchmarking**, **talent scouting / market mapping**, and **skill-gap and retention signals**.

:::{tip} Working with the same dataset twice
A common pattern in industry is to do EDA *once* on a dataset and then reuse the cleaned version across multiple downstream analyses. We follow that pattern here: the EDA notebook persists a cleaned Parquet file, and the HR analytics notebook loads it without repeating the preprocessing.
:::

## 📌 Dataset Information

- **Source:** [`lukebarousse/data_jobs`](https://huggingface.co/datasets/lukebarousse/data_jobs)
- **Licensing:** Apache-2.0
- **Format:** Parquet (original CSV file converted to Parquet for compression - no other preprocessing applied)
- **Size:** ~30 MB (~786,000 rows)
  - The original CSV file is much larger (~230 MB) due to the large number of rows and text fields, but the Parquet format significantly reduces the file size while preserving all data.

## 📘 Data Dictionary

| Column Name             | Description                                                               | Type        | Source           |
| ----------------------- | ------------------------------------------------------------------------- | ----------- | ---------------- |
| `job_title_short`       | Cleaned/standardized job title using BERT model (10-class classification) | Calculated  | From `job_title` |
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
