# Natural Language Processing

## What is Natural Language Processing (NLP)?

Natural Language Processing (NLP) is a field within artificial intelligence and data science focused on enabling computers to understand, interpret, and generate human language. Unlike structured numerical data, natural language data (such as emails, customer reviews, social media posts, or transcripts) is inherently ambiguous and unstructured. NLP techniques allow analysts to transform text into structured information that can be analyzed using computational methods.

NLP sits at the intersection of several disciplines:

- **Computer Science**: algorithms and software systems
- **Linguistics**: the structure and meaning of language
- **Machine Learning**: statistical models that learn patterns from data
- **Statistics and Data Science**: analyzing and modeling language data

Organizations increasingly rely on NLP to extract insights from large volumes of textual data. Common applications include:

- Sentiment analysis of customer reviews
- Topic discovery in large document collections
- Chatbots and virtual assistants
- Automatic document summarization
- Language translation
- Information extraction from reports or news

In business analytics, NLP allows organizations to incorporate unstructured text data into decision-making processes.

## Business Context

Every quarter, public companies hold **earnings conference calls** in which
executives discuss results, strategy, and risks. Investors, journalists, and
competitors read the transcripts closely. Inside companies the situation is
similar: expense reports, customer reviews, and employee surveys hold
valuable information in free text that nobody has time to read in full. This
chapter shows how analysts turn such text into numbers and labels a business
can act on.

:::{note} What "Conference Calls" means in this chapter

The chapter is named after earnings conference calls, but it does not
analyze a collection of call transcripts. The Preprocessing notebook uses a
short excerpt from one Microsoft earnings call, and the finance demo in NLP
in Business scores a handful of made-up earnings-call statements. The other
demos use synthetic expense, review, and HR text. For an analysis of real
company disclosures, see the
[Financial Data Analysis with LLMs](../financial-data-with-llms/case-overview.md)
case study, which works with 10-K filings.

:::

## Learning Objectives

By the end of this chapter you should be able to:

1. Explain what NLP is and how rule-based, statistical, and deep-learning
   approaches differ.
2. Clean text with spaCy: sentence segmentation, tokenization, lowercasing,
   removing stopwords, punctuation, and whitespace, and lemmatization.
3. Extract part-of-speech tags and named entities, and check entity output
   for the errors a small pretrained model makes.
4. Score the tone of financial statements with a domain lexicon.
5. Map free-text expense descriptions to categories with TF-IDF and cosine
   similarity, and route low-confidence matches to a reviewer.
6. Discover themes in customer reviews with NMF topic modelling, and check
   for reviews the vocabulary cannot place.
7. Train a TF-IDF + Naive Bayes text classifier and evaluate it with
   cross-validation against a baseline.

## Data

All text in this chapter is small and defined inside the notebooks, so
nothing needs to be downloaded.

| Notebook        | Text                                                                                                         | Origin                         |
| --------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------ |
| NLP in Business | 6 earnings-call statements, 8 expense descriptions, 24 app reviews, 48 labeled employee comments (plus 5 new ones to route) | Synthetic examples             |
| Preprocessing   | One paragraph from Microsoft's earnings call for the second quarter of fiscal year 2026 (28 January 2026)     | Official transcript (quoted)   |

### Source and licence

The finance, accounting, marketing, and HR examples are synthetic. The
finance demo's word lists are a tiny illustrative subset in the style of the
[Loughran–McDonald Master Dictionary](https://sraf.nd.edu/loughranmcdonald-master-dictionary/).
The earnings-call excerpt is quoted from the official transcript of
Microsoft's earnings conference call for the second quarter of fiscal year
2026, linked from
[Microsoft's investor relations page for that call](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2).
Check the source pages for terms of use.

## Notebooks in This Case Study

| Notebook                                       | What it covers                                                                                                                                                                                                                                 |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [NLP in Business](./nlp-in-business.ipynb)     | Four short demos on synthetic text: lexicon-based tone scoring of earnings-call statements (finance), TF-IDF similarity for expense categorisation (accounting), NMF topic modelling of app reviews (marketing), and a Naive Bayes classifier for employee feedback evaluated with cross-validation (HR). |
| [NLP Preprocessing](./preprocessing.ipynb)     | spaCy preprocessing of a Microsoft earnings-call excerpt: sentences, tokens, token attributes, lowercasing, stopword, punctuation, and whitespace removal, lemmatization, part-of-speech tags, and named entities, including the mistakes a small model makes. |

The two notebooks can be read in either order. Preprocessing covers the
cleaning steps in detail; NLP in Business shows what businesses do with the
cleaned text.

## Setup

Install the packages used across the book from the root of the repository:

```bash
python -m pip install -r requirements.txt
```

The environment includes scikit-learn, Plotly, spaCy, and spaCy's small
English model `en_core_web_sm`, so no separate model download is needed.
Both notebooks run offline once the environment is installed.

## Brief History of NLP

The development of NLP has progressed through several major stages, each characterized by different approaches and technologies.

### Early Rule-Based Systems (1950s–1980s)

The earliest NLP systems relied heavily on manually constructed rules and linguistic knowledge.

Early efforts included:

- **Machine Translation Experiments (1950s)**: Researchers attempted to translate Russian to English using dictionaries and grammatical rules.
- **ELIZA (1966)**: One of the earliest chatbots, ELIZA simulated conversation using simple pattern-matching rules.

These systems relied on explicit linguistic rules such as:

- Grammar rules
- Dictionaries
- Pattern-matching templates

Rule-based approaches struggled with ambiguity, idioms, and the broader complexity of natural language.

---

### Statistical NLP (1990s–2010)

In the 1990s, NLP shifted toward statistical methods driven by increasing computational power and the availability of large digital text corpora. Instead of manually defining linguistic rules, statistical NLP models learned patterns from data.

Important developments included:

- N-gram language models
- Hidden Markov Models (HMMs) for part-of-speech tagging
- Probabilistic parsing
- Machine learning classifiers for tasks such as sentiment analysis

During this period, many of the foundational NLP tools and datasets that are still used today were developed.

---

### Deep Learning Era (2010–Present)

Around 2010, deep learning transformed NLP by enabling models to learn complex semantic patterns directly from text.

Key innovations included:

- **Word embeddings (Word2Vec, GloVe)**: Words represented as vectors capturing semantic relationships.
- **Recurrent Neural Networks (RNNs)**: Models capable of processing sequences of words.
- **Transformers (2017)**: A neural architecture introduced in the paper _Attention is All You Need_, which dramatically improved language modeling performance.

Transformers enabled modern language models such as:

- BERT
- GPT
- T5
- LLaMA

These models power many modern NLP applications, including chatbots, summarization systems, and search engines.

## Common NLP Preprocessing Steps

Before applying NLP models, raw text typically undergoes several preprocessing steps. These steps transform text into a format suitable for computational analysis.

```{mermaid}
flowchart TD

A[Raw Text] --> B[Text Normalization]
B --> C[Tokenization]
C --> D[Stop Word Removal]
D --> E[Stemming / Lemmatization]
E --> F[Feature Extraction]

F --> F1[Bag of Words]
F --> F2[TF-IDF]
F --> F3[Embeddings]

F --> G[NLP Model]
```

### Tokenization

Tokenization splits text into smaller units called tokens, typically words or subwords.

Example:

> Text: `"Data science is transforming business."`\
> Tokens: `["Data", "science", "is", "transforming", "business"]`

Tokenization is a fundamental step in most NLP pipelines.

---

### Lowercasing

Converting all text to lowercase helps standardize the text and reduce redundancy.

Example: `"Apple"` and `"apple"` → treated as the same word.

---

### Stop Word Removal

Stop words are very common words that often carry little semantic meaning.

Examples: `the`, `is`, `and`, `of`, `to`.

Removing them can reduce noise in some analyses, although modern transformer-based models usually do **not** require stop word removal.

---

### Stemming

Stemming reduces words to their root form by removing suffixes.

Examples:

- `running` → `run`
- `connected` → `connect`

However, stemming sometimes produces non-dictionary forms (e.g., `studies` → `studi`).

---

### Lemmatization

Lemmatization also reduces words to their base form, but does so using linguistic knowledge.

Examples:

- `better` → `good`
- `running` → `run`

Lemmatization generally produces more accurate results than stemming.

---

### Vectorization

Machine learning models cannot directly process text, so words must be converted into numerical representations. The three most common families of representations are described below.

#### Bag-of-Words (BoW)

Represents a document by counting word occurrences.

Example representation:

| Word     | Count |
| -------- | ----- |
| data     | 2     |
| analysis | 1     |
| model    | 1     |

#### TF-IDF (Term Frequency–Inverse Document Frequency)

TF-IDF adjusts word counts by weighting words that appear frequently in a document but rarely across all documents. This helps highlight words that distinguish a document from the rest of the corpus.

#### Word Embeddings

Modern approaches represent words as dense vectors that capture semantic meaning.

Example:

> `king - man + woman ≈ queen`

These embeddings enable models to capture relationships between words.

## Rule-Based Algorithms vs. Modern Machine Learning Approaches

NLP systems historically relied on rule-based methods, but modern approaches increasingly use machine learning and deep learning.

---

### Rule-Based Systems

Rule-based NLP systems use manually defined linguistic rules.

Example rules:

- If a sentence contains `"not good"`, classify it as negative sentiment.
- If a phrase matches a specific pattern, extract a named entity.

**Advantages:**

- Transparent and interpretable
- Require little training data
- Easy to control behavior

**Limitations:**

- Hard to scale
- Difficult to maintain
- Cannot easily handle linguistic ambiguity

---

### Traditional Machine Learning Methods

Statistical machine learning methods improved upon rule-based approaches by learning patterns from labeled data.

Common algorithms include:

- Naive Bayes
- Logistic regression
- Support Vector Machines (SVM)
- Decision trees

These models often use features derived from text, such as TF-IDF vectors or n-gram frequencies. They perform well for many classification tasks but often struggle with deeper language understanding.

---

### Deep Learning Methods

Deep learning models learn complex representations of language directly from data.

Examples include:

- Recurrent Neural Networks (RNNs)
- Long Short-Term Memory networks (LSTMs)
- Transformers

These models can capture context, semantics, and long-range relationships between words.

---

## Hugging Face and the Transformer Ecosystem

[Hugging Face](https://huggingface.co/) is an open-source platform that provides tools and models for modern NLP applications.

The Hugging Face ecosystem includes:

- Pretrained models
- Datasets
- Tokenizers
- Training pipelines

The most widely used library is [`transformers`](https://huggingface.co/docs/transformers).

Example using a pretrained sentiment analysis model:

:::{note} Not part of the course environment

`transformers` is not in `requirements.txt`, and the first call to
`pipeline` downloads a pretrained model. Install `transformers` separately
if you want to try this example. The notebooks in this chapter do not need
it.

:::

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("I love learning about natural language processing.")
print(result)
```

The output looks like this:

```
[{'label': 'POSITIVE', 'score': 0.999}]
```

**Advantages of Hugging Face:**

- Access to thousands of pretrained models
- Easy integration with PyTorch or TensorFlow
- Rapid prototyping of NLP systems

Many organizations use Hugging Face to build production NLP pipelines.

---

### Large Language Models (LLMs) and NLP

Large Language Models (LLMs) represent the latest major advancement in NLP.

Examples include:

- GPT models
- LLaMA
- Claude

These models are trained on massive datasets containing billions or trillions of tokens.

---

### How LLMs Work

Most LLMs are based on the transformer architecture, which uses an **attention mechanism** to model relationships between words in a sequence. The model learns statistical patterns in language and can then generate coherent text.

Capabilities include:

- Text generation
- Question answering
- Summarization
- Translation
- Code generation

:::{tip} Where to go next

The **NLP in Business** notebook walks through short demos of NLP in
finance, accounting, marketing, and HR. The **Preprocessing** notebook
applies the cleaning steps described on this page to a short earnings-call
excerpt.

:::
