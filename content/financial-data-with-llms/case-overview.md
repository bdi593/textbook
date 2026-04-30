# Case Overview

In this case study, we combine two highly practical skills for modern business analytics:

1. Pulling real corporate filings from the U.S. Securities and Exchange Commission (SEC) using the [`edgartools`](https://github.com/dgunning/edgartools) Python package, and
2. Using a Large Language Model (LLM) API - accessed through OpenAI's Python SDK - to analyze the unstructured text inside those filings.

Together, these skills let you build the kind of "AI analyst" workflow that investment firms, accounting groups, and corporate strategy teams have been racing to deploy since 2023.

## 🏢 What is EDGAR?

[EDGAR](https://www.sec.gov/edgar/search/) stands for Electronic Data Gathering, Analysis, and Retrieval. It is the official online filing system operated by the U.S. Securities and Exchange Commission (SEC) since the early 1990s. Every public U.S. company — and many private companies that issue regulated securities — must submit periodic reports to EDGAR, and those filings are made freely available to the public at [https://www.sec.gov/edgar](https://www.sec.gov/edgar).

EDGAR is one of the largest publicly available collections of high-quality business data in the world. It contains decades of financial statements, executive compensation disclosures, risk factors, business descriptions, ownership data, and material events for thousands of companies.

### What are SEC filings?

An SEC filing is a formal document a company submits to the SEC to comply with U.S. securities law. Each filing has a form type that determines its structure and contents. Some of the most commonly analyzed forms include:

| Form        | What it is                                 | Typical use in analytics                                               |
| ----------- | ------------------------------------------ | ---------------------------------------------------------------------- |
| **10-K**    | Annual report                              | Long-form business description, audited financials, risk factors, MD&A |
| **10-Q**    | Quarterly report                           | Unaudited quarterly financials and updates                             |
| **8-K**     | Current report ("material event")          | Mergers, leadership changes, earnings releases, restructurings         |
| **DEF 14A** | Proxy statement                            | Executive compensation, board composition, shareholder proposals       |
| **S-1**     | IPO registration statement                 | First public look at a company filing to go public                     |
| **Form 4**  | Insider transactions                       | Stock buying/selling by officers, directors, and 10%+ owners           |
| **13F**     | Institutional manager holdings (quarterly) | What hedge funds and asset managers own                                |

In this case study we focus on the 10-K because it contains both rich quantitative data (audited financial statements) and rich qualitative data (the _Business_, _Risk Factors_, and _Management's Discussion and Analysis_ sections) — exactly the kind of unstructured text where an LLM adds the most value.

:::{seealso} What is in a 10-K?

A typical 10-K is divided into four parts and roughly 15 numbered "items." The most-read sections in industry are:

- **Item 1 — Business**: how the company makes money, its segments, customers, and competition.
- **Item 1A — Risk Factors**: the company's own list of what could go wrong, written by lawyers but extremely informative.
- **Item 7 — Management's Discussion and Analysis (MD&A)**: management's narrative explanation of recent results.
- **Item 8 — Financial Statements**: the audited income statement, balance sheet, cash flow statement, and notes.

:::

### The `edgartools` library

[`edgartools`](https://github.com/dgunning/edgartools) is a Python library that wraps the SEC's public EDGAR endpoints and gives you a clean, pandas-friendly way to look up companies, list their filings, and parse the contents of common forms (including 10-K, 10-Q, 8-K, and XBRL financial statements). We pin it to `edgartools>=5.0.0,<6.0.0` in this chapter so that example code in the notebooks continues to behave the same way even if a future major release changes the API.

:::{important} Set your SEC user agent

The SEC requires every automated request to include an identifying email in the `User-Agent` header. `edgartools` exposes this through `set_identity("Your Name your.email@example.com")`. You only need to call this once per Python session before making any requests, and you should use a real email address you actually monitor.

:::

## 🤖 What is an LLM API?

A Large Language Model (LLM) API is a hosted service that lets your code send a prompt to a model and receive a generated response. Instead of running a 70-billion-parameter model on your own laptop, you make an HTTPS request to a provider that hosts the model on GPUs and pay per token consumed.

The dominant API surface is the one introduced by OpenAI. It is so widely adopted that most other providers - Anthropic (via compatibility layers), Google, Mistral, DeepSeek, Together, Groq, Fireworks, and aggregators like OpenRouter - expose endpoints that accept the same request shape. This is what people mean when they say a provider supports "OpenAI-compatible syntax".

### Why the OpenAI Python package works for many providers

The official [`openai`](https://github.com/openai/openai-python) Python SDK exposes a single `OpenAI` client class. The client takes two arguments that you can override:

- `api_key` — your secret key for the provider you are calling, and
- `base_url` — the HTTPS endpoint the SDK should send requests to.

By default, the SDK points at `https://api.openai.com/v1`. If you change `base_url` to a different OpenAI-compatible endpoint and pass that provider's `api_key`, the **same code** works against the new provider with no other changes. That is the entire trick:

| Provider     | `base_url`                              | Works with `openai` SDK? |
| ------------ | --------------------------------------- | ------------------------ |
| OpenAI       | `https://api.openai.com/v1`             | ✅ Native                |
| OpenRouter   | `https://openrouter.ai/api/v1`          | ✅ OpenAI-compatible     |
| Groq         | `https://api.groq.com/openai/v1`        | ✅ OpenAI-compatible     |
| Together AI  | `https://api.together.xyz/v1`           | ✅ OpenAI-compatible     |
| Fireworks AI | `https://api.fireworks.ai/inference/v1` | ✅ OpenAI-compatible     |
| DeepSeek     | `https://api.deepseek.com/v1`           | ✅ OpenAI-compatible     |

Standardizing on this shape means your analytics code is portable: you can switch providers when prices fall, latency spikes, or a model is deprecated, without rewriting your application logic.

### What is OpenRouter?

[OpenRouter](https://openrouter.ai/) is an API aggregator. Instead of signing up with each model vendor separately, you create one OpenRouter account and get access to hundreds of open- and closed-source models — GPT-class models, Anthropic's Claude family, Google Gemini, Llama, Mistral, DeepSeek, Qwen, and many more — all behind a single OpenAI-compatible endpoint. You pick a specific model by passing its identifier (for example `openai/gpt-5.4-mini` or `meta-llama/llama-3.1-8b-instruct`) to the `model` parameter.

OpenRouter is convenient for classroom use because students can experiment with several models from different vendors using one API key, and the platform exposes a transparent per-model price list.

## 💵 How LLM APIs are priced

LLM API pricing is almost always per token, where a _token_ is roughly ¾ of an English word. Providers publish two prices for each model:

- **Input price** — what you pay per million input tokens (your prompt, system messages, and any context you supply).
- **Output price** — what you pay per million output tokens (the model's generated response).

Output tokens are typically 3× to 5× more expensive than input tokens because generation is the costly step.

```text
Cost ≈ (input_tokens  / 1,000,000) × input_price
     + (output_tokens / 1,000,000) × output_price
```

A few important points to internalize:

1. **Smaller models are dramatically cheaper.** A "nano" or "mini" model can be 20×–100× cheaper than a frontier model for the same workload. For routine analytics tasks like classification, extraction, summarization, and reformatting, small models are usually more than good enough.
2. **Prompts add up.** If you stuff an entire 10-K into the prompt for every question, you pay for those input tokens _every single call_. Caching, chunking, and re-using extracted intermediate results matter.
3. **Structured output (JSON schemas) costs the same** as free-text output token-for-token, but it usually _reduces_ downstream parsing/clean-up work and can shorten your output by removing chit-chat.
4. **Free tiers exist** but are rate-limited and not guaranteed; do not depend on them for production.

:::{tip} Estimate before you spend

Most providers expose a token counter (or you can use [`tiktoken`](https://github.com/openai/tiktoken) locally for OpenAI models). Always estimate prompt size before running a loop over 1,000 documents. A back-of-the-envelope calculation can save you from a surprise bill.

:::

## 📊 How to compare LLM models

There are far too many LLMs released each month to evaluate by hand. Analysts and engineers rely on a few public resources to filter the field:

- **Provider pricing pages.** Always your first stop. OpenAI, Anthropic, Google, and OpenRouter all publish per-model pricing tables.
- **[Artificial Analysis](https://artificialanalysis.ai/)** — independent benchmarks of cost, latency (tokens/sec), and quality across most commercial models. Excellent for "is this model fast and cheap enough for my use case?" questions.
- **[LMArena (formerly Chatbot Arena)](https://lmarena.ai/leaderboard)** — a crowdsourced human-preference leaderboard where users blind-vote between two model responses.
- **[Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)** — academic benchmarks (MMLU, GSM8K, HellaSwag, etc.) for open-weight models.
- **[OpenRouter rankings](https://openrouter.ai/rankings)** — real-world usage data showing which models developers actually pay for and on which workloads.
- **Domain-specific benchmarks** — for finance specifically, look at FinanceBench, FinQA, and the [Vals AI Legal/Finance leaderboards](https://www.vals.ai/).

A reasonable workflow for picking a model:

1. **Define the task and a quality bar.** "Summarize a Risk Factors section into five bullet points that a portfolio manager would accept."
2. **Filter by price and latency.** Eliminate any model that is too expensive or too slow for the volume you expect.
3. **Run a small evaluation set** (10–30 examples) yourself across the 2–3 surviving candidates. Hand-grade or LLM-grade the outputs.
4. **Pick the cheapest model that clears the quality bar.** Re-evaluate every quarter — the frontier moves quickly.

:::{caution} Leaderboards are not your evaluation

Public benchmarks tell you which models tend to be good _on average_. They do not tell you which model is best for _your_ prompts on _your_ data. Always run a small private eval before standardizing on a model in production.

:::

## 🎯 Learning Objectives

By the end of this case study you should be able to:

1. Explain what EDGAR is, what a 10-K filing is, and what kinds of business questions can be answered from SEC filings.
2. Use `edgartools` (v5.x) to look up a public company by ticker, list its filings, fetch its most recent 10-K, and pull specific sections (e.g., _Business_, _Risk Factors_, _MD&A_).
3. Configure the `openai` Python client to talk to either OpenAI directly _or_ an OpenAI-compatible provider such as OpenRouter, by changing only `api_key` and `base_url`.
4. Send chat-completion requests with both free-text and structured JSON-schema response formats.
5. Apply small/cheap models (e.g., `gpt-5.4-mini`, `gpt-5.4-nano`) to realistic financial-text tasks such as summarization, sentiment scoring, risk classification, and entity extraction.
6. Reason about the cost of a workflow before running it at scale, and about which model to pick given quality, price, and latency constraints.

## 📚 Notebooks in This Case Study

This chapter contains two notebooks, designed to be worked through in order:

1. **[`read-edgar-filings.ipynb`](./read-edgar-filings.ipynb)** — Uses `edgartools` to look up companies, list their filings, fetch a recent 10-K, and extract clean text from named sections. The output of this notebook (a few sections of one company's 10-K) becomes the input to the next notebook.
2. **[`analyze-filings-with-llm.ipynb`](./analyze-filings-with-llm.ipynb)** — Uses an OpenAI-compatible API (OpenAI directly, or OpenRouter) to run several analytical tasks against the 10-K text: summarization, sentiment, risk-theme classification, named-entity extraction, and a final "executive briefing" task. Some tasks use free-form responses, others use a strict JSON response schema.

:::{tip} Bring your own API key

You will need either an OpenAI API key (with at least a few dollars of credit) or an OpenRouter API key. If you are comfortable with another provider (e.g., DeepSeek) that provides OpenAI-compatible APIs, you can use that as well. The notebooks read the key from a JSON file or the `OPENAI_API_KEY` environment variable so that you never paste it directly into the notebook.

:::

## 🧰 Setup

Install the pinned dependencies once:

```bash
pip install "edgartools>=5.0.0,<6.0.0" "openai>=1.40.0"
```

:::{warning} Never commit API keys

Treat your `OPENAI_API_KEY` like a credit-card number. Do not paste it into a notebook cell, do not commit it to Git, and rotate it immediately if you suspect it leaked. The notebooks in this chapter only ever read keys from environment variables.

:::

:::{seealso} What is _rotating_ an API key?

Rotating an API key means generating a new key to replace an old one, and then deleting the old key. This is a security best practice if you think your key may have been exposed (for example, if you accidentally pasted it into a public GitHub repo). By rotating the key, you ensure that any unauthorized party who obtained the old key can no longer use it to access the API.

:::

## 📝 Grading Rubric (100 points)

| Component                                    | Points  | Criteria                                                                                                                                                                          |
| -------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Environment & reproducibility                | 10      | Pinned `edgartools` and `openai` versions installed; SEC identity and API key loaded from environment variables (never hard-coded); notebooks run top-to-bottom without edits.    |
| EDGAR data access (`read-edgar-filings`)     | 20      | Correctly looks up a company, lists 10-K filings, fetches the most recent one, and extracts at least three named sections (e.g., Business, Risk Factors, MD&A) into clean text.   |
| LLM API basics (free-form tasks)             | 20      | At least three tasks call the chat-completion API with no schema (e.g., summarization, plain-language explanation, sentiment narrative). Prompts are clear and roles are correct. |
| Structured output (JSON-schema tasks)        | 20      | At least two tasks use a JSON response format / structured schema, and the parsed responses are validated and used downstream (not just printed).                                 |
| Cost & model awareness                       | 10      | Notebook explicitly estimates token usage and cost for at least one task, and justifies the chosen model (e.g., "`gpt-5.4-mini` is sufficient because…").                         |
| Analytical interpretation                    | 15      | Each LLM output is followed by a short markdown interpretation explaining what the result means in business terms (not just a raw dump).                                          |
| Code quality, narrative, and reproducibility | 5       | Helpful comments, no dead code, clear section headings, and outputs that someone else could re-create from the notebook alone.                                                    |
| **Total**                                    | **100** |                                                                                                                                                                                   |

:::{tip} Going further

Once you have the basic pipeline working, try these extensions:

- Loop the same prompts over the last 5 years of 10-Ks for one company and chart how the _Risk Factors_ section changes.
- Compare two companies in the same industry by extracting the same fields from each 10-K and tabulating the differences.
- Try out multiple models through different providers and measure the cost/quality trade-off on the same eval set.

:::
