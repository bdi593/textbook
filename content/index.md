# BDI 199/593 - Advanced Analytics Applications in Business

- University of Illinois Urbana-Champaign
- **Instructor**: Ye Joo Park ([ypark32@illinois.edu](mailto:ypark32@illinois.edu))

This course is designed to build upon the data analytics foundations from BDI 475: Introduction to Data Analytics Applications in Business. The goal is to equip you with advanced skills in business analytics, focusing on solving real-world challenges in business analytics:

1. handling large-scale data,
2. performing sophisticated analyses using techniques used in the industry
3. creating impactful visualizations.

```{image} ../site_images/favicon.svg
:alt: BDI 199/593 Circle
:width: 320px
:align: center
```

&nbsp;

## Overview

The course is structured to provide a hands-on approach to advanced business analytics. You will work with real-world datasets, tackle complex business problems, and develop solutions using state-of-the-art tools and methodologies (e.g., pre-trained machine learning models). The course materials are divided into several key areas:

1. Loading and Cleaning Data with Python
2. Large-Scale Data Processing
3. Real-world Prediction and Classification
4. Data Retrieval and Real-time Analysis using SQL
5. Natural Language Processing and Text Analytics
6. Interactive Data Visualization
7. Cloud Computing for Business Analytics
8. Applied Machine Learning Projects

Throughout the course, you will engage in lots of exercises, case studies, and a final project that simulates real-world business analytics challenges.

## Learning Objectives

By the end of this course, you will be able to:

- define key terms and concepts related to large-scale business analytics using tools such as Python and pandas
- explain how Polars and DuckDB enhance data processing performance compared to traditional pandas workflows
- apply SQL queries in PostgreSQL to extract, filter, and join data from relational databases
- analyze business scenarios by performing complex data manipulations and statistical modeling in Python using pandas and industry techniques
- evaluate the clarity and impact of visualizations created with Plotly and Tableau Desktop for communicating business insights
- design and present an interactive dashboard in Plotly Dash or Tableau Desktop that integrates findings from multiple analytical techniques to support a business decision

## Course Topics

1. Load and Clean Data

- Utilize Pandas for efficient data manipulation and analysis
- Read different types of data (CSV, Excel, JSON, Parquet)

2. Handle Large-Scale Datasets

- Perform out-of-memory operations using Polars
- Execute ETL processes on datasets larger than 10 GB
- Apply various sampling techniques (random, stratified) for large datasets

3. Retrieve and Manage Data

- Interact with APIs to collect data programmatically
- Use PostgreSQL for advanced data retrieval and analysis
  o Utilize advanced JOIN techniques and subqueries effectively
  o Employ VIEWs and built-in functions for sophisticated data analysis
  o Use window functions for complex querying scenarios
- Generate insightful reports on sales trends, customer preferences, and operational performance

4. Apply Natural Language Processing Techniques

- Understand NLP preprocessing pipeline
- Implement BERT-based models for textual analysis and sentiment analysis
- Perform topic modeling using BERTopic

5. Create Interactive Data Visualizations

- Develop client-ready charts using Plotly's low-level API
- Design and publish interactive dashboards with Dash
- Apply data visualization best practices for effective communication

6. Leverage Cloud Computing for Analytics

- Utilize cloud resources for efficient data analysis and summarization
- Develop serverless functions for automated report generation

7. Tackle Real-World Machine Learning Projects

- Participate in past Kaggle challenges to gain practical ML project experience
- Utilize advanced tools for real-world data analytics such as DeepNote

8. Communicate Analytical Insights

- Present data-driven insights to stakeholders effectively
- Create compelling narratives around analytical findings

## Prerequisites

## Dataset Candidates

| **Dataset**                                 | **Source**                                                                                                                   | **Notes**                                                   |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Credit Card Transactions                    | [Link](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions/data)                                            | synthetic, no obfuscation                                   |
| Airbnb Listings, Calendar, and Reviews Data | [Link](https://insideairbnb.com/get-the-data/)                                                                               | real data, well-maintained                                  |
| Chicago Ridesharing Trips 2018-2022         | [Link](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips-2018-2022-/m6dm-c72p/about_data) | Public dataset, reported to the City of Chicago             |
| Sentiment Analysis for Mental Health        | [Link](https://www.kaggle.com/datasets/suchintikasarkar/sentiment-analysis-for-mental-health)                                | NLP-focused dataset                                         |
| Electric Vehicle Population Data            | [Link](https://data.wa.gov/Transportation/Electric-Vehicle-Population-Data/f6w7-q2d2/about_data)                             | Public dataset provided by the Washington State Data Portal |
| Sleeping Alone Data                         | [Link](https://github.com/fivethirtyeight/data/blob/master/sleeping-alone-data/sleeping-alone-data.csv)                      | Survey data                                                 |
