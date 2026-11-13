# Content review handoff: BDI 199/593 textbook

This document hands a content review of this repository to a coding agent. It lists what is wrong, where, how sure the reviewers are, and what a fix should look like. It was written on 2026-11-13 against commit `d3feeab` on `main`.

## 1. Scope

**In scope:** correctness, reproducibility, and consistency of the textbook in this repo (`content/`, `myst.yml`, `README.md`, `.github/workflows/deploy.yml`).

**Out of scope:** the student-facing GitHub Pages workflow. Students will publish their work from a separate student repository, so nothing here should add student publishing scaffolding, templates, or submission tooling to this repo.

**Not for the agent to decide:** section 6 lists choices that belong to the instructor (for example, whether to delete answer keys or re-sample a dataset). Do not act on those without an explicit instruction. Where a task below depends on one of them, it says so.

## 2. How to work in this repo

- Read `AGENTS.md` first. The stack is Jupyter Book v2 with MyST Markdown. The table of contents is explicit in `myst.yml`; a file that is not listed there is not built.
- Build check: `jupyter-book build --html` from the repo root. In a sandbox that blocks `github.com`, the theme download fails. `jupyter-book build --site` still parses all content and prints the content warnings before it reaches the theme step, so use that as a fallback.
- Plotly figures use the `"simple_white"` template. Horizontal bar charts set an explicit `height=`.
- Repo history includes a pass that removed em dashes from textbook prose (`a1e2f4d`). Do not introduce em dashes in content.
- **Cell references** in this document are zero-based indices into the notebook's `cells` array, as of commit `d3feeab`. Indices shift when cells are added or removed, so each task also quotes text you can search for.
- **Do not hand-edit notebook outputs.** If a fix changes code, re-run the notebook top to bottom so that execution counts are sequential and outputs match the code. If you cannot run a notebook (missing data, API key, or network), fix the source, clear the stale outputs for the cells you changed, and say so in your report.
- **Prose must follow output.** A large share of the findings are takeaways written before or without running the code. After any re-run, re-read every "Insight", "Takeaway", and summary cell in that notebook against the new output.

### Confidence labels

Each finding carries one of these:

- **[checked]**: confirmed by a script against the data or the stored output during the review.
- **[read]**: found by reading code, prose, and stored outputs. Not re-executed.
- **[unverified]**: a reasoned suspicion that the reviewers could not confirm. Verify before changing anything.

Severity: **H** = wrong result or broken page. **M** = misleading or incomplete. **L** = polish.

### Data each notebook needs

| Chapter | Notebook | Data source | Runs from a clean clone? |
| --- | --- | --- | --- |
| airbnb-barcelona-listings | clean-airbnb-listings | Inside Airbnb URL stamped `2025-09-14` | Only while that snapshot stays online |
| credit-card-transactions | analyze-...-with-polars | Local `credit_card_transactions-ibm_v2.csv` (gitignored, manual Kaggle download, about 2.3 GB) | No |
| credit-card-transactions | analyze-...-with-duckdb | Local `credit_card_transactions-ibm_v2.parquet` (gitignored; written by the Polars notebook, also linked from `bdi593/datasets`) | No |
| kickstarter-projects | preprocess-data | `bdi593/datasets` CSV over `http://` (20 MB) | Yes |
| kickstarter-projects | binary-classification | `bdi593/datasets` parquet | Yes |
| data-job-postings | eda, quiz-01 | `bdi593/datasets` parquet | Yes |
| data-job-postings | hr-analytics | Local `data_jobs_preprocessed.parquet` (gitignored; written by an "Optional" cell in `eda.ipynb`) | No |
| amazon-delivery | all three | `bdi593/datasets` CSV (two notebooks use `http://`) | Yes |
| australian-rental-market | both | `bdi593/datasets` CSV | Yes |
| conference-calls | both | Inline synthetic data | Yes |
| cu-zillow-listings | both | `bdi593/datasets` parquet (stored in Git LFS) | Yes, through the `github.com/.../raw/` URL |
| foundation-products | parse-json | `bdi593/datasets` JSON and CSV | Yes |
| foundation-products | competitive-analysis | Local `product-results/*.json` (committed) | Yes |
| instacart | all three | `subwaymatch/instacart-dataset-2017` mirror | Yes |
| walmart-sales-forecasting | both | `bdi593/datasets` CSV | Yes |
| financial-data-with-llms | read-edgar-filings | SEC EDGAR through `edgartools` (needs network and an identity string) | Needs network |
| financial-data-with-llms | analyze-filings-with-llm | `extracted/` (gitignored; written by the first notebook) and a paid LLM API key | No. Do not run without the instructor's key |
| campustown-zillow-listings | parts 1, 2a, 2b, 3 | Committed parquet files in `data/`; each part writes a file the next part reads | Yes |

During the review, `raw.githubusercontent.com` URLs were reachable from the sandbox and `github.com/.../raw/...` URLs were blocked by the sandbox proxy. That is a sandbox restriction, not evidence the files are missing.

## 3. Suggested order of work

1. **WP0: Environment.** Add one pinned environment file so re-runs are comparable (section 4.1).
2. **WP1: Mechanical hygiene.** Safe, small, no judgement needed (section 4.2).
3. **WP2: Notebook weight.** Four notebooks hold 130 MB (section 4.3).
4. **WP3: Chapter fixes.** Section 5, one chapter at a time, one pull request per chapter. Suggested chapter order by severity: kickstarter, amazon-delivery, australian-rental-market, walmart, campustown, instacart, credit-card, foundation-products, cu-zillow, data-job-postings, conference-calls, financial-data-with-llms, airbnb, then `index.md` and `README.md` last so they describe the corrected book.

## 4. Repo-level tasks

### 4.1 WP0: Environment

- **ENV-1 (H) [checked].** There is no `requirements.txt`, `pyproject.toml`, or `environment.yml`, and `uv.lock` is listed in `.gitignore`. Stored outputs were produced with mixed versions: pandas 2.3.3 and 3.0.0, xgboost 3.1.3 and 3.2.0, Python 3.8.10, 3.13.9, and 3.13.12. Install commands are scattered over 10 notebooks and 4 markdown pages.
  - Fix: add one environment file at the repo root that covers every chapter (pandas, polars, duckdb, pyarrow, numpy, plotly, plotnine, scikit-learn, xgboost, spacy plus `en_core_web_sm`, mlxtend, edgartools, openai, transformers and datasets if `case-studies/` is kept). Pin versions. Stop ignoring the lock file if one is used.
  - Then replace per-notebook install cells with a one-line pointer to the shared setup, or keep them and make them agree with the pinned file.
  - Note: at least one notebook relies on behaviour that changed between versions. `australian-rental-market/improve-the-model.ipynb` cell 17 casts categoricals separately on train and test, which a reviewer believes is only safe on recent xgboost [unverified].

### 4.2 WP1: Mechanical hygiene

- **HYG-1 (M) [checked].** `cleaned-output.csv` at the repo root is byte-identical to `content/airbnb-barcelona-listings/cleaned-output.csv`. Delete the root copy. Consider gitignoring notebook output files.
- **HYG-2 (M) [checked].** `content/airbnb-barcelona-listings/barcelona-listings.csv` (3.4 MB) is referenced by nothing. It is the 18-column summary file, not the 79-column file the notebook downloads. Delete it unless ABNB-1 below ends up using it.
- **HYG-3 (M) [checked].** Stored outputs contain the instructor's local paths. Search the notebooks for `C:\\Users\\ypark32` and `c:\\Users\\Park`. Known locations: `kickstarter-projects/binary-classification.ipynb`, `amazon-delivery/eda.ipynb`, `case-studies/customer-analytics.ipynb`, `financial-data-with-llms/read-edgar-filings.ipynb` (cell 5). These come from warnings and tracebacks, so fixing the underlying warning and re-running removes them.
- **HYG-4 (M) [checked].** The content build reports 26 "Duplicate identifier" warnings between `analyze-credit-card-transactions-with-polars.ipynb` and `analyze-credit-card-transactions-with-duckdb.ipynb`. Cells were copied with their cell IDs. Regenerate the IDs in one of the two notebooks.
- **HYG-5 (M) [checked].** `content/instacart/blog-post.md` lines 24, 30, 38, 63, 71 hot-link images from `github.com/user-attachments/assets/...` with no file extension, and the build flags all five. Download them into `content/instacart/images/` and reference local paths. Whether they currently render on the live site is [unverified].
- **HYG-6 (M) [checked].** `.github/workflows/deploy.yml` uses `node-version: 18.x` (end of life), `actions/configure-pages@v3`, and an unpinned `npm install -g jupyter-book`. It runs only on pushes to `main`. Update the versions, pin `jupyter-book`, and add a build job for pull requests.
- **HYG-7 (L) [checked].** Data URLs for `bdi593/datasets` use three styles and mix `http://` with `https://`. `http://` occurrences: `amazon-delivery/eda.ipynb` cell 7, `amazon-delivery/build-a-classifier.ipynb` cell 8, `kickstarter-projects/preprocess-data.ipynb` cell 7. Use `https://` throughout.
- **HYG-8 (L) [checked].** `.gitignore` is a Node template with a few Python lines appended. Add standard Python and Jupyter entries (`.ipynb_checkpoints/`, `*.pyc`, virtual environments). `content/financial-data-with-llms/.gitignore` ignores `openai_config.json` only inside that folder; add the pattern at the root too.
- **HYG-9 (M) [checked].** `README.md` omits two chapters from its case-study table and tree: Financial Data Analysis with LLMs and Campustown Zillow Listings. Its "Course Topics" and "Learning Objectives" repeat the claims in `index.md` that IDX-1 below flags. Update after IDX-1 is settled.

### 4.3 WP2: Notebook weight

- **WT-1 (H) [checked].** Four notebooks hold 130 MB of the repo's 201 MB, and the built site carries 271 MB of assets:

  | Notebook | Size | Cause |
  | --- | --- | --- |
  | `instacart/eda.ipynb` | 45.8 MB | Cell 30: `px.histogram(orders["days_since_prior_order"].dropna(), ...)` embeds 3.2M raw values (34.3 MB). Cells 27 and 33 add 4.6 MB each, cell 35 adds 1.9 MB. |
  | `instacart/analysis.ipynb` | 34.7 MB | Cell 38: the same histogram (34.3 MB). |
  | `amazon-delivery/eda.ipynb` | 29.8 MB | 33 Plotly outputs. Cells 28 and 36 draw 15 histograms and 15 box plots over all 45k rows (7.1 MB and 14.5 MB). |
  | `walmart-sales-forecasting/eda.ipynb` | 21.0 MB | Cell 32 `px.box` over 421,570 rows (7.4 MB); cells 24 and 26 histograms (4.5 MB each). |

  - Fix: Plotly histograms and box plots serialise every input value. Aggregate first, then plot the aggregate: `value_counts()` or `np.histogram` followed by `px.bar` for histograms; precomputed quartiles or a random sample for box plots. For the 15-panel grids, use one faceted figure built from aggregated data.
  - Acceptance: no notebook over about 5 MB; charts read the same as before.
  - Optional: add a CI step that fails when a notebook exceeds a size limit or contains an output of type `error`.

## 5. Chapter tasks

### 5.1 kickstarter-projects

- **KICK-1 (H) [checked].** `binary-classification.ipynb` uses `backers_count` as a feature. Cell 22 says the column "contains the number of backers at the time of prediction, not the final number of backers". That is false: the rows are finished campaigns. Cell 43 then says the opposite, that it "leaks information about the outcome". Reported accuracy is 0.967 and ROC AUC 0.998 (cell 35).
  - Fix: train once with and once without `backers_count`, show both results, and rewrite cells 20 to 22 and 43 so the notebook teaches the leak as a before-and-after comparison.
- **KICK-2 (H) [checked].** The sample is itself an artifact. 65 of 124 categories contain only one outcome (for example, "3D Printing" 12 of 12 successful, "Academic" 0 of 18). Predicting each category's majority class gives 90.5% accuracy in-sample. Cell 43's first explanation ("drawn from a very specific slice of time") is wrong: launch years span 2009 to 2026. Cell 39 labels category "Dominates model decisions" without flagging this. Five duplicate project ids can fall on both sides of the split.
  - Fix depends on instructor decision D-3 (re-sample the data, or keep it and make this the lesson). In either case, correct cell 43, drop duplicate ids before splitting, and add a majority-class baseline (62%) and a category-majority baseline.
- **KICK-3 (M) [checked].** `spotlight` equals the outcome exactly (true for all 1,676 successful projects, false for all 1,030 failed). `preprocess-data.ipynb` cell 22 describes it as "featured on the Kickstarter homepage", and `case-overview.md` line 45 poses its effect as an open question. Rewrite both.
- **KICK-4 (M) [read].** Cell 39 says "XGBoost's default importance is based on how often a feature is used to split". For `XGBClassifier.feature_importances_` with tree boosters the default is gain. Confirm against the installed version's documentation, then correct.
- **KICK-5 (M) [read].** Cells 33 and 34 promise a majority baseline, segment slicing, and threshold experiments that never appear. Cells 1 and 43 and `case-overview.md` line 21 promise a "larger dataset" chapter that is not in `myst.yml`. The overview's five question groups are never answered, and the overview does not mention the classifier notebook. Either deliver or remove each promise.
- **KICK-6 (L) [read].** Cell 27: `select_dtypes(include="object")` raises a pandas deprecation warning (source of the path leak in HYG-3) and the prose says `object` where the output shows `str`. `preprocess-data.ipynb` has no introduction, and its last cell (`write_parquet`, cell 43) is unexecuted.

### 5.2 amazon-delivery

- **AMZ-1 (H) [checked].** `improve-classifier.ipynb` cell 2 creates `X_tr, X_val, y_tr, y_val` from `X_train`. Cell 7 then calls `xgb_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], ...)`. Early stopping is validated on rows the model was trained on, and `X_tr` is never used.
  - Fix: fit on `X_tr, y_tr`; print `best_iteration`.
- **AMZ-2 (H) [read].** Cell 11 chooses the decision threshold on the test set and reports that F1 (0.801, equal to the baseline's 0.80). Choose the threshold on the validation set and report test once.
- **AMZ-3 (H) [read].** The notebook never shows an improvement. The random search (cell 5, `n_iter=4`) is never evaluated on test, there is no results table, and the overview's 80% goal was already met by the baseline (82.6%). Add a table comparing baseline and each technique on the same test set, and write the conclusion from it, even if the conclusion is "little improvement".
- **AMZ-4 (H) [checked].** `total_items` is mechanically tied to the label. `case-overview.md` line 13 defines Delayed as "at least 10 items from a single truck arrived late". The delay rate rises from 12% in the lowest `total_items` decile to 99.9% in the highest, and the single rule `total_items > 419` reaches 81.5% accuracy against XGBoost's 82.6% with 15 features. `build-a-classifier.ipynb` cell 48 attributes the 63% importance to picking and packing time.
  - Fix: add the one-feature baseline and rewrite cell 48.
- **AMZ-5 (M) [read].** `build-a-classifier.ipynb` prose is stale: cell 29 prints `[[4361 867] [697 3075]]` while cell 30 interprets 694 and 3078; cell 32 prints 0.8262 while cell 33 says 82.7%.
- **AMZ-6 (M) [checked].** `zipcode` is treated as a numeric feature throughout. `precipitation_rate` is constant (`eda.ipynb` cell 43) but stays in the model and causes the NaN and RuntimeWarning in `eda.ipynb` cell 49.
- **AMZ-7 (M) [read].** `improve-classifier.ipynb` cell 8 suggests features the data cannot support (`total_items / number_of_trucks`, calendar features, 30-day zipcode delay rates: there is no truck or date column; `temperature × precipitation`: precipitation is all zeros). Cell 9 uses `scale_pos_weight` to up-weight "On time" while cell 0 argues recall on "Delayed" matters, and sets `eval_metric="aucpr"` with no `eval_set`.
- **AMZ-8 (L) [read].** `case-overview.md` line 15 mentions Canvas and has no learning objectives or data dictionary. One chart uses plotnine while the rest of the book uses Plotly. `improve-classifier.ipynb` cell 2 sets `warnings.filterwarnings("ignore")`.

### 5.3 australian-rental-market

- **AUS-1 (H) [checked].** `improve-the-model.ipynb` cell 15 builds `suburb_median_rent` with `df_train_fe.groupby("suburb")["price_display"].median()`. The median includes each row's own rent and is computed before the cross-validation in cell 20. On a replicated split, 15.5% of training rows are the only listing in their suburb and 26.5% have a feature exactly equal to their own target. It is the top feature in cell 25. The caution in cell 13 covers only test leakage.
  - Fix: out-of-fold or smoothed target encoding inside the pipeline, then re-run and rewrite the results.
- **AUS-2 (H) [read].** Cell 0 promises to measure each technique "on its own". Only one final model is evaluated (cell 23). The "Typical impact" column in the summary (cell 27) is unmeasured. Add the ablation or remove the claims.
- **AUS-3 (M) [read].** Cell 0 and `build-a-regressor.ipynb` cell 35 quote the "tuned" baseline as MAE ≈ 130 and R² ≈ 0.4. Those are the default model's numbers (131.76 and 0.385). The tuned model scored 123.98 and 0.449 (cell 34).
- **AUS-4 (M) [checked].** Cell 10: `amen_built_in_robes` is 0 for every row because the data says "Built-in Wardrobes" (present in 40% of rows).
- **AUS-5 (M) [checked].** `case-overview.md`: `locality` is described as a "broader administrative region" (line 65) but equals `suburb` in every row. State values are `Qld`, `Vic`, `Tas`, not the forms on line 69. Line 123 says XGBoost is "robust to outliers" while `improve-the-model.ipynb` cell 6 says squared-error loss is "dominated by" them.
- **AUS-6 (L) [read].** `build-a-regressor.ipynb` cell 1 has six unused imports and no introduction. The "tuned" configuration is chosen and judged on the test set.

### 5.4 walmart-sales-forecasting

- **WAL-1 (H) [read].** `build-a-forecasting-model.ipynb` cells 9, 13, 15, 24: `Sales_Lag1` and `Sales_Roll4` use actual prior-week sales throughout the 12-week test window. Ridge and XGBoost are therefore scored one week ahead, against a lag-52 baseline, under the framing "hold out the last 12 weeks".
  - Fix: state the forecast horizon explicitly and add a lag-1 persistence baseline, or restrict lag features to the horizon or longer.
- **WAL-2 (H) [read].** Cell 11 fills missing lags with per-series medians computed over the full data before the split, while cell 8 says "no future information ever leaks". 41.4% of training rows have no lag-52 value and receive this constant. Compute fill values from the training period only.
- **WAL-3 (M) [checked].** Cell 9 builds lags by row shift. 605 of 3,331 Store-Dept series have missing weeks, so 5.0% of lag-52 values are not from 364 days earlier. Reindex each series to a complete weekly calendar before shifting.
- **WAL-4 (M) [read].** `case-overview.md` line 48 says WMAE "triples" the holiday weight; both notebooks use 5. The test window (2012-08-10 to 2012-10-26) contains only Labor Day, so the model is never evaluated on Thanksgiving or Christmas. Line 22 says the data runs to "November 2012".
- **WAL-5 (M) [read].** Cell 28 says Store, Dept, and Size follow the lag features in importance. The output ranks IsThanksgiving, IsChristmas, MarkDown3, WeekOfYear, Year, and IsHoliday above Dept; Store and Size are not in the top 10. Cells 25 and 33 are generic "if..." text not tied to output.
- **WAL-6 (M) [read].** Store and Dept ids enter Ridge as unscaled numerics (cells 18, 20). MarkDown NaNs are filled with 0 as "no markdown" although `eda.ipynb` cell 6 says those columns do not exist before November 2011. Overview objectives 5 (tuning) and 7 (business recommendations) are not delivered.
- **WAL-7 (L) [read].** `eda.ipynb` execution counts are out of order; cell 22 has an unclosed parenthesis in prose.

### 5.5 campustown-zillow-listings

- **CAMP-1 (H) [checked].** The modelling target is not a list price. `price` in `data/properties_clean.parquet` equals the most recent `sold` event price in `data/price_history.parquet` for 98.4% of rows. The data dictionary (`case-overview.md` line 123) calls it "current list price" and `part-2a-price-predictor.ipynb` cell 0 says "predict the list price". `part-3-price-history.ipynb` cell 27 says "In Part 2 we predicted list price. Now... the realized sale price", but its `sold_price` equals Part 2's `price` for 98.9% of modelling rows. Part 3's MAPE drop from 17% to 5.6% comes from adding `list_price` as a feature.
  - Fix depends on instructor decision D-5. The minimal fix is to relabel the target as last sold price everywhere and rewrite Part 3's framing as "what does knowing the list price add".
- **CAMP-2 (H) [checked].** Part 3 cell 56 prints `Discount-prediction R²: -0.422` with no comment, and cell 58 presents the model as a per-listing offer tool. Mismatched list and sold pairs are never filtered: `list_to_sale_pct` ranges from −99.9% to +2,854%, 81 rows lie beyond ±50%, and 604 kept cycles contain more than one sold event. There is no naive "sold = list" baseline.
  - Fix: filter implausible pairs, add the naive baseline, and write the conclusion from the result.
- **CAMP-3 (H) [checked].** Part 3 states results that are never computed. Cell 24 "sold vs. removed" is built from `sold_cycles` only (the stored figure has one trace). Cell 58 says properties with two or more price cuts are "materially less likely" to close; a replication gives 79% sold with zero cuts, 72% with one, 71% with two. Cell 30 promises a per-property prior list price feature that is never built. Cell 10 calls pre-listing events "rare" where 13% of events are dropped.
- **CAMP-4 (M) [read].** The rubric in `case-overview.md` contradicts the notebooks. Line 265 and objective 5 ask students to use per-property list-to-sale ratio, days-to-sale, and price cuts to predict the sale outcome, which Part 3 cell 30 itself calls leakage. Line 260 requires Part 1 to load both parquet files and chart time trends; Part 1 loads one file and has no time chart. Depends on D-5.
- **CAMP-5 (M) [checked].** `part-2b-nlp-features.ipynb`: the `PhraseMatcher` phrases are singular only. Cell 20 shows granite 1.5%, stainless 0.3%, hardwood 3.3%; a plural-tolerant match gives 7.9%, 11.9%, 16.8%. Match on lemmas or add plural forms.
- **CAMP-6 (M) [read].** Part 2b prose disagrees with output: cell 25 says luxury lifts price 60% (output: 34%); cell 49 names luxury, granite, and updated_kitchen as top lifts (output: primary_suite, luxury, finished_basement); cell 4 says only the tokenizer is loaded (output shows `tok2vec`). The NLP gain is mixed (MAPE 17.06 to 16.55, RMSE and R² worse, cell 42) while the rubric requires "measurably better". Part 2a cell 22 says "12% MAPE" (output: 17.06%).
- **CAMP-7 (L) [checked].** "Nine universities" (`case-overview.md` line 40, Part 1 cell 23) should be 11. Part 1 cell 49's example bullets are wrong against the data (top price per square foot is Davis, Carrboro, Chapel Hill). The year 2026 is hard-coded in Part 1 cells 12 and 18.
- **CAMP-8 (L) [read].** Many cells in parts 1, 2a, and 2b have outputs but no execution count. The outputs do match the code, so a clean re-run is enough.

### 5.6 instacart

- **INST-1 (H) [checked].** `customer_behavior_analysis.ipynb`: 25 of 35 code cells have no output, including data loading (cells 4, 6, 8), all of Part A market-basket analysis (11 to 33), the profile tables (38 to 46), the heatmap (77, 79), and department mix (91 to 95). The takeaways are written as results. Cell 31 cites the rule "baby food formula → baby accessories", which is impossible at the notebook's own `min_support=0.02` because baby accessories appears in 0.23% of orders.
  - Fix: run the notebook and rewrite every takeaway from the real output.
- **INST-2 (H) [checked].** `order_products_train` holds exactly one order per user, always their last, with a minimum `order_number` of 4. So "average basket size per customer" (cells 40, 53) is a single basket, the reorder-rate-by-order-number curve (cells 99, 100) is a cross-section of users and not a lifetime curve, and the "Light (1-5)" segment is really 4 to 5 orders. `case-overview.md` questions C1 and C3 (lines 232 to 243) inherit this.
  - Fix depends on instructor decision D-4 (add the prior split to the data mirror, or reframe as cross-sectional).
- **INST-3 (H) [checked].** Takeaways that contradict stored output:
  - `eda.ipynb` cell 49: says personal care has the highest reorder rate. It is the lowest (0.337). `analysis.ipynb` cell 31 has it right.
  - `eda.ipynb` cell 52: says personal care and babies are added to the cart first. Alcohol is first (5.6), babies last (11.1).
  - `analysis.ipynb` cell 51: says dairy and beverages first, bulk last. Alcohol is first, bulk mid-table.
  - `customer_behavior_analysis.ipynb` cell 62: says Light is the largest segment. Regular is (92,744 vs 43,576).
  - Cell 84: says reorder rate rises with basket size then plateaus. The output is U-shaped.
  - Cell 88: says the scatter "validates" the segmentation. The segments are defined on the x-axis variable.
  - `eda.ipynb` cell 55: median basket "about 8". It is 9.
- **INST-4 (M) [checked].** `case-overview.md` lines 157 to 189 were copied from the dataset repository. They refer to `overview.md`, `README.md`, `eda_tutorial.ipynb`, and "data files included in this repository", none of which exist here, and describe unzipping with `zipfile` where the notebooks read from a URL. Section 3 says all listed analyses work with the included files; several need the prior split.
- **INST-5 (M) [unverified].** `order_dow` 0 = Saturday is stated as fact (`case-overview.md` line 62, `dow_map` in all three notebooks). Instacart is not known to have documented the encoding. Label it an assumption.
- **INST-6 (M) [unverified].** The official dataset page `https://www.instacart.com/datasets/grocery-shopping-2017` returned 404 from the review sandbox. It is linked from `eda.ipynb`, `customer_behavior_analysis.ipynb` cell 0, and `case-overview.md` line 188. Confirm from an open network, then repoint or remove.
- **INST-7 (L) [read].** `eda.ipynb` cell 0 promises practice exercises, `pd.crosstab`, and missing-value heatmaps that do not exist, and the notebook ends at cell 70 without a summary. Horizontal-bar cells have `height=600` in source but the stored figures were not re-run (`eda.ipynb` 42, 44, 48, 51; `analysis.ipynb` 18, 22, 26, 30, 46, 50). Tips are blockquotes, not MyST admonitions. `blog-post.md` lines 52 to 55 have collapsed bullets, and line 14 promises a download link that is absent.

### 5.7 credit-card-transactions

These notebooks need the 2.3 GB dataset. If you cannot obtain it, limit yourself to the prose and code fixes and flag the notebooks as needing an instructor re-run.

- **CC-1 (H) [read].** The same composite "suspicious" flag yields 3,155 rows in the Polars notebook (cell 53) and 3,508 in the DuckDB notebook (cell 46). DuckDB cell 47 says "The business logic is identical; only the syntax changes." Likely cause [unverified]: `Datetime` has minute resolution, so same-minute ties are ordered arbitrarily by `sort` and `LAG`.
  - Fix: add a deterministic tie-breaker to both, and assert the two counts match.
- **CC-2 (H) [read].** Polars cells 49 to 53 say "only seconds apart" and "within 60 seconds", but `Datetime` is built from HH:MM only (cell 16), so gaps are multiples of 60 seconds and `< 60` means "same minute". `user_avg_amount` uses each user's whole history, including later transactions. The flag is never compared with `Is Fraud?`.
  - Fix: reword, use an expanding mean, and report the rule's precision and recall against the label.
- **CC-3 (M) [read].** Polars cells 30 to 34 compute three flag columns but never assign them (cell 34's output still has 16 columns), yet cell 32 says "you can now quickly segment". Cell 34 puts `.alias("is_refund")` inside `filter`, which does nothing. Cell 15 prose names the column `"timestamp"`; the code creates `"Datetime"`. Cell 40's SQL "equivalent" returns partial sums for the first nine rows where `rolling_sum(window_size=10)` returns nulls.
- **CC-4 (M) [read].** DuckDB cell 14 says `Is Fraud?` holds "True" and "False"; cell 13's output shows Yes and No. Cell 19 describes "the `.value_counts()` method" above a SQL `GROUP BY`. The view built in cell 15 is never used.
- **CC-5 (M) [read].** `introduction-to-duckdb.ipynb` cell 19: the published output is the fallback message "Skipped remote query (... httpfs ...)", so the remote-parquet demo shows nothing. Cell 9 says DuckDB queries pandas DataFrames "without needing to load them into memory first" (they are already in memory). Cell 13 claims "the full SQL standard".
- **CC-6 (M) [read].** `case-overview.md` objective 3 (missing zip codes), objective 6 (limits of synthetic data), and task 5 (online + foreign + above-average) have no counterpart in the notebooks. Both analysis notebooks list "Identify and handle missing values" in cell 0 and never do it. `introduction-to-polars.ipynb` cell 29 promises a merchant-metadata join that does not exist. Overview line 128 is an orphan footnote.
- **CC-7 (L) [read].** `introduction-to-polars.ipynb` cell 10 quotes type names that differ from the outputs in cells 6 and 9. DuckDB cells 34 and 46 contain ipywidget progress outputs that do not render on a static site. The Polars notebook's cell 3 says "using both Pandas and Polars" but pandas appears only in markdown.

### 5.8 foundation-products

- **FND-1 (H) [checked].** `competitive-analysis.ipynb` cells 32 and 36 store `KeyError` tracebacks ("Columns not found: 'lightweight', 'full_coverage', ..." and "None of [Index(['lightweight', 'skin_tint', ...])] are in the [columns]"). The keyword flags they need are commented out in cells 14 and 30, and cell 36 also uses a nonexistent `current_price`. Cell 41 still reports keyword and "Gen Z score" findings.
- **FND-2 (H) [checked].** Cell 5 returns `"brand": ""`, so `foundation_products.csv` has an empty brand in all 227 rows. The stored brand charts (cells 24 to 28) come from an older first-word version with "brands" such as `Foundation`, `IT`, `Color`. Cell 41 says "Revlon, Maybelline, and L'Oréal dominate"; the stored chart shows COVERGIRL 11, L'Oreal 10, 'Foundation' 9, Maybelline 9, and no Revlon in the top 15.
  - Fix: extract brand from the product JSON, re-run, and rewrite cell 41 from the output.
- **FND-3 (H) [checked].** The data includes non-makeup items (a "Foundation Study Bible", Asimov's *Foundation*, mattress foundations, a nail base coat) and prices in PYG, ARS, CAD, and GBP read as US dollars. Cell 12 calls 45,152 and 19,575 "outliers or errors"; they are PYG and ARS prices.
  - Fix: filter on the price currency symbol and on a makeup flag before any analysis.
- **FND-4 (M) [read].** Cell 24 prints "rating vs. log reviews" but correlates raw counts. Cell 41 says "Nearly all products rate 4.3-4.8"; cell 16 shows a 25th percentile of 4.10. "Step 6" follows Step 4. Cell 8 overwrites the tracked CSV on every run. Execution counts are out of order.
- **FND-5 (M) [checked].** `case-overview.md` lines 79 and 113 describe `search-results/` and `products.csv`, which exist only in the remote datasets repo; this repo holds `product-results/` (227 files). `parse-json.ipynb` cell 36 points to a "next step" that is a hidden page. The overview's MAC question (line 132) has only two MAC products to draw on.

### 5.9 cu-zillow-listings

- **CUZ-1 (H) [checked].** `case-study-demo.ipynb` cells 26 to 28 and 38 treat `days_on_zillow` as time to sale. Its median is 577 days, 66% of rows exceed 365, and `date_posted + days_on_zillow` clusters in January and February 2026, so it looks like time since posting. The recap's "Most properties sell within a few months" is unsupported, and `case-overview.md` question 3 (lines 77 to 80) cannot be answered with this dataset.
  - Fix: remove or reframe the liquidity analysis and the overview question, unless a sold date can be added to the data.
- **CUZ-2 (M) [checked].** Two rows have `living_area == 0`, which makes `price_per_sqft` infinite and Champaign's `avg_price_per_sqft` in cell 15 `inf`. The minimum price is 0. Cell 29 silently drops 438 rows with no `date_posted`. The first eight months have 1 to 9 sales each (the 2022-08 "median" is one $1.15M sale) and dominate the trend line. Add a cleaning step and a minimum-count filter.
- **CUZ-3 (M) [checked].** Cell 12 says Savoy is "not necessarily more expensive *space*". Median price per square foot is 188 in Savoy against 150 in Champaign and 145 in Urbana, and the recap itself says Savoy is highest. The recap recommends adding "a bathroom or attached garage" for ROI against the correlation caution in cell 18.
- **CUZ-4 (M) [checked].** `case-overview.md` line 23 says "last ~5 years"; the data spans 2022-05 to 2026-03. "Sold" and "listings" are used interchangeably (lines 21, 45; "Median Listing Price" in cell 15).
- **CUZ-5 (L) [read].** Execution counts are out of order. Admonitions in cells 12 and 36 refer to charts "above" that are below. The overview's code snippet omits `import pandas`. `cu-zillow-listings-starter.ipynb` duplicates the overview verbatim and is not in `myst.yml` (see D-2).

### 5.10 data-job-postings

- **DJP-1 (H) [checked].** `hr-analytics.ipynb` cell 3 loads `data_jobs_preprocessed.parquet`, which is gitignored and produced only by `eda.ipynb` cell 78, under a heading marked "(Optional)". Make the HR notebook self-sufficient: load a hosted cleaned file, or rebuild it when missing.
- **DJP-2 (M) [read].** `hr-analytics.ipynb` cells 20 to 24 describe a "year-over-year ratio" and "H1 of the most recent year to the previous year". The data covers 2023 only; the code compares the last 180 days with the prior 180. The section title promises a heatmap that is never drawn, and `skill_by_month` (cell 21) is unused. The top "heating up" skills have shares of 0.1% to 0.2%, yet cell 24 calls matching employees "highest-risk retention targets".
- **DJP-3 (M) [read].** The chart titled "Top 15 U.S. cities" (cells 12 to 14) is topped by "Anywhere" with "United States" third, and cell 14 recommends "the top three cities here". The "primary competitors" in cell 17 are mostly job boards and staffing firms (Dice, Insight Global, Upwork, Robert Half, Jobot), and KPMG appears under two names. Filter non-city locations and intermediaries.
- **DJP-4 (M) [read].** Cell 9 says a `position_in_market` of 0.5 "means we are sitting at P50". In cell 8, Data Scientist has midpoint = p50 = 130,000 and scores 0.42. The measure is position within the interquartile range.
- **DJP-5 (M) [read].** `eda.ipynb` cells 59 and 60 say `ast.literal_eval` "can execute arbitrary code if the input string is malicious". That describes `eval`. Cell 119 claims "holding role constant" over a plain median by skill (cell 120).
- **DJP-6 (M) [unverified cause].** "Sudan" is the 8th-largest country (cell 86, 21,781 postings) and the highest-paying (cell 103). This is implausible and is presented without comment. Investigate the source column and either correct or caveat.
- **DJP-7 (L) [read].** `eda.ipynb` cells 97 to 122 have outputs but no execution count. "Drop Rows with Missing Job Title" (cells 21 to 25) drops nothing. The "Job Titles" heading (cell 80) covers remote share. "Persist the Cleaned Dataset" (cell 124) comes after "What's next".
- `quiz-01.ipynb`: see D-1.

### 5.11 conference-calls

- **CONF-1 (H) [read].** `nlp-in-business.ipynb` cells 16 to 18: the classification report shows accuracy 0.33 on six test rows with F1 of 0.00 for two classes, and the demo predictions are made at probability 0.28 (chance is 0.25). Cell 17 says "the classifier is already useful".
  - Fix: enlarge the synthetic data or use cross-validation, and write the prose to the actual result.
- **CONF-2 (M) [checked].** Cells 12 and 13: `min_df=2` leaves a six-word vocabulary, so every topic's "top 6 words" is the whole vocabulary. Four of 15 reviews become all-zero vectors and `argmax` assigns them to Topic 1.
- **CONF-3 (M) [read].** `preprocessing.ipynb` cell 32 ends "In the next page, we will see how to use these features"; no next page exists. `overview.md` line 26 promises a "running case study" on earnings-call transcripts; the only transcript is an unsourced excerpt in cell 2. Stemming and vectorisation are listed in cell 6 and never shown.
- **CONF-4 (M) [read].** `preprocessing.ipynb` cells 21 to 30: the "clean" tokens still contain `'\n'` (no `is_space` filter). The NER output tags "AI" as GPE and "Claude 4.5" as LAW and misses several company names, with no comment. Either fix or turn it into a teaching point about model limits.
- **CONF-5 (L) [read].** Cell 0's table says the accounting demo finds "anomalous" expenses; the section does categorisation. Typos: "lemmatizatio", "Puntuation". No code cell in either notebook has an execution count. The page is named `overview.md` where the convention is `case-overview.md` (renaming requires updating `myst.yml`).

### 5.12 financial-data-with-llms

Do not execute `analyze-filings-with-llm.ipynb` without the instructor's API key and consent to the cost.

- **LLM-1 (H) [unverified].** `analyze-filings-with-llm.ipynb` cell 32 lists `gpt-5.4-mini` at $0.15 input and $0.60 output per 1M tokens, and `gpt-5.4-nano` at $0.05 and $0.20, as "time-of-writing list price". A reviewer found $0.75/$4.50 and $0.20/$1.25 on a model-listing API. Check the provider's own pricing page before editing. The "output is 3 to 5× input" rule of thumb (`case-overview.md` line 92, cell 33) should be checked at the same time.
- **LLM-2 (H) [read].** Cell 31 says it estimates the cost of "this entire notebook"; the code prices only the last call. Accumulate usage inside the `chat()` helper.
- **LLM-3 (H) [read].** LLM outputs are never validated, and hallucination is never mentioned. The rubric (`case-overview.md` line 187) requires parsed responses to be "validated"; the notebook only calls `json.loads` (cells 22, 26, 29). Evidence snippets (cell 27) are not checked against the source text. Task 3 scores tone neutral-to-cautious, 3 of 5 (cell 19); task 6, built from earlier LLM outputs, returns "positive", 4, confidence "high" (cell 29), and the disagreement is not discussed. Cell 30 gates a compliance alert on self-reported confidence.
  - Fix: add a verification section (substring check on evidence quotes, schema validation, cross-check figures against the XBRL table from the first notebook) and a short discussion of the conflicting scores.
- **LLM-4 (M) [checked].** `trim()` (cell 11) keeps the first and last 6,000 characters. Risk Factors is 68,329 characters, so the model sees about 18% while the prompt (cell 21) asks it to judge severity by "how much space and emphasis the filing gives". State the limitation or chunk the section.
- **LLM-5 (M) [read].** Key handling is inconsistent. `case-overview.md` line 170 and rubric line 184 say keys come from environment variables only; cell 5 reads `openai_config.json` first. `read-edgar-filings.ipynb` cell 7 hard-codes "John Doe jdoe@example.com" while overview line 49 requires a real monitored email. Pick one mechanism and make all three places agree.
- **LLM-6 (L) [read].** Cell 1: `pip install openai>=1.40.0` is unquoted, so a shell treats `>` as a redirect. Cell 4 uses `:::warning` without braces. Cell 18 says the sentiment redo is in "section 9"; it is section 10. The second notebook cannot run without the first because `extracted/` is gitignored; say so at the top. There is no retry or rate-limit handling.

### 5.13 airbnb-barcelona-listings

- **ABNB-1 (H) [unverified].** `clean-airbnb-listings.ipynb` cell 9 reads `https://data.insideairbnb.com/spain/catalonia/barcelona/2025-09-14/data/listings.csv.gz`. Inside Airbnb retires old snapshots. Confirm whether the URL is live; either way, point the notebook at a pinned copy (see D-7 for where it should live).
- **ABNB-2 (M) [read].** Cell 21: `np.where(df_c["is_superhost"] == "t", 1, 0)` runs before missing-value handling, so the 383 missing `host_is_superhost` values (cell 15) silently become 0.
- **ABNB-3 (M) [checked].** Cells 25 and 28: `dropna` cuts 19,410 rows to 11,794 (39%) with no comment, which removes every never-reviewed listing. The saved output still has 18 empty prices, a maximum price of 10,000, and `minimum_nights` up to 865, while `case-overview.md` line 45 calls the result "more reliable". Add a validation step and a short drop-versus-impute discussion.
- **ABNB-4 (L) [read].** Cell 0 promises date conversion and sampling; neither is done. `import os` is unused. The overview's title is "Case Overview" with a single section and no business question.

### 5.14 index.md, README.md, grammar-of-graphics.md

- **IDX-1 (H) [checked].** `content/index.md` lines 39 to 44 and 55 to 83 promise PostgreSQL, Tableau Desktop, Plotly Dash dashboards, BERTopic, serverless functions, and ETL on datasets over 10 GB. None of these appear in any chapter. Rewrite depends on instructor decision D-6.
- **IDX-2 (M) [checked].** `## Prerequisites` (line 95) is empty. "Dataset Candidates" (lines 97 to 106) is a planning table: four of its six datasets are not in the book. Lines 63 to 65 use literal "o" characters as sub-bullets. Line 88 names DeepNote.
- **GOG-1 (M) [read].** `content/grammar-of-graphics.md` is not in `myst.yml` (see D-2). If it is kept: its plotnine example uses `geom_smooth(method='loess')`, which needs `scikit-misc`, and the install line (148) omits it. Line 132's "Performance" bullet says nothing about performance.

### 5.15 Cross-chapter consistency

- **X-1 (M) [checked].** No two overview pages share a structure. Only five have a "Learning Objectives" section (credit-card, data-job-postings, walmart, financial-data-with-llms, campustown). Three use MyST admonitions heavily (credit-card, financial-data-with-llms, campustown), and six use none. Some use emoji headings and some do not. After the chapter fixes, bring the overviews to one skeleton: business context, learning objectives, dataset and data dictionary with source and licence, notebooks in this case study, setup. `campustown-zillow-listings/case-overview.md` and `financial-data-with-llms/case-overview.md` are the best current models.
- **X-2 (M) [read].** Most notebooks have no exercises and no closing summary. Do not invent graded work (see D-9), but every notebook should at least end with a summary that matches its outputs.

## 6. Decisions for the instructor

Do not act on these without an answer. Tasks above that depend on them say so.

- **D-1: Answer keys.** `hidden: true` in `myst.yml` removes a page from navigation only; the build still produces it. Built and reachable: `data-job-postings/quiz-01` (an abandoned draft: a copy of the EDA plus out-of-order scratch cells computing answer values), `cu-zillow-listings/case-study-demo` (a full worked answer to that chapter's deliverable), `foundation-products/competitive-analysis`. In the repo but not built: `instagram-brand-profiles/quiz-03.ipynb`, `google-trends-celebrities/quiz-04-solution.ipynb`, and both `case-studies/` notebooks, all with solutions filled in. Options: delete, move to a private repo, or keep as worked examples.
- **D-2: Orphaned content.** Not in `myst.yml`: `content/grammar-of-graphics.md`, `content/case-studies/` (two notebooks, one with a saved torch import error and the other never executed), `content/cu-zillow-listings/cu-zillow-listings-starter.ipynb`, `content/instagram-brand-profiles/`, `content/google-trends-celebrities/`. For each: add to the table of contents, or delete.
- **D-3: Kickstarter sample.** Re-sample the dataset so categories are not single-outcome, or keep it and teach the artifact (KICK-2).
- **D-4: Instacart data.** Add the prior order-products split to the mirror so customer-level analysis is valid, or reframe the customer notebook and overview questions C1 and C3 as cross-sectional (INST-2).
- **D-5: Campustown target and rubric.** Relabel the target as last sold price and rework Part 3's framing, or re-source a true list price. The rubric rows for Part 1 and Part 3 need rewriting in either case (CAMP-1, CAMP-4).
- **D-6: Course scope on the landing page.** Which of PostgreSQL, Tableau, Dash, BERTopic, cloud, and 10 GB ETL are still part of the course (IDX-1).
- **D-7: Data kept in this repo.** `campustown-zillow-listings/data/` holds a Zillow extract with 35,940 street addresses and agent text containing phone numbers and emails, committed twice at 19 MB each (`campustown_properties.parquet` and `properties_clean.parquet`). 210 of the 227 `foundation-products/product-results/*.json` files contain reviewer names and profile URLs (1,560 entries). `instagram-brand-profiles/data/` holds captions and tagged names. Options: keep, strip the personal fields, or move to the datasets repo. Only the data-jobs dataset states a licence.
- **D-8: Repository licence.** There is no `LICENSE` file. `content/instacart/blog-post.md` is a verbatim copy of a third-party blog post; decide whether to keep it or link to it.
- **D-9: Exercises and assessment.** Whether to add student tasks to the chapters, and in what form. Several flaws found here (the Kickstarter leak, the Amazon `total_items` rule, the disagreeing fraud counts) would make good "audit this analysis" exercises if the instructor prefers to keep and teach them and not simply fix them.
- **D-10: Notebook execution in CI.** The deploy workflow publishes committed outputs as they are. Executing notebooks in CI would catch stale outputs but needs the pinned environment, the large credit-card data, and exclusion of the paid LLM notebook.

## 7. Definition of done

For each chapter pull request:

1. Every notebook touched runs top to bottom in the pinned environment with sequential execution counts and no `error` outputs, or the pull request states which notebook could not be run and why.
2. Every takeaway, insight, and summary cell agrees with the output directly above it.
3. The chapter's overview page describes what the notebooks do, with no promises of content that does not exist.
4. `jupyter-book build --html` (or `--site` in a restricted sandbox) finishes with no new warnings.
5. No instructor-machine paths remain in outputs, and no notebook exceeds about 5 MB.
6. Any file renamed or added to the book is reflected in `myst.yml` in the same change.
7. The pull request description lists the task ids closed (for example `KICK-1, KICK-3`) and any `[unverified]` item it confirmed or refuted.

## 8. How this review was done

Four reviewers each read a slice of the book in full (every markdown page and every notebook cell, with outputs summarised), and a fifth pass covered the repo-level checks: file sizes, build warnings, data URLs, secrets, and configuration. The highest-severity findings were then re-checked against the notebook source, stored outputs, or the committed data. No API keys were found in the current tree; history was not scanned because the review clone was shallow. The full HTML build could not be run because the theme download was blocked in the review sandbox; the content-only build passed with 46 pages.
