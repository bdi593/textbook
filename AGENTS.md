# AGENTS.md

This repository is a work-in-progress online textbook for **BDI 199/593: Advanced Analytics Applications in Business**. The content is organized around business analytics case studies for undergraduate and graduate learners.

:::{important} Primary authoring stack
This project uses **Jupyter Book v2** with **MyST Markdown**. When editing prose content, prefer valid MyST syntax and patterns that fit the existing book structure in `/home/runner/work/textbook/textbook/myst.yml`.
:::

## Repository structure

- `/home/runner/work/textbook/textbook/myst.yml` defines the book metadata and table of contents.
- `/home/runner/work/textbook/textbook/content/` contains the textbook chapters, case studies, notebooks, and supporting markdown pages.
- Most folders inside `content/` represent a **case study**.
- Case study folders typically include:
  - a case overview markdown file
  - one or more teaching notebooks (`.ipynb`)
  - optional supporting markdown files, images, or data assets

:::{tip} Case-study convention
For new case-study folders, include a clear overview page, preferably named `case-overview.md`, unless an existing folder already uses a different filename that is referenced in `myst.yml`.
:::

## Content authoring guidance

- Keep the **case study** as the central organizing unit.
- Write for advanced business analytics learners and connect methods to realistic business questions.
- Prefer clear section headings, short paragraphs, and instructional scaffolding.
- Use **MyST directives** to highlight teaching moments, caveats, and optional enrichment.

Named admonitions commonly used in this project include:

- `{note}`
- `{attention}`
- `{important}`
- `{caution}`
- `{hint}`
- `{warning}`
- `{seealso}`
- `{danger}`
- `{tip}`
- `{error}`

Example:

:::{tip} Teaching emphasis
Use admonitions to call out practical advice, conceptual reminders, warnings about mistakes, and links to related ideas.
:::

## Editing expectations

- Preserve existing paths referenced by `myst.yml`, or update `myst.yml` in the same change if files are renamed or added to the table of contents.
- Keep filenames, headings, and navigation consistent with the surrounding case-study materials.
- Prefer minimal, focused edits that align with the existing instructional style.
- When adding a new case study, add both:
  - the case-study folder content
  - the corresponding entry in `myst.yml`

:::{caution} Build note
The standard validation command is `jupyter-book build --html` from the repository root. In restricted environments, the build may fail if the MyST template API cannot be reached.
:::
