# Ethics Statement

This document describes the ethical framework governing the collection, processing, and publication of the MEDIQ dataset.

---

## Data Source and Collection Context

MEDIQ is derived from interactions with an AI chatbot deployed at King George's Medical University (KGMU), Lucknow, India. The chatbot is a publicly accessible service provided through the university's digital infrastructure. It does not require user registration, login, or any form of identification to use.

The chatbot serves as an information resource for students, patients, hospital visitors, and staff seeking guidance on hospital services, academic programs, appointments, and related topics. Interactions are logged as part of normal system operation.

## Consent and Public-Service Nature

The chatbot is a public-facing service of a public institution. Users interact with it voluntarily to obtain information. The nature of the service is informational, not medical: the chatbot does not provide diagnoses, treatment plans, or clinical advice, and users are not in a patient–clinician relationship with the system.

Because no registration is required and the service is publicly accessible, individual consent for each interaction is not practical in the same way it would be for a clinical trial or a registered user database. The data is handled in accordance with the ethical norms applicable to publicly accessible digital services, including the principles of data minimization, purpose limitation, and anonymization.

## PII Removal Process

No personally identifiable information reaches the public dataset. The following categories of data are detected and removed or replaced during the private processing stage, before any data enters this repository:

- **Names**: Personal names detected via named-entity recognition and pattern matching
- **Phone numbers**: Indian and international phone number formats
- **Email addresses**: All email address patterns
- **National identifiers**: Aadhaar numbers and other national ID formats
- **Addresses**: Street addresses, pin codes used in personal context
- **Any other strings matching PII patterns**: Detected using a combination of regular expressions and model-based classifiers

When PII is detected in a query or answer, the affected entry is either dropped entirely or the PII string is replaced with a type-specific placeholder (e.g., `[PHONE_REDACTED]`).

Residual PII is possible despite these measures. If you identify an entry that appears to contain personal information, please report it immediately using the [Data Quality Report](.github/ISSUE_TEMPLATE/data-quality.md) issue template.

## Session Anonymization

Session identifiers from the original system are replaced with cryptographic hashes (SHA-256, truncated). The mapping between original session IDs and hashed identifiers is not stored in this repository or in any publicly accessible location. Users cannot be re-identified from session identifiers in this dataset.

## Timestamp Handling

Timestamps are retained at minute-level precision. Sub-minute timing data (seconds, milliseconds) is discarded. This limits the possibility of using timing patterns to infer user behavior or identity.

## Compliance with the Digital Personal Data Protection Act 2023 (DPDP Act)

India's Digital Personal Data Protection Act 2023 governs the processing of personal data of individuals in India. MEDIQ is designed to be compliant with this legislation:

- The dataset does not contain personal data as defined by the DPDP Act after the PII removal process described above.
- The data is processed for a legitimate, documented purpose: advancing research in natural language processing, healthcare informatics, and multilingual AI.
- Data minimization principles are applied: only the question, answer, timestamp, and anonymized session identifier from the original interaction are retained; no other metadata is collected.

## Intended Uses

MEDIQ is intended to support:

- Natural language processing research, particularly for low-resource and code-mixed language settings
- Research on medical question answering and health information retrieval
- Studies of user behavior in healthcare information systems
- Development and evaluation of multilingual AI systems
- Benchmarking of intent classification, language detection, and sentiment analysis models in the medical domain

## Misuse and Out-of-Scope Uses

The following uses are explicitly outside the intended scope and are discouraged:

- **Re-identification attempts**: Any attempt to identify individuals from the dataset
- **Clinical decision support without validation**: Using the dataset to build or validate clinical decision-making tools without appropriate clinical oversight and validation
- **Training systems to provide medical advice**: The chatbot responses in this dataset are informational and institution-specific; they are not a source of validated medical knowledge
- **Generating synthetic PII**: Using the dataset to train models that generate realistic personal information

## Limitations of the Dataset

Users should be aware of the following limitations before using MEDIQ in research:

1. **Geographic and institutional specificity**: The data originates from a single institution in Lucknow, India. Query patterns, topics, and language use may not generalize to other medical institutions, regions, or healthcare systems.

2. **Chatbot response quality**: Answers are generated by the deployed chatbot, which is not infallible. The `answer_quality` field provides an automated quality signal, but it is itself model-generated and imperfect.

3. **AI annotation noise**: All enriched fields (language labels, intent classes, sentiment, etc.) are model-generated and carry inherent error rates. They should not be treated as ground truth for evaluation purposes without independent validation.

4. **Temporal drift**: The dataset grows continuously. Query distributions, intents, and language patterns may shift over time as the chatbot's user base and the institution's services evolve.

5. **Underrepresentation of some user types**: Users who are less comfortable with digital interfaces may be underrepresented. The dataset reflects the population that chose to use the chatbot, not the full population of the institution.

6. **Language detection challenges**: Code-mixed and Romanized Hindi text is difficult to classify reliably. The `corrected_language` field mitigates some systematic errors, but ambiguous cases remain.

---

Questions about this ethics statement can be directed to the maintainer via GitHub: [@ProxyAyush](https://github.com/ProxyAyush).
