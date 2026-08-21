# Power BI DAX Measures

All measures assume the fact table is named `MarketingAnalytics`, loaded from
`processed_marketing_analytics.csv`, with a related `Date` table (`DimDate`)
marked as the official Date table for time intelligence.

Columns referenced: `Date`, `URL`, `Revenue`, `Clicks`, `Impressions`,
`Completed_Orders`, `SEMrush_Best_Position`, `Total_Keyword_Search_Volume`.

---

## 1. Total Revenue

```dax
Total Revenue =
SUM ( MarketingAnalytics[Revenue] )
```

## 2. Total Organic Clicks

```dax
Total Organic Clicks =
SUM ( MarketingAnalytics[Clicks] )
```

## 3. MoM Revenue Growth %

```dax
MoM Revenue Growth % =
VAR CurrentMonthRevenue =
    [Total Revenue]
VAR PreviousMonthRevenue =
    CALCULATE (
        [Total Revenue],
        DATEADD ( DimDate[Date], -1, MONTH )
    )
RETURN
    IF (
        NOT ISBLANK ( PreviousMonthRevenue ) && PreviousMonthRevenue <> 0,
        DIVIDE ( CurrentMonthRevenue - PreviousMonthRevenue, PreviousMonthRevenue ),
        BLANK ()
    )
```

## 4. YoY Revenue Growth %

```dax
YoY Revenue Growth % =
VAR CurrentYearRevenue =
    [Total Revenue]
VAR PriorYearRevenue =
    CALCULATE (
        [Total Revenue],
        SAMEPERIODLASTYEAR ( DimDate[Date] )
    )
RETURN
    IF (
        NOT ISBLANK ( PriorYearRevenue ) && PriorYearRevenue <> 0,
        DIVIDE ( CurrentYearRevenue - PriorYearRevenue, PriorYearRevenue ),
        BLANK ()
    )
```

## 5. Revenue Per Click (RPC)

```dax
Revenue Per Click (RPC) =
DIVIDE ( [Total Revenue], [Total Organic Clicks], 0 )
```

## 6. Opportunity Flag — Page 2 Keywords (High-Volume, Position 11–20)

Flags URLs ranking on Google's page 2 (positions 11–20) that carry high
search volume — these are the fastest, lowest-effort wins for an SEO team,
since a small ranking improvement can move them onto page 1.

```dax
Page 2 Opportunity Flag =
VAR AvgPosition =
    AVERAGE ( MarketingAnalytics[SEMrush_Best_Position] )
VAR TotalVolume =
    SUM ( MarketingAnalytics[Total_Keyword_Search_Volume] )
VAR HighVolumeThreshold = 1000  -- adjust to your dataset's distribution
RETURN
    IF (
        AvgPosition >= 11 && AvgPosition <= 20 && TotalVolume >= HighVolumeThreshold,
        "Opportunity",
        "No Action"
    )
```

**Optional supporting measure** — count of opportunity URLs, useful for a
KPI card on the executive summary page:

```dax
Page 2 Opportunity Count =
CALCULATE (
    DISTINCTCOUNT ( MarketingAnalytics[URL] ),
    FILTER (
        VALUES ( MarketingAnalytics[URL] ),
        [Page 2 Opportunity Flag] = "Opportunity"
    )
)
```

---

## Notes for Interview Discussion

- `DATEADD` and `SAMEPERIODLASTYEAR` require a proper Date dimension table
  marked as the model's Date table — a common gotcha interviewers probe for.
- `DIVIDE()` is used instead of the `/` operator throughout to avoid
  divide-by-zero errors without wrapping every measure in `IFERROR`.
- The Opportunity Flag threshold (1000 monthly search volume) should be
  justified against the actual dataset's volume distribution — in a real
  interview, mention that you'd validate this cutoff against the 75th
  percentile of `Total_Keyword_Search_Volume` rather than hardcoding it.
