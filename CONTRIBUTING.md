# Contributing to MEDIQ

Thank you for your interest in MEDIQ. This document explains how you can contribute to the project.

## What kind of contributions are accepted

MEDIQ is an **automated dataset** — the data flows directly from a live chatbot through a processing pipeline into this repository. Direct data contributions (submitting new question–answer pairs manually) are therefore not accepted. The dataset grows automatically.

What you *can* contribute to:

- **Data quality reports** — If you find entries that appear malformed, contain residual PII, or have clearly incorrect enrichment labels, please open an issue.
- **Schema and enrichment suggestions** — If you think a new field would make the dataset more useful for research, propose it as a feature request.
- **Documentation improvements** — Corrections or clarifications to the README, Data Dictionary, or Ethics statement are welcome via pull request.
- **Bug reports** — If the dataset schema breaks unexpectedly across releases, please open an issue.

## Reporting data quality issues

Use the **Data Quality Report** issue template. Please include:

1. The `messageId` of the affected entry (if known)
2. A description of the problem (e.g., "this entry appears to contain a phone number", "intent label seems wrong")
3. What the correct value should be, if you know it

We take PII reports seriously and will act on them promptly.

## Suggesting new enrichment fields

Use the **Feature Request** issue template. A good feature request includes:

1. The proposed field name and type
2. What values it can take (controlled vocabulary or free-form?)
3. Why this field would be useful for research
4. How it could be automatically generated (the pipeline must remain fully automated)

## Citing MEDIQ in research

If you use this dataset in a publication, please cite it using the BibTeX entry in the [README](README.md#citation) or the [CITATION.cff](CITATION.cff) file. Letting us know about publications that use MEDIQ is appreciated but not required — feel free to open an issue or reach out.

## Code of Conduct

All contributors are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Contact

For questions not suited to a GitHub issue, you can reach the maintainer via GitHub: [@ProxyAyush](https://github.com/ProxyAyush).
