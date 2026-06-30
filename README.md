# Candidate Fusion Engine



## Overview

Candidate Fusion Engine is an intelligent identity resolution system that consolidates candidate information from multiple heterogeneous data sources into a single canonical profile.

The system ingests recruiter CSV records, resumes, and recruiter notes, identifies duplicate candidates using identity resolution, merges the information using configurable source priorities, tracks provenance for every extracted field, validates the final profile, and provides runtime JSON projections through an interactive Streamlit dashboard.

---

# Features

- Multi-source candidate ingestion
  - Recruiter CSV
  - Resume PDFs
  - Recruiter Notes

- Resume Information Extraction
  - Name
  - Email
  - Phone
  - Headline
  - Skills
  - Experience
  - Education
  - Location
  - LinkedIn
  - GitHub

- Identity Resolution
  - Email Matching
  - Phone Matching
  - Name Similarity

- Candidate Profile Fusion
  - Automatic duplicate detection
  - Field-level merge strategy
  - Source priority handling

- Data Normalization
  - Email normalization
  - Phone normalization
  - Skill normalization

- Confidence Scoring

- Provenance Tracking

- Validation Engine

- Runtime JSON Projection

- Interactive Streamlit Dashboard

---

# Architecture

```
                     +-------------------+
                     | Recruiter CSV     |
                     +---------+---------+
                               |
                               |
                     +---------v---------+
                     | Resume PDFs       |
                     +---------+---------+
                               |
                               |
                     +---------v---------+
                     | Recruiter Notes   |
                     +---------+---------+
                               |
                               |
                   +-----------v------------+
                   | Data Parsers           |
                   +-----------+------------+
                               |
                   +-----------v------------+
                   | Candidate Registry     |
                   +-----------+------------+
                               |
                   +-----------v------------+
                   | Identity Resolution    |
                   +-----------+------------+
                               |
                   +-----------v------------+
                   | Candidate Merge Engine |
                   +-----------+------------+
                               |
              +----------------+----------------+
              |                                 |
      +-------v--------+               +--------v-------+
      | Normalization  |               | Confidence     |
      +-------+--------+               +--------+-------+
              |                                 |
              +----------------+----------------+
                               |
                    +----------v-----------+
                    | Provenance Tracking  |
                    +----------+-----------+
                               |
                    +----------v-----------+
                    | Validation Engine    |
                    +----------+-----------+
                               |
                    +----------v-----------+
                    | Canonical JSON       |
                    +----------+-----------+
                               |
                    +----------v-----------+
                    | Streamlit Dashboard  |
                    +----------------------+
```

---

# Project Structure

```
Candidate-Fusion-Engine/
│
├── confidence/
├── identity/
├── input/
│   ├── recruiter.csv
│   ├── resumes/
│   └── notes/
│
├── models/
├── normalizers/
├── parsers/
├── projection/
├── registry/
├── utils/
├── validation/
│
├── output/
│
├── main.py
├── streamlit_app.py
├── requirements.txt
└── README.md
```

---

# Identity Resolution Strategy

Candidates are matched using multiple identity signals.

Priority order:

1. Phone Number
2. Email Address
3. Name Similarity

Duplicate candidates are automatically merged into a single canonical profile.

---

# Candidate Merge Strategy

For duplicate profiles:

- Emails are merged and deduplicated
- Phones are merged and deduplicated
- Skills are merged
- Experience is merged
- Education is merged
- Location is enriched
- Headline is selected based on source priority

Source Priority:

| Source | Priority |
|----------|----------|
| Resume | High |
| CSV | Medium |
| Recruiter Notes | Low |

---

# Confidence Scoring

Each extracted field receives a confidence score based on its extraction source.

Example:

| Source | Confidence |
|----------|------------|
| CSV | 0.99 |
| Resume Extraction | 0.95 |
| Notes | 0.90 |

An overall confidence score is generated for every candidate profile.

---

# Provenance Tracking

Every extracted field stores its origin.

Example:

```json
{
  "field": "email",
  "value": "candidate@gmail.com",
  "source": "Resume",
  "method": "Regex Extraction",
  "confidence": 0.95
}
```

This ensures complete traceability of all extracted information.

---

# Validation

The validation engine verifies:

- Required fields
- Missing values
- Invalid projections
- Schema consistency

Each profile includes a validation report.

---

# Runtime Projection

The projection engine dynamically transforms canonical profiles into different output schemas without modifying backend logic.

Supported templates include:

- Minimal Profile
- HR System
- Strict Validation

Custom runtime configurations can also be applied through the Streamlit interface.

---

# Streamlit Dashboard

The dashboard provides:

- Candidate Overview
- Skills
- Experience
- Education
- Identity Resolution
- Merge Decisions
- Provenance Tracking
- Recruiter CSV Viewer
- Resume Browser
- Recruiter Notes
- Runtime Projection
- JSON Download

---

# Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/Candidate-Fusion-Engine.git

cd Candidate-Fusion-Engine
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

Generate canonical profiles

```bash
python main.py
```

Launch the dashboard

```bash
streamlit run streamlit_app.py
```

---

# Input Sources

The project accepts:

```
input/
│
├── recruiter.csv
├── resumes/
│      *.pdf
└── notes/
       *.txt
```

---

# Output

The system generates:

```
output/
    canonical_profiles.json
```

Each profile contains:

- Candidate Information
- Skills
- Experience
- Education
- Confidence Score
- Provenance
- Validation
- Merge Decisions

---

# Technologies Used

- Python 3.11
- OpenAI API (LLM-powered Resume Extraction)
- Streamlit
- Pandas
- PDF Parsing
- Regular Expressions (Regex)
- JSON
- Dataclasses
- Object-Oriented Programming (OOP)

---

# Future Enhancements

- OCR Support for Scanned Resumes
- Named Entity Recognition (NER)
- Large Language Model Resume Parsing
- Elasticsearch Integration
- Candidate Ranking
- Semantic Skill Matching
- REST API Support
- PostgreSQL Storage
- Docker Deployment

---

## 🚀 Live Demo

**Streamlit App**

https://candidate-fusion-engine-hwvkvqfrsrecxi2uwaqjjp.streamlit.app/

Explore the Candidate Fusion Engine through the interactive Streamlit dashboard.

---

# Author

**Poojashri D**

Software Developer | AI & Software Engineering Enthusiast

GitHub: https://github.com/Poojashri24

LinkedIn: https://www.linkedin.com/in/poojashri-d-a36449290
