"""
etl_pipeline.py
================
Marketing Performance vs. Revenue Growth — ETL Pipeline

Purpose
-------
Simulates a realistic 3-source marketing data stack (SEO rank tracking,
search console performance, and CRM revenue) and blends them into a single
analytics-ready dataset for Power BI / Excel reporting.

Sources simulated:
    1. SEMrush keyword rankings   -> data/raw/semrush_keywords.csv
    2. Google Search Console      -> data/raw/gsc_performance.csv
    3. Sales CRM revenue export   -> data/raw/crm_revenue.xlsx

Output:
    data/processed/processed_marketing_analytics.csv

Author: <Your Name>
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# 0. CONFIG
# ---------------------------------------------------------------------------
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# 12 months of daily data — realistic for a Power BI time-intelligence demo
DATE_RANGE = pd.date_range(start="2024-08-01", end="2025-07-31", freq="D")

# A small, realistic content catalog shared across all 3 sources.
# Real-world messiness (trailing slashes, http/https, query params, casing)
# is injected deliberately so the cleaning step has something to prove.
PAGES = [
    {"url": "/blog/best-running-shoes-2025", "intent": "Commercial", "vol_base": 8200},
    {"url": "/blog/how-to-train-for-a-marathon", "intent": "Informational", "vol_base": 5400},
    {"url": "/products/trail-running-shoes", "intent": "Transactional", "vol_base": 3100},
    {"url": "/blog/protein-powder-buying-guide", "intent": "Commercial", "vol_base": 6700},
    {"url": "/products/smart-fitness-watch", "intent": "Transactional", "vol_base": 4300},
    {"url": "/blog/beginner-strength-training-plan", "intent": "Informational", "vol_base": 7100},
    {"url": "/blog/best-yoga-mats-review", "intent": "Commercial", "vol_base": 2900},
    {"url": "/products/adjustable-dumbbells", "intent": "Transactional", "vol_base": 5600},
    {"url": "/blog/home-gym-setup-guide", "intent": "Informational", "vol_base": 9400},
    {"url": "/products/resistance-bands-set", "intent": "Transactional", "vol_base": 2100},
    {"url": "/blog/pre-workout-supplements-explained", "intent": "Commercial", "vol_base": 3800},
    {"url": "/products/recovery-foam-roller", "intent": "Transactional", "vol_base": 1700},
]

KEYWORDS_PER_PAGE = 4  # SEMrush usually returns several ranking keywords per URL


# ---------------------------------------------------------------------------
# 1a. SIMULATE SEMRUSH KEYWORD RANKINGS
# ---------------------------------------------------------------------------
def generate_semrush_data() -> pd.DataFrame:
    """Creates a synthetic SEMrush-style keyword ranking export."""
    rows = []
    for page in PAGES:
        root_kw = page["url"].split("/")[-1].replace("-", " ")
        variants = [
            root_kw,
            f"best {root_kw}",
            f"{root_kw} review",
            f"{root_kw} 2025",
        ][:KEYWORDS_PER_PAGE]

        for kw in variants:
            position = int(np.clip(np.random.normal(loc=14, scale=8), 1, 95))
            search_volume = int(page["vol_base"] * np.random.uniform(0.05, 0.35))
            rows.append(
                {
                    "Keyword": kw,
                    "Search Volume": search_volume,
                    "Position": position,
                    # Deliberately messy URL formatting -> cleaned later
                    "URL": f"https://www.fitcommerce.com{page['url']}/?ref=semrush",
                    "Intent": page["intent"],
                }
            )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 1b. SIMULATE GOOGLE SEARCH CONSOLE PERFORMANCE
# ---------------------------------------------------------------------------
def generate_gsc_data() -> pd.DataFrame:
    """Creates a synthetic daily GSC performance export per URL."""
    rows = []
    for page in PAGES:
        # Each page gets its own trend + seasonality + a slow ranking improvement
        trend_strength = np.random.uniform(0.0008, 0.0025)
        seasonal_amp = np.random.uniform(0.1, 0.3)

        for i, date in enumerate(DATE_RANGE):
            trend = 1 + (trend_strength * i)  # gradual organic growth over the year
            seasonality = 1 + seasonal_amp * np.sin(2 * np.pi * date.dayofyear / 365)
            noise = np.random.uniform(0.85, 1.15)

            impressions = max(
                0, int(page["vol_base"] * 0.04 * trend * seasonality * noise)
            )
            base_ctr = np.random.uniform(0.02, 0.07)
            clicks = max(0, int(impressions * base_ctr * np.random.uniform(0.8, 1.2)))
            ctr = round(clicks / impressions, 4) if impressions > 0 else 0.0
            position = round(
                np.clip(np.random.normal(loc=14 / trend, scale=3), 1, 100), 1
            )

            rows.append(
                {
                    "Date": date,
                    # Different (but equivalent) URL formatting than SEMrush on purpose
                    "URL": f"fitcommerce.com{page['url']}",
                    "Clicks": clicks,
                    "Impressions": impressions,
                    "CTR": ctr,
                    "Position": position,
                }
            )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 1c. SIMULATE CRM SALES / REVENUE DATA
# ---------------------------------------------------------------------------
def generate_crm_data() -> pd.DataFrame:
    """Creates a synthetic CRM-style revenue export (as if pulled from Excel)."""
    rows = []
    for page in PAGES:
        avg_order_value = np.random.uniform(35, 220)
        conv_rate = np.random.uniform(0.01, 0.04)  # estimated clicks -> orders
        trend_strength = np.random.uniform(0.0008, 0.0025)
        # Average daily clicks this page tends to generate (mirrors GSC scale:
        # vol_base * impression_rate * avg_ctr), used as the Poisson base rate.
        avg_daily_clicks = page["vol_base"] * 0.04 * 0.045

        for i, date in enumerate(DATE_RANGE):
            trend = 1 + (trend_strength * i)
            seasonality = 1 + 0.15 * np.sin(2 * np.pi * (date.dayofyear + 30) / 365)

            expected_orders = max(
                0.05, avg_daily_clicks * conv_rate * trend * seasonality
            )
            orders = int(np.random.poisson(lam=expected_orders))
            revenue = round(orders * avg_order_value * np.random.uniform(0.85, 1.15), 2)

            rows.append(
                {
                    "Date": date,
                    # Trailing slash + different case, again on purpose
                    "URL": f"https://fitcommerce.com{page['url']}/".upper(),
                    "Completed Orders": orders,
                    "Revenue": revenue,
                }
            )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. CLEANING — URL NORMALIZATION
# ---------------------------------------------------------------------------
def normalize_url(url: str) -> str:
    """
    Standardizes URLs across all 3 sources so they can be joined reliably.

    Handles:
        - protocol differences (http/https/none)
        - www. prefix
        - trailing slashes
        - query strings (?ref=, ?utm_, etc.)
        - inconsistent casing
    """
    url = str(url).strip().lower()
    url = url.replace("https://", "").replace("http://", "")
    url = url.replace("www.", "")
    url = url.split("?")[0]           # drop query params
    url = url.rstrip("/")             # drop trailing slash
    if not url.startswith("fitcommerce.com"):
        url = "fitcommerce.com" + url
    return url


# ---------------------------------------------------------------------------
# 3. MERGE + METRIC CALCULATIONS
# ---------------------------------------------------------------------------
def build_pipeline() -> pd.DataFrame:
    print("Generating synthetic raw sources...")
    semrush_df = generate_semrush_data()
    gsc_df = generate_gsc_data()
    crm_df = generate_crm_data()

    # Persist the "raw" extracts, mimicking real vendor exports
    semrush_df.to_csv(RAW_DIR / "semrush_keywords.csv", index=False)
    gsc_df.to_csv(RAW_DIR / "gsc_performance.csv", index=False)
    crm_df.to_excel(RAW_DIR / "crm_revenue.xlsx", index=False)
    print(f"Raw files written to: {RAW_DIR}")

    print("Cleaning and normalizing URLs across all 3 sources...")
    semrush_df["url_clean"] = semrush_df["URL"].apply(normalize_url)
    gsc_df["url_clean"] = gsc_df["URL"].apply(normalize_url)
    crm_df["url_clean"] = crm_df["URL"].apply(normalize_url)

    # Aggregate SEMrush to one row per URL (best position + total keyword volume)
    # since ranking data isn't date-indexed like GSC/CRM.
    semrush_agg = (
        semrush_df.groupby("url_clean")
        .agg(
            best_position=("Position", "min"),
            tracked_keywords=("Keyword", "count"),
            total_keyword_search_volume=("Search Volume", "sum"),
            primary_intent=("Intent", lambda x: x.mode().iloc[0]),
        )
        .reset_index()
    )

    print("Merging GSC performance with CRM revenue on Date + URL...")
    merged = pd.merge(
        gsc_df,
        crm_df,
        on=["Date", "url_clean"],
        how="left",
        suffixes=("_gsc", "_crm"),
    )

    print("Joining SEO ranking context (SEMrush) onto the blended dataset...")
    merged = pd.merge(merged, semrush_agg, on="url_clean", how="left")

    # Fill any dates/pages with no recorded orders that day
    merged["Completed Orders"] = merged["Completed Orders"].fillna(0)
    merged["Revenue"] = merged["Revenue"].fillna(0.0)

    print("Calculating KPIs: RPC, Conversion Rate %, MoM Revenue Growth %...")

    # --- Revenue Per Click (RPC) ---
    merged["Revenue_Per_Click"] = np.where(
        merged["Clicks"] > 0, merged["Revenue"] / merged["Clicks"], 0
    ).round(2)

    # --- Conversion Rate % (Orders / Clicks) ---
    merged["Conversion_Rate_%"] = np.where(
        merged["Clicks"] > 0,
        (merged["Completed Orders"] / merged["Clicks"]) * 100,
        0,
    ).round(2)

    # --- MoM Revenue Growth % (site-wide, applied per row's month) ---
    merged["YearMonth"] = merged["Date"].dt.to_period("M")
    monthly_revenue = (
        merged.groupby("YearMonth")["Revenue"].sum().sort_index().reset_index()
    )
    monthly_revenue["MoM_Revenue_Growth_%"] = (
        monthly_revenue["Revenue"].pct_change() * 100
    ).round(2)

    merged = pd.merge(
        merged,
        monthly_revenue[["YearMonth", "MoM_Revenue_Growth_%"]],
        on="YearMonth",
        how="left",
    )

    # Final column selection + friendly naming for BI consumption
    final_df = merged.rename(
        columns={
            "url_clean": "URL",
            "Position": "GSC_Position",
            "best_position": "SEMrush_Best_Position",
            "tracked_keywords": "Tracked_Keywords_Count",
            "total_keyword_search_volume": "Total_Keyword_Search_Volume",
            "primary_intent": "Primary_Search_Intent",
            "Completed Orders": "Completed_Orders",
        }
    )[
        [
            "Date",
            "YearMonth",
            "URL",
            "Primary_Search_Intent",
            "SEMrush_Best_Position",
            "Tracked_Keywords_Count",
            "Total_Keyword_Search_Volume",
            "GSC_Position",
            "Impressions",
            "Clicks",
            "CTR",
            "Completed_Orders",
            "Revenue",
            "Revenue_Per_Click",
            "Conversion_Rate_%",
            "MoM_Revenue_Growth_%",
        ]
    ]

    final_df["YearMonth"] = final_df["YearMonth"].astype(str)
    final_df = final_df.sort_values(["URL", "Date"]).reset_index(drop=True)

    return final_df


# ---------------------------------------------------------------------------
# 4. MAIN
# ---------------------------------------------------------------------------
def main():
    start = datetime.now()
    print("=" * 70)
    print("MARKETING PERFORMANCE vs REVENUE GROWTH — ETL PIPELINE")
    print("=" * 70)

    final_df = build_pipeline()

    output_path = PROCESSED_DIR / "processed_marketing_analytics.csv"
    final_df.to_csv(output_path, index=False)

    print("-" * 70)
    print(f"Rows processed:      {len(final_df):,}")
    print(f"Unique URLs:         {final_df['URL'].nunique()}")
    print(f"Date range:          {final_df['Date'].min().date()} -> {final_df['Date'].max().date()}")
    print(f"Total Revenue:       ${final_df['Revenue'].sum():,.2f}")
    print(f"Output file:         {output_path}")
    print(f"Runtime:             {(datetime.now() - start).total_seconds():.2f}s")
    print("=" * 70)
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
