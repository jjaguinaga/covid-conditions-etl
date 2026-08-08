# COVID Conditions ETL Pipeline

---

## Overview

This project was built to further understand which health conditions were present at the time of someone's death who was diagnosed with COVID-19. This project pulls real CDC data, builds a clean and reliable database, and lets the numbers answer the question directly.

---

## Architecture Diagram

```
CDC SODA API
↓
Extract → Raw JSON → data/raw/
↓
Transform → Clean DF → Quarantine (bad rows)
↓
Load → Staging → Atomic Swap → PostgreSQL 
```

---

## Tech Stack 

| Tools | Purpose | Version |
|---|---|---|
| Python | Core logic | 3.11 |
| Pandas | Data manipulation | 2.2.3 |
| PostgreSQL | Database | 15 |
| psycopg2-binary | PostgreSQL driver | 2.9.12 |
| pytest | Testing | 9.1.1 |
| Docker | Containerization | 29.x |
| Docker Compose | Multi-container orchestration | 5.x |

---

## Project Structure 

```
covid-conditions-etl/
├── config/
│   └── settings.py
├── data/
│   ├── raw/
│   ├── processed/
│   ├── quarantine/
│   └── logs/
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── logger.py
├── tests/
│   └── test_transform.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── run_pipeline.py

```

## Key Features

| Feature | Description |
|---|---|
| **REST API ingestion** | CDC SODA API with filtered queries (Texas 2021) |
| **Environment-based config** | All settings via env vars, no hardcoded credentials |
| **Structured logging** | Timestamps, severity levels, module names to console + file |
| **Data validation** | Null checks, type conversion, aggregate row filtering |
| **Quarantine pattern** | Bad rows saved to CSV with rejection reason |
| **Bulk loading** | PostgreSQL COPY with CSV formatting for comma-containing fields |
| **Staging + atomic swap** | No partial data visible to queries |
| **Transaction safety** | Full rollback on any failure |
| **Docker containerization** | One command runs entire stack |
| **Automated testing** | pytest covering date parsing, numeric conversion, filtering |

---

## How to Run

### Local Development:
1. Install dependencies 
```bash
pip install -r requirements.txt
```
2. Set environment variables (or use defaults)
```bash 
export DB_PASSWORD=your_password
```
3. Run pipeline 
```bash
python run_pipeline.py
```

### Docker (recommended):
1. Start PostgreSQL + pipeline
```bash
docker compose up --build
```
2. Verify data loaded
```bash
docker compose exec postgres psql -U naga -d covid_table -c "SELECT COUNT(*) FROM covid_table;"
```

---

## Testing 

```bash
python -m pytest tests/ -v
```

---

## Results

- **1,814 rows** loaded to PostgreSQL after cleaning
- **877 rows quarantined**:
  - 299 rows: missing age group (`Not stated`)
  - 578 rows: missing death counts

  ---

## Data Source

[Conditions Contributing to COVID-19 Deaths, by State and Age, Provisional 2020-2023](https://data.cdc.gov/National-Center-for-Health-Statistics/Conditions-Contributing-to-COVID-19-Deaths-by-Stat/hk9y-quqm/about_data)
