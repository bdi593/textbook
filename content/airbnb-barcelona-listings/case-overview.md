# Cleaning Airbnb Listings in Barcelona

In this case study, we walk through the process of cleaning a real-world Airbnb dataset for listings in Barcelona, Spain. The raw data comes from [Inside Airbnb](https://insideairbnb.com/), a source that provides detailed listing information scraped from Airbnb's public website.

```{figure} images/kaspars-upmanis-nD2WzCZrlLE-unsplash.jpg
:label: Barcelona
:alt: Barcelona
:align: center

Barcelona, Spain - Photo by [Kaspars Upmanis on Unsplash](https://unsplash.com/photos/brown-buildings-lot-nD2WzCZrlLE)
```

## 🏙️ Business Context

Short-term rentals are a policy and business issue in many cities, including Barcelona. Researchers, journalists, policymakers, and community groups use Inside Airbnb data to ask questions such as: what does a typical listing cost per night, how does that vary by neighbourhood and room type, and how many listings are entire homes rather than rooms?

Suppose you are an analyst preparing data for a colleague who will study nightly prices across Barcelona's neighbourhoods. Your job is to deliver a **clean, documented table** that they can trust. Raw listing data often contains:

- Missing values
- Inconsistent data types
- Redundant or irrelevant columns

Every cleaning decision changes the answer to the price question. Dropping all listings without reviews, for example, removes every new listing. So the deliverable is not only the clean table but also a record of what was removed and why.

## 🎯 Learning Objectives

By the end of this case study you should be able to:

1. Load a compressed CSV file with pandas and confirm which data snapshot it comes from.
2. Profile missing values and select the columns relevant to a business question.
3. Convert messy text columns into numbers (bathrooms, price) and flags (superhost) without hiding missing values.
4. Decide, column by column, whether to drop rows, fill in values, or keep values missing, and measure how many rows each choice removes.
5. Validate a cleaned dataset with explicit rules and a look at the extreme values.

## 📊 Dataset

The notebook uses Inside Airbnb's detailed listings file (`listings.csv.gz`) for Barcelona from the **snapshot dated 17 September 2026**: 15,236 listings and 90 columns. A copy is saved in this case study's `data/` folder, because Inside Airbnb keeps only about the last 12 months of snapshots online.

The cleaned output, `cleaned-output.csv`, has one row per listing and these columns:

| Column              | Description                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| `name`              | Name of the listing                                                                               |
| `neighbourhood`     | Neighbourhood, geocoded by Inside Airbnb from the listing's coordinates (`neighbourhood_cleansed`) |
| `room_type`         | `Entire home/apt`, `Private room`, `Shared room`, or `Hotel room`                                 |
| `bedrooms`          | Number of bedrooms                                                                                |
| `accommodates`      | Maximum number of guests. The value stops at 16.                                                  |
| `minimum_nights`    | Minimum stay in nights. Missing for listings whose booking rules were not captured.               |
| `price`             | Daily price in local currency (euros). The `$` sign in the raw file is an export artifact.        |
| `availability_365`  | Number of open dates in the next 365 days. A date can be closed because it is booked or blocked.  |
| `number_of_reviews` | Number of reviews the listing has                                                                 |
| `review_score`      | Overall review score from 0 to 5 (`review_scores_rating`). Missing for listings with no reviews.  |
| `latitude`, `longitude` | Location of the listing (WGS84)                                                               |
| `is_superhost`      | 1 if the host is a superhost, 0 if not                                                            |
| `bathrooms`         | Number of bathrooms, parsed from `bathrooms_text` (a half-bath counts as 0.5)                     |

### Source and licence

Data: [Inside Airbnb](https://insideairbnb.com/get-the-data/), Barcelona, snapshot of 17 September 2026. Inside Airbnb's Get the Data page states that its datasets "are available to download and use under the Creative Commons Attribution 4.0 International (CC BY 4.0) licence". Its [Data Policies](https://insideairbnb.com/data-policies/) page explains how to credit the data and asks users to download it once rather than every time an analysis runs. The same page asks users not to republish the data, so the raw snapshot is not stored in this repository: the notebook downloads it the first time you run it.

## 📚 Notebooks in This Case Study

| Notebook                                                     | What it covers                                                                                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`clean-airbnb-listings.ipynb`](./clean-airbnb-listings.ipynb) | Loads the Barcelona listings, selects 14 columns, converts bathrooms, price, and the superhost flag, handles missing values, validates the result, and saves `cleaned-output.csv`. |

## 🗂️ Key Steps in the Cleaning Workflow

1.  **Import Libraries**
    Use _pandas_ and _NumPy_ for data handling and transformation.

2.  **Load the Dataset**
    The dataset is compressed (gzip) and contains information on about 15,000 Airbnb listings in Barcelona.

3.  **Inspect the Data**
    The dataset includes 90 columns with various data types and missing values.

4.  **Select Relevant Features**
    Only a subset of columns important for analysis (e.g., price, room type, number of reviews, location) is retained.

5.  **Convert Data Types**
    The number of bathrooms is extracted from text such as `"1.5 shared baths"`. _Price_ is stored as a string and is converted to a number after removing the `$` sign and commas. The _superhost_ indicator is converted from `"t"`/`"f"` to 1/0, keeping missing values missing.

6.  **Handle Missing Values**
    Listings without a price, bedrooms, or bathrooms are dropped (about 17% of listings). Listings without reviews are kept, with a missing review score, so that new listings are not lost.

7.  **Validate**
    Explicit rules check prices, review scores, minimum stays, and coordinates. The most expensive listings are inspected by hand: they all have no reviews, and some prices look like placeholders.

8.  **Save the Clean Data**
    The cleaned dataset has 14 columns and about 12,600 listings. It is saved as `cleaned-output.csv` for downstream analysis or modeling.

## 🧰 Setup

Install the course environment from the repository root:

```bash
python -m pip install -r requirements.txt
```

The notebook reads `data/listings.csv.gz` from this folder. If the file is missing, the notebook downloads the 17 September 2026 snapshot from Inside Airbnb once and saves it there, which needs internet access and works only while that snapshot is still online.
