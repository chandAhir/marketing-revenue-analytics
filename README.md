# Marketing Performance vs. Revenue Growth Analytics

**End-to-end analytics pipeline connecting organic search performance to revenue outcomes — built with Python (ETL), Excel, and Power BI (DAX).**

---

## Overview

This project simulates a realistic marketing analytics stack for an e-commerce
content site and answers the question every marketing leader eventually asks:
**"Which content is actually driving revenue, not just traffic?"**

It blends three data sources that, in most companies, live in three separate
tools and never talk to each other:

| Source | What it represents | Format |
|---|---|---|
| SEMrush keyword rankings | SEO visibility (Keyword, Search Volume, Position, Intent) | CSV export |
| Google Search Console | Organic performance (Clicks, Impressions, CTR, Position) | CSV export |
| Sales CRM | Actual revenue attributed by landing page | Excel export |

A Python ETL pipeline cleans and joins these sources on a normalized URL key,
calculates blended KPIs, and outputs a single analytics-ready table that
feeds a Power BI dashboard.

---

## Business Problem Statement

Marketing and SEO teams are usually measured on **traffic metrics**
(clicks, impressions, rankings), while the business is measured on
**revenue**. These two worlds are rarely connected in the same report,
which makes it difficult to answer basic prioritization questions:

- Which pages should we invest more content/SEO effort into?
- Is our page-2 keyword backlog (positions 11–20) worth chasing?
- Is revenue growth being driven by more traffic, or better conversion?
- Which "high traffic" pages are actually low-value, and vice versa?

This project builds the missing bridge: a single source of truth joining
**SEO visibility → organic traffic → revenue**, so decisions can be made
on business impact instead of vanity metrics.

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data generation & ETL | **Python** (Pandas, NumPy) | Simulate raw sources, clean, join, calculate KPIs |
| Data storage | **CSV / Excel** | Raw and processed data layers |
| Modeling & measures | **Power BI + DAX** | Time intelligence, KPI cards, opportunity flags |
| Ad hoc analysis | **Excel** | Pivot validation, quick-look QA on the processed dataset |
| Version control | **Git / GitHub** | Project hosting and documentation |

---

## Key Insights & Executive Recommendations

*(Based on 12 months of simulated data, Aug 2024–Jul 2025, 12 tracked landing pages, 51.1K organic clicks, $182K attributed revenue)*

- **Revenue concentration is high**: the top 3 pages generate ~50% of total
  attributed revenue, led by `/blog/protein-powder-buying-guide`
  ($38.2K) and `/blog/home-gym-setup-guide` ($27.1K).
  → *Recommendation: prioritize refresh/expansion of the top 3 revenue
  pages before investing in new content — they have proven commercial
  intent, not just traffic.*

- **Traffic and revenue are not the same ranking**: `/blog/best-running-shoes-2025`
  drives strong clicks but converts at only 1.88%, well below the account
  average of 2.88%, while `/products/smart-fitness-watch` converts at 4.53%
  on far less traffic.
  → *Recommendation: audit high-traffic, low-conversion pages for CTA
  placement and product relevance before spending more on rankings there.*

- **Three pages sit in the "Page 2 Opportunity" zone** (positions 11–20 with
  meaningful search volume): `best-running-shoes-2025`, `best-yoga-mats-review`,
  and `recovery-foam-roller` — together already worth ~$38.5K in revenue at
  page-2 rankings.
  → *Recommendation: these are the fastest ROI plays for the SEO team —
  a jump from page 2 to page 1 typically multiplies CTR 2–3x for the same
  content investment already made.*

- **Blended Revenue Per Click (RPC) across all channels is $3.56**, giving
  the business a defensible way to value future organic traffic — e.g.
  justifying content investment by projecting `expected clicks x $3.56`
  rather than guessing.

---

## Folder Directory Structure

```
marketing-revenue-analytics/
│
├── data/
│   ├── raw/
│   │   ├── semrush_keywords.csv
│   │   ├── gsc_performance.csv
│   │   └── crm_revenue.xlsx
│   └── processed/
│       └── processed_marketing_analytics.csv
│
├── scripts/
│   └── etl_pipeline.py
│
├── powerbi/
│   ├── dax_measures.md
│   └── marketing_revenue_dashboard.pbix      # (build locally from processed CSV)
│
├── docs/
│   └── dashboard_screenshots/                # add PNG exports of report pages
│
└── README.md
```

---

## How to Run This Project

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/marketing-revenue-analytics.git
cd marketing-revenue-analytics

# 2. Install dependencies
pip install pandas numpy openpyxl

# 3. Run the ETL pipeline
python scripts/etl_pipeline.py

# Output: data/processed/processed_marketing_analytics.csv
# 4. Load this CSV into Power BI and apply the measures in powerbi/dax_measures.md
```

---

## Resume Bullet Points

Use these as a starting template — adapt the metrics to your actual dashboard
once you've built it out, and be ready to explain every number in an interview:

- Built an end-to-end marketing analytics pipeline in **Python (Pandas,
  NumPy)** that cleaned and merged 3 disparate data sources (SEO rank
  tracking, Google Search Console, CRM revenue) via URL normalization,
  processing 4,000+ records into a single analytics-ready dataset.
- Designed and calculated custom KPIs — **Revenue Per Click, Conversion
  Rate %, and Month-over-Month Revenue Growth** — to connect organic
  search performance directly to business revenue outcomes.
- Developed a **Power BI dashboard** with custom **DAX measures**
  (time-intelligence functions including `DATEADD` and
  `SAMEPERIODLASTYEAR`) to track YoY/MoM growth and surface a
  **"Page 2 SEO Opportunity" flag**, identifying quick-win keyword
  targets worth an estimated **$38K+ in existing attributed revenue**.
- Delivered executive-level insights identifying revenue concentration
  and traffic/conversion mismatches across landing pages, translating
  raw data into **actionable content and SEO prioritization
  recommendations**.
- Applied a **business-first analytics approach** — framing every metric
  around the question "so what should the business do differently,"
  rather than reporting traffic numbers in isolation.

### How to Frame This in an Interview

If asked *"walk me through a project you're proud of,"* structure your
answer as: **problem → data → process → insight → recommendation**:

> "Marketing and revenue data usually live in separate tools, so teams
> optimize for traffic without knowing if it converts. I built a Python
> pipeline that joins SEO, search console, and CRM data on a normalized
> URL key, calculated conversion and revenue-per-click metrics, and
> visualized it in Power BI. That surfaced that our highest-traffic page
> actually had below-average conversion, while three page-2-ranking
> articles were sitting on real revenue potential — a $38K quick-win
> opportunity we wouldn't have seen by looking at rankings or revenue
> data alone."

This demonstrates the full analyst skill set — **technical execution
(Python/DAX) plus business judgment** — which is what separates a
data analyst from someone who can just write queries.
