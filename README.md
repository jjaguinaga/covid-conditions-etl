# COVID Conditions ETL - Conditions Related To COVID-19 Deaths

**An end-to-end ETL pipeline analyzing COVID-19 deaths and their conditions grouped by age group and condition, using CDC public health data.**

---

## Motivation

This project was built to further understand which health conditions were present at the time of someone's death who was diagnosed with COVID-19. This project pulls real CDC data, builds a clean and reliable database, and lets the numbers answer the question directly.

---

## What This Project Does

This pipeline extracts CDC data conditions contributing to COVID-19 deaths, broken down by age group and only for the state of Texas in 2021. It cleans and validates the data, stores it in a relational database, and produces SQL views that allow analysts to explore the relationship between conditions and deaths.
---

## Key Findings 

**Older people were most affected from COVID-19 in all age groups.** The 'age_group_most_deaths' view shows that as you get older you were more likely to die from COVID-19 with underlying condtions. This view is set up as a percentage of the population to better understand how many deaths there were in each age group.

**COVID-19 and the respiratory system**The 'total_deaths_by_condition' view shows that Respiratory diseases remained the top condition contributing to a COVID-19 death. This makes sense since COVID-19 attacked the lungs when someone tested positive for it. 

---

## Architecture

```
CDC SODA API
↓
extract.py → MongoDB (raw data storage)
↓
transform.py → Pandas (data cleaning & validation)
↓
load.py → PostgreSQL (data warehouse)
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline logic |
| Pandas | Data cleaning and transformation |
| MongoDB | Raw data storage |
| PostgreSQL | Data warehouse |
| CDC Public API | Data source |
| Requests | API calls |
|Psycopg2 | PostgreSQL connection |

---

## Project Structure

```
covid-conditions-etl/
├── extract.py
├── transform.py
├── load.py
├── README.md
├── analytics.sql
└── requirements.txt
```
---

## How to Run

1. Clone the repo
2. Install dependencies:
```bash
   pip install pandas pymongo sqlalchemy psycopg2-binary requests
```
3. Make sure MongoDB and PostgreSQL are running locally
4. Create the PostgreSQL database:
```sql
   CREATE DATABASE tx_covid_2021;
```
5. Run extract then load:
```bash
   python3 extract.py
   python3 load.py
```

---

## Data Source
[Conditions Contributing to COVID-19 Deaths, by State and Age, Provisional 2020-2023](https://data.cdc.gov/National-Center-for-Health-Statistics/Conditions-Contributing-to-COVID-19-Deaths-by-Stat/hk9y-quqm/about_data)