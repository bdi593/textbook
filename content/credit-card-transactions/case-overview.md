# Analyzing Credit Card Transactions Overview

Limited credit card transaction data is available for training fraud detection models and other uses, such as analyzing similar purchase patterns. Credit card data that is available often has significant obfuscation, relatively few transactions, and short time duration. For example, this Kaggle dataset has 284,000 transactions over two days, of which less than 500 are fraudulent. In addition, all but two columns have had a principal components transformation, which obfuscates true values and makes the column values uncorrelated.

- **Dataset**: [Kaggle Datasets - Credit Card Transactions](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions)
- **Data Generation Detail**: [Synthesizing Credit Card Transactions](https://arxiv.org/abs/1910.03033)

## Dataset[^1]

The data here has almost no obfuscation and is provided in a CSV file whose schema is described in the first row. This data has more than 20 million transactions generated from a multi-agent virtual world simulation performed by IBM. The data covers 2000 (synthetic) consumers resident in the United States, but who travel the world. The data also covers decades of purchases, and includes multiple cards from many of the consumers.

[^1]: [Kaggle Credit Card Transactions Dataset](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions/)

## Tasks

- Read the CSV file into a Polars DataFrame.
- Print the data types of each column (i.e., schema).
- Parse the `"Amount"` column as a `float64` type.
- Create a `"timestamp"` column by combining the date component columns.
- Look at the distributions of categorical columns such as `"Use Chip"` and `"Is Fraud?"`.
- Create boolean flag columns to mark suspicious transactions.
- Filter online transactions where the amount is negative (i.e., refunds).
- Find the total transaction amount, average amount, and the number of transactions by each user.
- Use a rolling/window feature to mimic SQL's functionality.
