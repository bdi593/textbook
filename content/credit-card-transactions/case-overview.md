# Analyzing Credit Card Transactions

Credit card transactions are one of the most valuable (and most sensitive) data assets a financial institution owns. They power fraud detection, customer segmentation, lifetime-value modeling, merchant analytics, and personalised offers. Yet _publicly available_ card data is scarce: real transactions cannot be released for privacy reasons, and the synthetic datasets that exist are usually small, heavily anonymised, or both.

For example, the well-known [Kaggle Credit Card Fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) contains only 284,807 transactions over two days, of which fewer than 500 are fraudulent. Worse, all but two of its columns are the result of a principal-components transformation, which obfuscates the underlying business meaning.

This case study uses a much larger, more realistic synthetic dataset published by IBM. It contains over **24 million transactions** generated from a multi-agent simulation of consumer behaviour, with no obfuscation of the columns.

![Pay with Credit Card](images/undraw_pay-with-credit-card_77g6.svg)

## Learning objectives

By the end of this chapter you should be able to:

1. Explain why banks and analytics teams treat card transaction data as a strategic asset, for example for fraud screening and merchant analysis.
2. Load a multi-gigabyte CSV / Parquet file efficiently using **Polars** and **DuckDB**.
3. Clean common dirty-data patterns (currency strings, split date columns) and investigate missing values such as missing zip codes before deciding how to handle them.
4. Engineer features such as rolling spend, time since last transaction, and boolean flags.
5. Use SQL window functions and Polars expressions interchangeably, with a deterministic sort order so both give the same answer.
6. Evaluate a simple rule-based fraud flag against the `Is Fraud?` label using precision and recall.

## About the dataset

The data is provided as a single CSV whose column names are in the header row. The DuckDB notebook uses a Parquet copy of the cleaned data. It covers:

- **2,000 synthetic consumers** based in the United States who travel internationally.
- **Decades of purchases** (1991 to February 2020), including multiple cards per customer.
- A mix of **chip, swipe, and online** transactions.
- A small, realistic fraction of **fraudulent transactions** labeled with `Is Fraud?`.

```{list-table} Notable columns
:header-rows: 1

* - Column
  - Description
  - Notes
* - `User`
  - Synthetic customer id
  - Use to partition rolling/window features.
* - `Card`
  - Card index for that user
  - A user may hold multiple cards.
* - `Year`, `Month`, `Day`, `Time`
  - Transaction timestamp split across columns
  - Combine into a single `Datetime` column. `Time` has hours and minutes only, so two transactions in the same minute share a timestamp.
* - `Amount`
  - Transaction amount as a string (e.g. `"$54.32"`)
  - Strip the `$` and cast to `float64`. Negative values are refunds.
* - `Use Chip`
  - `Chip Transaction`, `Swipe Transaction`, `Online Transaction`
  - Useful for fraud heuristics.
* - `Merchant Name`, `Merchant City`, `Merchant State`, `Zip`, `MCC`
  - Merchant attributes
  - `Merchant Name` is an anonymised integer id. `MCC` (Merchant Category Code) is a standard 4-digit retail category. `Merchant State` and `Zip` are empty for online merchants. `Zip` is also empty for merchants outside the U.S., where `Merchant State` holds the country.
* - `Errors?`
  - Error recorded for the transaction, such as `Insufficient Balance` or `Bad PIN`
  - Empty for about 98% of transactions.
* - `Is Fraud?`
  - `"Yes"` / `"No"` label
  - Highly imbalanced: about 0.12% of transactions are fraud.
```

### Source and licence

The data is the IBM synthetic credit card transactions dataset, published on Kaggle as [Credit Card Transactions](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions). The method that generated it is described in [Synthesizing Credit Card Transactions (Altman, 2019)](https://arxiv.org/abs/1910.03033). A Parquet copy of the cleaned data is in the [`bdi593/datasets` repository](https://github.com/bdi593/datasets/tree/main/credit-card-transactions-ibm). Check the source page for terms of use.

:::{important} Why we use Polars _and_ DuckDB
The chapter teaches both libraries because they complement each other:

- **Polars** is a Rust-based DataFrame library with a fluent expression API. It excels at transformations and pipeline-style code, and is the natural successor to pandas for medium-to-large data.
- **DuckDB** is an in-process analytical SQL engine. It is the right choice when your team thinks in SQL, when you want to read Parquet directly, or when you need window functions over hundreds of millions of rows on a laptop.

Most analytics teams end up using both. Knowing the same operation in each language makes it much easier to choose the right tool for the next problem.
:::

## Notebooks in this case study

```{list-table}
:header-rows: 1

* - Notebook
  - What it covers
* - **Introduction to Polars**
  - The Polars DataFrame API: expressions, filtering, `group_by`, joins, and lazy evaluation, on a small example.
* - **Analyze Credit Card Transactions with Polars**
  - Reads the 2.3 GB CSV, checks missing values, cleans `Amount` and the date columns, writes Parquet, builds flags, aggregates, and window features, and tests a fraud rule against the label.
* - **Introduction to DuckDB**
  - What DuckDB is, SQL over pandas DataFrames, `GROUP BY` and window functions, and querying a remote Parquet file.
* - **Analyze Credit Card Transactions with DuckDB**
  - Repeats the analysis in SQL on the Parquet file and checks that DuckDB and Polars flag exactly the same transactions.
```

:::{tip} Recommended order
If you are new to both libraries, work through the **Polars** track first (it is closer to pandas and easier to debug), then redo the analysis in **DuckDB** to see the same operations expressed in SQL.
:::

## Tasks (the analytical workflow)

The notebooks build up the following workflow step by step:

1. Read the CSV (or Parquet) file and inspect the schema and dtypes.
2. Check which columns have missing values and why.
3. Parse `"Amount"` from a `$`-prefixed string into `float64`.
4. Combine the `Year`, `Month`, `Day`, and `Time` columns into a single `Datetime`.
5. Look at the distributions of categorical columns such as `"Use Chip"` and `"Is Fraud?"`.
6. Create boolean flag columns such as refunds, large transactions, and online transactions.
7. Filter for online refunds (online transactions whose amount is negative).
8. Aggregate per user: total spend, average ticket size, and number of transactions.
9. Use a rolling/window feature (per user) to mimic SQL's `OVER (PARTITION BY user ORDER BY datetime)` behaviour and capture spending trends.
10. Flag _online + above the user's average so far + same minute as the previous transaction_, and measure the rule's precision and recall against `Is Fraud?`.
11. Compare the same operation expressed in Polars and in DuckDB SQL.

:::{caution} Real-world fraud detection is more than feature engineering
The features built in this chapter are useful inputs to a fraud model, but a production fraud system also requires:

- Sub-second scoring latency
- Continuous re-training on labeled feedback
- Calibrated probabilities so a risk team can set policy thresholds
- Rigorous monitoring for **concept drift** (fraudster behaviour changes constantly)

Treat the work in this chapter as the **data layer** that any of those systems would sit on top of.
:::

## Setup

Install the course environment from the repository root:

```bash
python -m pip install -r requirements.txt
```

The two analysis notebooks need local data files:

- **Polars notebook:** download `credit_card_transactions-ibm_v2.csv` (about 2.3 GB) from the [Kaggle page](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions) and place it in the same folder as the notebook.
- **DuckDB notebook:** it reads `credit_card_transactions-ibm_v2.parquet` (about 250 MB) from the same folder. The Polars notebook writes this file, or you can download it from the [course datasets repository](https://media.githubusercontent.com/media/bdi593/datasets/main/credit-card-transactions-ibm/credit_card_transactions-ibm_v2.parquet).

Both data files are listed in the repository's `.gitignore`, so they are not committed. The full table takes several GB of memory in Polars, so close other memory-heavy programs first. The remote-file example in the DuckDB introduction needs internet access.

:::{seealso} Further reading

- IBM Research: [Synthesizing Credit Card Transactions](https://arxiv.org/abs/1910.03033)
- Polars: [User Guide](https://docs.pola.rs/)
- DuckDB: [Documentation](https://duckdb.org/docs/)
- Visa Risk: [Public materials on real-time fraud scoring](https://usa.visa.com/about-visa/visa-fraud-detection.html)

:::
