#  NSW FuelCheck Data Analytics Pipeline

An end-to-end data engineering and analytics project built on the **NSW Government FuelCheck** dataset (January 2025), combining geospatial enrichment, multi-level price aggregation, and data visualisation to uncover fuel pricing trends across New South Wales.

> **Course:** COMP9321 – Data Services Engineering | UNSW Sydney

---

##  Project Overview

This pipeline ingests, cleans, enriches, and analyses over 60,000 real-world fuel price records from NSW service stations. It answers two research questions using data-driven visualisations:

1. **Is it cheaper to patron independent or franchised service stations?**
2. **Are consumers in certain regions of NSW being unfairly charged for fuel?**

---

##  Dataset

| File | Source | Description |
|---|---|---|
| `fuel.csv` | NSW Government FuelCheck | 60,151 fuel price records for Jan 2025 |
| `postcodes.json` | GitHub – Elkfox | 16,875 Australian postcodes with lat/long |

---

##  Pipeline Stages

### Part 1 – Data Ingestion & Cleaning
- **Q1:** Loaded `fuel.csv` with malformed row handling using `on_bad_lines` lambda and strict dtype mapping → **(60,151 × 8)**
- **Q2:** Renamed columns, standardised suburb casing, filtered non-NSW addresses → **(59,256 × 8)**
- **Q3:** Loaded `postcodes.json`, dropped `accuracy` column → **(16,875 × 6)**
- **Q4:** Geo-enriched fuel data via two-pass merge (Postcode + Suburb first, then Postcode-only fallback with alphabetical suburb tie-breaking) → **(59,256 × 10)**, exported as `df4.csv`

### Part 2 – Data Exploration
- **Q5:** Built a **3-level hierarchical average price** (Station → Postcode → Duration) with a MultiIndex DataFrame of Postcode × FuelType → **(4,048 × 1)**

### Part 3 – Data Manipulation
- **Q6:** Calculated `PriceChangeAverage` — percentage deviation of each reading from the postcode-level average (from Q5) → **(59,256 × 11)**
- **Q7:** Calculated `PriceChangePrevious` — raw price change from the immediately preceding reading per station and fuel type using `groupby.diff()` → **(59,256 × 12)**

### Part 4 – Data Visualisation
- **Q8:** Grouped bar chart comparing cheapest franchise brands vs. independent stores per fuel type, with fuel-coded colour scheme
- **Q9:** Grouped bar chart comparing average fuel prices across 15 NSW regions (Sydney, Hunter Valley, Riverina, Far West, etc.)

---

## Key Insights

**Independent vs. Franchise (Q8):**  
Franchised brands consistently undercut independent stations for most fuel types. Speedway leads for DL, P95, and E85; Costco for E10 and P98; Metro Fuel for LPG — showing that brand specialisation, not independence, drives the lowest prices.

**Regional Pricing Fairness (Q9):**  
Most fuel types vary by only 5–8 cents/litre across NSW regions, suggesting broad pricing fairness. The notable exception is **LPG**, which ranges from ~108 c/L in Sydney to ~140 c/L in Richmond–Tweed — a 30% regional disparity.

---

## Tech Stack

| Tool | Usage |
|---|---|
| Python 3.11 | Core language |
| pandas | All data processing, merging, aggregation |
| matplotlib / numpy | Visualisation |


---

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/nsw-fuelcheck-analytics

# 2. Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Place fuel.csv and postcodes.json in the project root

# 4. Run the pipeline
python z1234567.py
```

**Outputs:**
- `df4.csv` — Geo-enriched fuel dataset
- `z1234567-Q8.png` — Independent vs. Franchise visualisation
- `z1234567-Q9.png` — Regional pricing visualisation

---


