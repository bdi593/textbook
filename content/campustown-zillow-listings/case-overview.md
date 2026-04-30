# 🏡 Campustown Zillow Listings - Final Case Study

This is the final case study for BDI 199/593. It pulls together every major
skill we have practiced this term - exploratory data analysis, business
visualization, predictive modeling, model evaluation, NLP feature engineering,
and time-aware analysis - on a single, realistic dataset of single-family home
listings from sixteen U.S. campus towns.

The case is delivered in three parts that build on one another.

- Parts 1 & 2 are required for all students (3-credit and 4-credit).
- Part 3 is required only for 4-credit (BDI 593) students, who extend
  the analysis with the property-level price-history event log.

```{image} https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=1200&q=80
:alt: Suburban single-family home
:width: 540px
:align: center
```

## 🏘️ Why campus towns?

College towns are an unusual real-estate asset class. They have:

- Anchored demand. A large public university typically employs thousands of
  faculty and staff and enrolls tens of thousands of students whose families,
  visiting scholars, and graduate students need housing year after year.
- Counter-cyclical stability. Enrollment tends to rise in recessions, which
  cushions rental demand exactly when other markets weaken.
- Geographically concentrated demand. A short list of neighborhoods near
  campus drives most of the rental and owner-occupied demand, which makes the
  market easier to model than a sprawling metro area.
- Modest absolute price points. Compared with coastal metros, single-family
  homes in campus towns are reachable for mid-sized investment funds and
  individual investors.

For these reasons, several real investment platforms - Roofstock, Invitation
Homes, AMH, Pretium, and many private syndicates - explicitly target
"university-anchored" markets. Our dataset gives us a window into sixteen of
them, anchored by nine major universities.

### 🎓 City to university mapping

Every city in the dataset is mapped to its anchoring public university. Part 1
adds a `campus` column based on this mapping so satellite towns are pooled
with their parent city when we aggregate or model.

| City            | State | Anchoring university                                        |
| --------------- | ----- | ----------------------------------------------------------- |
| Madison         | WI    | University of Wisconsin-Madison                             |
| Middleton       | WI    | University of Wisconsin-Madison (suburb)                    |
| Ann Arbor       | MI    | University of Michigan                                      |
| Athens          | GA    | University of Georgia                                       |
| State College   | PA    | Pennsylvania State University                               |
| Charlottesville | VA    | University of Virginia                                      |
| Gainesville     | FL    | University of Florida                                       |
| Chapel Hill     | NC    | University of North Carolina at Chapel Hill                 |
| Carrboro        | NC    | University of North Carolina at Chapel Hill (adjacent town) |
| Davis           | CA    | University of California, Davis                             |
| Iowa City       | IA    | University of Iowa                                          |
| Champaign       | IL    | University of Illinois Urbana-Champaign                     |
| Savoy           | IL    | University of Illinois Urbana-Champaign (suburb)            |
| Urbana          | IL    | University of Illinois Urbana-Champaign (campus spans both) |
| Lafayette       | IN    | Purdue University (across the river)                        |
| West Lafayette  | IN    | Purdue University (main campus)                             |

## 🎬 Hypothetical Scenario

You have just been hired as a Real Estate Analyst at Quad Capital
Partners (QCP), a mid-sized private investment firm that buys, renovates, and
rents single-family homes in university-anchored markets across the United
States. QCP currently operates in sixteen campus towns and is planning a
$25 million capital deployment over the next eighteen months.

The Head of Acquisitions has handed you a Zillow data extract covering every
single-family listing the firm's data vendor could find in those sixteen
markets. Your charter is broad and explicitly analytical:

> "Help us understand these markets, build a tool that estimates a fair price
> for any single-family home in our footprint, and tell us where the best
> opportunities are. We want one notebook we can re-run when new data arrives,
> and a slide deck we can show the Investment Committee."

You will play this role for the entire case study. Every chart, model, and
recommendation should be framed for an investment-committee audience - not for
a data-science conference.

:::{tip} Pick another role if it fits you better
The deliverable is the same regardless of role, but you are welcome to
re-frame the narrative. Two equally good alternatives are:

- Business Developer at a relocation-services firm advising employers
  whose new hires need to buy in a campus town.
- Strategy Analyst at a regional bank deciding which campus-town markets
  the bank should grow its mortgage book in.

Pick whichever role you can talk about most credibly.
:::

## 📦 The Dataset

The data lives in two Parquet files inside this case-study folder:

```
content/campustown-zillow-listings/data/
├── campustown_properties.parquet   (~36,000 rows, one row per listing)
└── price_history.parquet           (~292,000 rows, one row per market event)
```

The properties file covers sixteen campus towns across eleven states, including
Champaign-Urbana (IL), Madison (WI), Gainesville (FL), Ann Arbor (MI), Athens
(GA), Charlottesville (VA), Chapel Hill (NC), Iowa City (IA), Lafayette and
West Lafayette (IN), State College (PA), Davis (CA), and a few smaller
satellite towns.

### Data dictionary - `campustown_properties.parquet`

| Column                         | Type   | Description                                                                                                                                                          |
| ------------------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `property_id`                  | int    | Stable Zillow identifier for the property (joins to price history).                                                                                                  |
| `date_posted`                  | string | Date the listing was most recently posted on Zillow (ISO `YYYY-MM-DD`).                                                                                              |
| `days_on_zillow`               | float  | Days between the most recent posting and the date the data was scraped. Not a reliable liquidity signal (see Part 1); Part 3 derives a cleaner days-to-sale measure. |
| `price`                        | int    | Current list price in USD (or last list price for inactive listings).                                                                                                |
| `last_sold_price`              | int    | Price of the most recent recorded sale, in USD.                                                                                                                      |
| `description`                  | string | Free-text marketing description written by the listing agent.                                                                                                        |
| `beds`                         | int    | Number of bedrooms.                                                                                                                                                  |
| `baths`                        | float  | Number of bathrooms (half-baths counted as `0.5`).                                                                                                                   |
| `year_built`                   | float  | Year the structure was built.                                                                                                                                        |
| `latitude` / `longitude`       | float  | Property coordinates (WGS-84).                                                                                                                                       |
| `lot_size`                     | float  | Lot size in square feet.                                                                                                                                             |
| `living_area`                  | float  | Above-ground living area in square feet.                                                                                                                             |
| `address_street`               | string | Street address.                                                                                                                                                      |
| `address_city`                 | string | City.                                                                                                                                                                |
| `address_state`                | string | Two-letter state abbreviation.                                                                                                                                       |
| `address_zipcode`              | int    | Five-digit ZIP code.                                                                                                                                                 |
| `address_county`               | string | County name (e.g., `Dane County`).                                                                                                                                   |
| `address_country`              | string | Always `USA` in this extract.                                                                                                                                        |
| `address_raw`                  | string | Raw address string before parsing.                                                                                                                                   |
| `county_fips`                  | float  | Five-digit FIPS code for joins to Census data.                                                                                                                       |
| `reso_is_new_construction`     | float  | `1.0` if newly built, else `0.0`.                                                                                                                                    |
| `reso_architectural_style`     | string | Style label (e.g., `Ranch`, `Traditional`, `Bungalow`).                                                                                                              |
| `reso_hoa_fee`                 | string | HOA fee as a raw string (e.g., `"$185 annually"`).                                                                                                                   |
| `reso_parking_capacity`        | int    | Parking spots (garage + driveway).                                                                                                                                   |
| `reso_elementary_school`       | float  | School-rating placeholder (mostly missing in this extract).                                                                                                          |
| `reso_middle_or_junior_school` | string | Assigned middle / junior high school name.                                                                                                                           |
| `reso_high_school`             | string | Assigned high school name.                                                                                                                                           |

### Data dictionary - `price_history.parquet`

| Column              | Type     | Description                                                                                                    |
| ------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| `property_id`       | int      | Joins to `campustown_properties.property_id`.                                                                  |
| `date`              | datetime | Date of the market event.                                                                                      |
| `event_type`        | string   | One of `listedForSale`, `priceChange`, `pendingSale`, `contingent`, `sold`, `listingRemoved`, `listedForRent`. |
| `price`             | float    | Reported price at the event, in USD.                                                                           |
| `price_change_rate` | float    | Fractional change from the previous price for the same property (e.g., `-0.05` = 5% price cut).                |

A single property can have multiple full list->sold cycles in this table -
some homes have changed hands two or three times in the last decade.

## 🎯 Learning Objectives

By the end of this case study you should be able to:

1. Load, profile, and clean a moderately large multi-source real-estate
   dataset spanning multiple regional markets.
2. Use Plotly Express to build clear, business-ready exploratory charts
   that compare markets and highlight pricing drivers.
3. Build, evaluate, and interpret a regression-based price-prediction model
   using `scikit-learn` and `xgboost`, including baseline error metrics
   (MAE, RMSE, R², MAPE) and residual analysis.
4. Use spaCy to tokenize a free-text listing description, extract
   amenity-style features with `PhraseMatcher`, combine them with structured
   tabular features, and measurably improve the price model.
5. (4-credit only) Reshape an event-log of price-change history into
   property-level features (list-to-sale ratio, days-to-sale, number of price
   cuts, market temperature) and use them to predict realized sale outcomes
   rather than list price.
6. Communicate analytical findings to a non-technical audience through a
   tightly edited slide deck that leads with business implications.

## 📚 Notebooks in This Case Study

This chapter contains four notebooks. Each notebook is clearly labeled with
the case-study part it belongs to.

| Notebook                              | Part   | Audience      | Focus                                                                                              |
| ------------------------------------- | ------ | ------------- | -------------------------------------------------------------------------------------------------- |
| `part-1-eda-and-visualizations.ipynb` | Part 1 | All students  | EDA, data quality, market comparisons, Plotly Express visualizations                               |
| `part-2a-price-predictor.ipynb`       | Part 2 | All students  | Baseline price-prediction model from structured features; metric-based evaluation                  |
| `part-2b-nlp-features.ipynb`          | Part 2 | All students  | spaCy NLP on the description column; engineered text features improve the model                    |
| `part-3-price-history.ipynb`          | Part 3 | 4-credit only | Reshape the price-history event log into market-dynamics features and model realized sale outcomes |

:::{tip} Each notebook builds on the previous one
Treat the four notebooks as a single analytical pipeline. The cleaned dataset
from Part 1, the modeling pipeline from Part 2a, and the description-derived
features from Part 2b are all reused in Part 3.
:::

## 🧰 Setup

The notebooks rely on a small, focused stack. Install once at the top of the
case study:

```bash
pip install pandas pyarrow numpy plotly scikit-learn xgboost spacy
python -m spacy download en_core_web_sm
```

Plotly Express is the default visualization library for this case study.
Always set the `simple_white` template once at the top of each notebook so the
visual style is consistent across the deliverable:

```python
import plotly.io as pio

pio.templates.default = "simple_white"
```

## 📑 Deliverables

You will hand in two artifacts for the final case study:

1. One Jupyter notebook that contains your end-to-end analysis. You may
   either turn in the four notebooks in this folder edited with your own work,
   or consolidate them into a single notebook - your choice. The notebook must
   run top-to-bottom on a fresh machine.
2. One slide deck (PowerPoint or PDF) summarizing your findings for
   the QCP Investment Committee. The deck must:
   - be fewer than 30 slides,
   - include several of your own Plotly visualizations (exported as static
     images is fine), and
   - lead with business implications, not with code.

:::{tip} You are encouraged to use AI tools
You may - and are encouraged to - use AI assistants (ChatGPT, Claude, Copilot,
Gemini, etc.) for both the analysis and the slide deck. Two ground rules:

1. You are responsible for every number, chart, and claim you submit. AI tools
   hallucinate; verify before you ship.
2. Disclose, in one sentence on your title slide or in the notebook header,
   which AI tools you used and roughly how. ("I used ChatGPT to draft the
   first cut of the deck and to debug a `ColumnTransformer` error.")
   :::

:::{caution} The deliverables count, not the scaffolding
The four notebooks in this folder are scaffolding to teach you the
workflow. They are intentionally a little under-built so that you can put
your own analytical fingerprints on the final notebook and slide deck.
:::

## 📝 Grading Rubric (100 points)

The same rubric applies to all students. 4-credit students are graded on
all six rows; 3-credit students are graded only on the first five rows
(re-scaled to 100 points by ignoring Part 3).

| Component                                        | Points | Criteria                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------ | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Part 1 - EDA & Visualization                     | 20     | Clean load of both Parquet files; documented data-quality issues; at least five Plotly Express charts comparing markets, price drivers, and time trends; each chart paired with a short business interpretation.                                                                                                       |
| Part 2a - Baseline Price Predictor               | 20     | Reproducible `scikit-learn` pipeline (preprocessing + XGBoost) trained on a held-out split; reports MAE, RMSE, R², and MAPE; residual analysis breaks errors down by market and price band; chosen model is justified in plain English.                                                                                |
| Part 2b - NLP Feature Engineering with spaCy     | 20     | Uses spaCy (`en_core_web_sm`) to tokenize and extract structured signals from `description`; engineered features (e.g., amenity flags, TF-IDF) are added to the Part 2a pipeline; the improved model is measurably better on the same held-out split, and the improvement is explained.                                |
| Communication & slide deck                       | 15     | Slide deck is < 30 slides, leads with business implications, uses your own visualizations, and is comprehensible to a non-technical audience. AI-tool usage is disclosed.                                                                                                                                              |
| Code quality, narrative, reproducibility         | 5      | Logical section headings, no dead code, no hard-coded paths outside the case folder, and a clear top-to-bottom run path.                                                                                                                                                                                               |
| Part 3 - Price-History Analytics (4-credit only) | 20     | Joins `price_history.parquet` to the properties file; engineers list-to-sale ratio, days-to-sale, and price-cut features per property; trains and evaluates a model that uses these history-derived features to predict a realized-sale outcome; interprets which dynamics matter most for QCP's acquisition strategy. |
| Total (4-credit)                                 | 100    |                                                                                                                                                                                                                                                                                                                        |
| Total (3-credit, rescaled)                       | 100    | (sum of first five rows scaled by `100 / 80`)                                                                                                                                                                                                                                                                          |

:::{seealso} Going further
Once the required pieces work, optional extensions that real QCP analysts
would actually do:

- Pull current 30-year mortgage rates and recompute affordability for each
  market.
- Layer Census ACS rent and household-income data on top of `county_fips`
  to estimate gross rental yield.
- Cluster listings (k-means on price-per-sqft, year-built, age) and label the
  resulting segments - "value plays," "trophy homes," "stale inventory," etc.
- Use an LLM to summarize the description column at scale and compare your
  spaCy-derived features against the LLM-derived ones.
  :::
