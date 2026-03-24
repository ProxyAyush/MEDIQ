# MEDIQ — Medical Inquiry Dataset

<!-- TODO: update with actual logo image -->
<!-- ![MEDIQ Logo](assets/mediq-logo.png) -->

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.placeholder.svg)](https://doi.org/10.5281/zenodo.placeholder)
<!-- TODO: update Zenodo DOI badge once first release is archived -->
![Dataset Size](https://img.shields.io/badge/entries-growing-blue)
<!-- TODO: replace with dynamic badge or actual count -->
![Last Updated](https://img.shields.io/badge/updated-daily-green)

---

## Overview

MEDIQ is a continuously growing, bilingual (Hindi–English) medical question-answering dataset collected from a real-world AI chatbot deployed at King George's Medical University (KGMU), Lucknow, India. The chatbot serves a diverse population — medical students, patients, hospital visitors, and administrative staff — fielding questions about medical education, hospital services, appointments, admissions, and university operations.

Unlike benchmark datasets constructed from textbooks or curated corpora, MEDIQ captures organic, spontaneous interactions in a live clinical-institutional setting. This makes it particularly valuable for studying how non-expert users phrase medical and health-system queries in a low-resource, code-mixed language environment. The dataset contains both standard English queries and Hindi queries written in Devanagari script as well as Romanized Hindi (transliterated into Latin characters), reflecting actual user behavior.

The dataset is automatically enriched with AI-generated metadata — including detected language, query intent, medical relevance scores, sentiment, answer quality assessments, and topic tags — before being published here. Quarterly snapshots are archived on Zenodo with permanent DOIs, enabling reproducible research. The full pipeline runs daily with no manual curation step, ensuring the dataset reflects current, real-world usage patterns.

---

## Key Features

- **Bilingual**: Hindi (Devanagari and Romanized) and English queries in a single dataset
- **Real-world sourcing**: Collected from live chatbot interactions at a major Indian medical university
- **Continuously growing**: New entries are appended and published daily
- **AI-enriched metadata**: Each entry is annotated with language detection, intent classification, sentiment, medical relevance, answer quality, and more
- **Romanized Hindi detection**: Explicitly flags queries written in Latin-script Hindi (code-mixed or transliterated), a common pattern in Indian digital communication
- **Zero PII**: All personally identifiable information is removed before publication; compliant with India's Digital Personal Data Protection (DPDP) Act 2023
- **Diverse query types**: Covers clinical queries, administrative questions, appointment requests, educational inquiries, and general hospital navigation
- **Structured schema**: Consistent fields across all entries with well-defined types and controlled vocabularies where applicable
- **Open license**: CC-BY-4.0 — free to use, share, and build upon with attribution

---

## Dataset Schema

### Original Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `question` | string | The user's query as submitted to the chatbot | `"What are OPD timings?"` |
| `answer` | string | The chatbot's response to the query | `"OPD runs Monday–Saturday, 8 AM to 2 PM."` |
| `timestamp` | ISO 8601 datetime | When the interaction occurred (UTC) | `"2024-11-15T09:32:11Z"` |
| `sessionId` | string (hashed) | Anonymized session identifier; consistent within a session, not linkable to a user | `"sess_a3f9c..."` |
| `messageId` | string | Unique identifier for the message | `"msg_00123"` |

### AI-Enriched Fields

| Field | Type | Possible Values / Format | Description |
|-------|------|--------------------------|-------------|
| `detected_language` | string | `en`, `hi`, `hi-Latn`, `mixed` | Language of the user's query as detected by the AI enrichment model |
| `corrected_language` | string | Same as `detected_language` | Post-heuristic correction; accounts for misclassifications of Romanized Hindi |
| `intent` | string | See [Data Dictionary](DATA_DICTIONARY.md) | Classified intent category of the query |
| `medical_relevance` | float | 0.0–1.0 | Estimated relevance of the query to medical or clinical topics |
| `sentiment` | string | `positive`, `neutral`, `negative` | Sentiment of the user's query |
| `answer_quality` | string | `high`, `medium`, `low`, `uncertain` | AI assessment of the chatbot response quality |
| `topic_tags` | list[string] | Free tags | Subject tags assigned to the query (e.g., `["OPD", "timing", "outpatient"]`) |
| `user_type` | string | `student`, `patient`, `visitor`, `staff`, `unknown` | Inferred type of user based on query context |
| `english_translation` | string or null | Free text | English translation of the query if it was in Hindi; null for English queries |
| `is_followup` | boolean | `true`, `false` | Whether the query appears to be a follow-up within the same session |

For detailed field descriptions, edge cases, and controlled vocabulary, see [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

---

## Quick Start

### Python (pandas)

```python
import pandas as pd

# Load the latest full dataset
df = pd.read_json(
    "https://raw.githubusercontent.com/proxyayush/mediq/main/data/mediq_latest.jsonl",
    lines=True
)

# Basic exploration
print(f"Total entries: {len(df)}")
print(f"Language distribution:\n{df['detected_language'].value_counts()}")
print(f"Top intents:\n{df['intent'].value_counts().head(10)}")

# Filter to high-quality English entries
english_hq = df[
    (df["detected_language"] == "en") &
    (df["answer_quality"] == "high")
]
```

### Node.js

```javascript
import { createReadStream } from "fs";
import { createInterface } from "readline";

// Stream and parse a JSONL file
const rl = createInterface({
  input: createReadStream("mediq_latest.jsonl"),
  crlfDelay: Infinity,
});

const entries = [];
for await (const line of rl) {
  if (line.trim()) entries.push(JSON.parse(line));
}

console.log(`Loaded ${entries.length} entries`);

// Filter Hindi queries
const hindiEntries = entries.filter(
  (e) => e.detected_language === "hi" || e.detected_language === "hi-Latn"
);
console.log(`Hindi entries: ${hindiEntries.length}`);
```

---

## Statistics

<!-- TODO: update these values with each quarterly release or via automated script -->

| Metric | Value |
|--------|-------|
| Total entries | — |
| Date range | — |
| Languages | Hindi (Devanagari), Romanized Hindi, English, Mixed |
| Top intent categories | — |
| Median answer length (tokens) | — |
| Sessions | — |

*Statistics are updated with each quarterly Zenodo release. For the live count, see the dataset files directly.*

---

## Data Pipeline

MEDIQ is produced by a three-stage automated pipeline:

```
Firebase (live chatbot logs)
        |
        v
Private processing repository
  - Deduplication
  - PII scrubbing
  - Normalization
        |
        v
AI enrichment (Groq API — Kimi K2 model)
  - Language detection & correction
  - Intent classification
  - Sentiment analysis
  - Medical relevance scoring
  - Answer quality assessment
  - Topic tagging
  - Translation (Hindi to English)
  - Follow-up detection
        |
        v
Public release (this repository)
  - JSONL append to data/
  - Quarterly Zenodo archive
```

The processing and enrichment code lives in a private repository. Only the final, anonymized, enriched data is published here. The pipeline runs daily via automated scheduling.

---

## AI Enrichment Details

All enrichment is performed using the **Kimi K2** model accessed via the **Groq API**. The model receives each question–answer pair and returns structured JSON with the enriched fields listed in the schema above.

| Enriched Field | How it is produced |
|----------------|--------------------|
| `detected_language` | Model classifies the script and language of the query |
| `corrected_language` | A heuristic post-pass corrects common misclassifications (e.g., Romanized Hindi misidentified as English) |
| `intent` | Multi-class classification into predefined intent categories (see Data Dictionary) |
| `medical_relevance` | A 0–1 float representing how clinically or medically relevant the query is |
| `sentiment` | Three-way sentiment classification of the query text |
| `answer_quality` | The model assesses whether the chatbot's answer is complete, accurate, and appropriate |
| `topic_tags` | Free-form tags capturing subjects mentioned in the query |
| `user_type` | Inferred from lexical and contextual cues in the query |
| `english_translation` | Produced for non-English queries; null otherwise |
| `is_followup` | Detected by comparing the query to previous messages in the same session |

Enrichment is not guaranteed to be error-free. Users should treat AI-generated fields as noisy annotations rather than ground truth. See [ETHICS.md](ETHICS.md) for further discussion of limitations.

---

## Ethics & Privacy

MEDIQ is derived from interactions with a publicly accessible chatbot at a public university. No user login or registration was required to use the chatbot. The following measures are applied before any data reaches this repository:

- **PII removal**: Names, phone numbers, email addresses, national ID numbers, and other identifiable strings are detected and removed using a combination of regex patterns and model-based detection.
- **Session anonymization**: Session IDs are cryptographically hashed and are not reversible to any user identity.
- **Timestamp rounding**: Timestamps are retained at minute-level precision; sub-minute timing is discarded.
- **DPDP Act 2023 compliance**: The dataset does not contain personal data as defined under India's Digital Personal Data Protection Act 2023.

For a full ethics statement including intended uses, limitations, and misuse prevention, see [ETHICS.md](ETHICS.md).

---

## Citation

If you use MEDIQ in your research, please cite:

```bibtex
@dataset{yadav2025mediq,
  author    = {Yadav, Ayush},
  title     = {{MEDIQ}: A Bilingual Medical Question-Answering Dataset from a Real-World Clinical-Institutional Chatbot},
  year      = {2025},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.placeholder},
  url       = {https://github.com/proxyayush/mediq},
  license   = {CC-BY-4.0}
}
```
<!-- TODO: update DOI once first Zenodo release is published -->

A machine-readable citation is also available in [CITATION.cff](CITATION.cff).

---

## License

- **Dataset** (all files under `data/`): [Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE)
- **Code and scripts**: [MIT License](LICENSE-CODE)

You are free to use, share, and adapt the dataset for any purpose, including commercial use, provided you give appropriate credit. See [LICENSE](LICENSE) for the full text.

---

## Acknowledgments

The data underlying MEDIQ originates from the AI chatbot deployed at **King George's Medical University (KGMU), Lucknow, India**. We thank the institution for providing the deployment environment that makes this dataset possible.

AI enrichment is powered by the **Kimi K2** model via the **Groq** inference API.
