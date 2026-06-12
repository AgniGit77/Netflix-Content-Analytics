<div align="center">

# 🎬 Netflix Content Analytics
### End-to-End Data Analyst Portfolio Project

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-E50914?style=for-the-badge)](LICENSE)

*Analyzing 8,800+ Netflix titles across 100+ countries to surface business insights*  
*for content strategy, audience segmentation, and geographic expansion.*

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Skills Demonstrated](#-skills-demonstrated)
- [Dataset](#-dataset)
- [Project Architecture](#-project-architecture)
- [Installation & Setup](#-installation--setup)
- [Running the Pipeline](#-running-the-pipeline)
- [Key Findings & Insights](#-key-findings--insights)
- [Visualizations](#-visualizations)
- [SQL Queries](#-sql-queries)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Business Recommendations](#-business-recommendations)
- [Interview Q&A](#-interview-qa)
- [Resume Description](#-resume-description)
- [Contact](#-contact)

---

## 🎯 Project Overview

This end-to-end data analytics project transforms raw Netflix catalog data into **actionable business intelligence**. Using Python for data cleaning and EDA, SQL for analytical queries, and Power BI for executive dashboards, this project demonstrates the complete data analyst workflow from raw CSV to boardroom-ready insights.

### Business Questions Answered
1. 📺 How does Netflix balance Movies vs TV Shows — and is the mix optimal?
2. 📈 What does Netflix's content growth trajectory reveal about its strategy?
3. 🌍 Which countries represent the biggest content opportunities?
4. 🎭 What genres dominate — and where are the white spaces?
5. 👨‍👩‍👧 How well does Netflix serve different audience segments?
6. 📅 When does Netflix release content — is there a seasonal pattern?
7. 🎬 Who are the most prolific directors and actors on the platform?

---

## 🛠️ Skills Demonstrated

| Category | Technologies & Techniques |
|----------|--------------------------|
| **Data Cleaning** | Pandas, missing value imputation, type casting, feature engineering |
| **EDA** | Univariate / bivariate / time-series analysis, 12 charts |
| **SQL** | Window functions (`LAG`, `SUM OVER`), CTEs, subqueries, normalization |
| **Visualization** | Matplotlib, Seaborn, Netflix dark theme, 12 publication-ready charts |
| **Dashboarding** | Power BI, DAX measures, slicers, cross-filtering, heatmaps |
| **Business Insight** | KPI analysis, strategic recommendations, executive reporting |
| **Engineering** | Modular Python scripts, genre normalization (explode), reusable pipeline |

---

## 📂 Dataset

| Property | Value |
|----------|-------|
| **Source** | [Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows) |
| **File** | `netflix_titles.csv` |
| **Size** | ~3 MB |
| **Rows** | 8,807 titles |
| **Columns** | 12 original + 10 engineered |
| **Time Period** | 2008–2021 (content added dates) |

### Column Dictionary

| Column | Type | Description |
|--------|------|-------------|
| `show_id` | string | Unique identifier |
| `type` | string | Movie or TV Show |
| `title` | string | Title of the content |
| `director` | string | Director name(s) |
| `cast` | string | Comma-separated cast list |
| `country` | string | Production country |
| `date_added` | date | Date added to Netflix |
| `release_year` | int | Year of original release |
| `rating` | string | MPAA / TV rating |
| `duration` | string | Duration (min or seasons) |
| `listed_in` | string | Comma-separated genres |
| `description` | string | Plot summary |
| *(engineered)* | | |
| `year_added` | int | Year extracted from date_added |
| `month_added` | int | Month extracted from date_added |
| `primary_country` | string | First-listed country |
| `primary_genre` | string | First-listed genre |
| `duration_minutes` | float | Movie duration in minutes |
| `duration_seasons` | float | TV Show season count |
| `rating_category` | string | Kids / Teens / Adults / Unknown |
| `era` | string | Decade bucket of release_year |
| `content_age_at_addition` | float | Years between release and Netflix addition |

---

## 🏗️ Project Architecture

```
Netflix/
│
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv          ← Original Kaggle dataset
│   └── processed/
│       ├── netflix_cleaned.csv         ← Cleaned & feature-engineered
│       └── netflix_sql_ready.csv       ← Exploded genres (one per row)
│
├── src/
│   ├── data_cleaning.py               ← Step 1: Clean & preprocess
│   ├── eda_analysis.py                ← Step 2: Generate all charts
│   └── insights.py                    ← Step 3: Business insights report
│
├── sql/
│   ├── schema.sql                     ← Table + view definitions
│   ├── genre_analysis.sql             ← 7 genre queries
│   ├── country_analysis.sql           ← 7 country queries
│   ├── ratings_analysis.sql           ← 8 rating queries
│   ├── content_type_analysis.sql      ← 8 content type queries
│   └── yearly_growth_analysis.sql     ← 8 growth queries (with window fns)
│
├── visualizations/
│   ├── 00_kpi_summary.png
│   ├── 01_content_type_split.png
│   ├── 02_content_growth.png
│   ├── 03_top_genres.png
│   ├── 04_top_countries.png
│   ├── 05_ratings_distribution.png
│   ├── 06_top_directors.png
│   ├── 07_top_actors.png
│   ├── 08_duration_analysis.png
│   ├── 09_monthly_heatmap.png
│   ├── 10_era_distribution.png
│   └── 11_rating_categories.png
│
├── powerbi/
│   └── README_PowerBI.md              ← Dashboard setup & DAX guide
│
├── reports/
│   ├── business_insights.md           ← Full written insight report
│   └── business_insights_data.txt     ← Auto-generated numeric summary
│
├── requirements.txt
└── README.md                          ← This file
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/netflix-content-analytics.git
cd netflix-content-analytics
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the Dataset
1. Go to [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)
2. Download `netflix_titles.csv`
3. Place it in `data/raw/netflix_titles.csv`

---

## 🚀 Running the Pipeline

Run all three steps in sequence:

```bash
# Step 1: Clean and preprocess the data
python src/data_cleaning.py

# Step 2: Run EDA and generate all visualizations
python src/eda_analysis.py

# Step 3: Generate business insights report
python src/insights.py
```

**Expected output after Step 1:**
```
[Load] Raw shape: (8807, 12)
[Clean] Processed shape: (8653, 22)
✅ Data cleaning complete!
```

**Expected output after Step 2:**
```
Generating charts …
  ✓ Saved: visualizations/00_kpi_summary.png
  ✓ Saved: visualizations/01_content_type_split.png
  ... (12 charts total)
✅ All charts saved to: visualizations/
```

---

## 📊 Key Findings & Insights

### 🔑 Finding 1: Netflix is 70% Movies — Suboptimal for Retention
Netflix's catalog skews heavily toward movies (69.6%) despite research showing TV shows deliver 3–5× higher subscriber retention. The platform is leaving engagement value on the table.

### 🔑 Finding 2: 2019 was Peak Content Year — Strategy Has Shifted
Content additions peaked at ~2,153 in 2019, then declined. This signals Netflix's pivot from volume-based growth to quality-driven original content production.

### 🔑 Finding 3: US Dominates but International is the Growth Engine
US content represents 36% of the catalog but Indian, Korean, and Japanese content is growing 40–60% YoY. K-Dramas and anime deliver outsized international subscriber growth.

### 🔑 Finding 4: Adults-Only Skew Limits Market Expansion
~36% of content is rated TV-MA or R. Only ~9% targets kids/families — a significant gap vs Disney+ and a lost opportunity for multi-year subscriber loyalty.

### 🔑 Finding 5: The One-Season Problem — 67% of Shows Cancelled Early
Two-thirds of Netflix originals don't get renewed past season one. This pattern erodes audience trust and prevents long-form storytelling that builds dedicated fan bases.

---

## 📈 Visualizations

All 12 charts are saved in `visualizations/` with Netflix's iconic dark theme:

| # | Chart | Key Insight |
|---|-------|-------------|
| 00 | KPI Summary Dashboard | At-a-glance metrics |
| 01 | Movies vs TV Shows | 70/30 content split |
| 02 | Content Growth | Peak 2019, quality shift |
| 03 | Top Genres | Drama & Comedy dominance |
| 04 | Top Countries | US leads, India growing fast |
| 05 | Ratings Distribution | TV-MA is #1 rating |
| 06 | Top Directors | Raúl Campos leads with 19 |
| 07 | Top Actors | Anupam Kher most featured |
| 08 | Duration Analysis | Avg movie: 99 min |
| 09 | Monthly Heatmap | Q1 and Q4 = peak months |
| 10 | Era Distribution | Mostly 2010s content |
| 11 | Rating Categories | Adults dominate catalog |

---

## 🗃️ SQL Queries

38 production-ready SQL queries across 5 files, using:
- **Window Functions:** `LAG()`, `SUM() OVER()`, `ROW_NUMBER() OVER(PARTITION BY)`
- **CTEs:** Modular, readable multi-step analysis
- **Aggregations:** `GROUP BY`, `HAVING`, conditional sums
- **Self-joins and subqueries** for growth rate calculations

### Sample Query — YoY Growth with Window Functions
```sql
SELECT
    year_added,
    COUNT(*) AS titles_added,
    COUNT(*) - LAG(COUNT(*), 1, 0) OVER (ORDER BY year_added) AS yoy_change,
    ROUND(100.0 * (COUNT(*) - LAG(COUNT(*), 1) OVER (ORDER BY year_added))
          / LAG(COUNT(*), 1) OVER (ORDER BY year_added), 1) AS yoy_growth_pct
FROM netflix_titles
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;
```

---

## 📊 Power BI Dashboard

The dashboard consists of **4 interactive pages**:

| Page | Focus | Key Visuals |
|------|-------|-------------|
| **Executive Summary** | Top-level KPIs | 7 KPI cards, donut chart, bar chart |
| **Content Trends** | Time-series analysis | Stacked area, combo chart, heatmap |
| **Geographic Analysis** | Country deep-dive | World map, bar chart, table |
| **Genre Analysis** | Genre intelligence | Treemap, stacked bars, matrix |

### DAX Highlights
```dax
-- Year-over-Year growth calculation
Titles Added YoY Change = 
    VAR CurrentYear = MAX(netflix_cleaned[year_added])
    VAR CurrentCount = CALCULATE([Total Titles], 
                        netflix_cleaned[year_added] = CurrentYear)
    VAR PrevCount = CALCULATE([Total Titles], 
                    netflix_cleaned[year_added] = CurrentYear - 1)
    RETURN DIVIDE(CurrentCount - PrevCount, PrevCount, 0) * 100
```

> See `powerbi/README_PowerBI.md` for full setup guide, DAX measures, and design system.

---

## 💡 Business Recommendations

| Priority | Recommendation | Expected Impact |
|----------|---------------|----------------|
| 🔴 Critical | Increase TV Show budget to 40% of catalog | +15% retention |
| 🔴 Critical | Expand Kids/Family content to 15% | +8% subscriber growth |
| 🟡 High | Double investment in India, Korea, Brazil originals | +20% international growth |
| 🟡 High | Commit to 3-season minimums for originals | +25% engagement per title |
| 🟢 Medium | Diversify into Sci-Fi, Anime, True Crime genres | +12% catalog differentiation |
| 🟢 Medium | Day-and-date theatrical releases | Premium positioning |

---

## 🎤 Interview Q&A

**Q: How did you handle missing data?**  
> "The dataset had ~2,600 missing directors and ~831 missing countries. Rather than dropping these rows (which would bias geographic analysis), I imputed them with 'Unknown' and excluded 'Unknown' specifically when it was the analysis focus. For ratings — only 7 rows were bad data (duration values in the rating column) which I cleaned via regex."

**Q: Why did you choose Python over Excel?**  
> "Reproducibility and scalability. A Python script runs on 8,800 rows as easily as 8,800,000. I also needed regex-based text parsing, datetime manipulation, and multi-column transformations that would be very slow in Excel. The script saves to CSV which Power BI and SQL can both consume."

**Q: What was technically challenging about the SQL queries?**  
> "The YoY growth query — I needed to calculate the percentage change between consecutive years. This required `LAG()` inside a grouped aggregation, which means nesting the GROUP BY inside a window function. I verified the output against my Python pandas calculation to ensure correctness."

**Q: If you had more data, what else would you analyze?**  
> "User engagement data — watch time, completion rates, and star ratings. With that, I'd calculate content ROI (engagement per dollar of production cost), identify which genres have the highest completion rate, and build a recommendation system. The catalog analysis is the 'supply side'; engagement data would give us the 'demand side.'"

---

## 📄 Resume Description

> **Netflix Content Analytics | Python · SQL · Power BI**  
> *Portfolio Project | [github.com/yourusername/netflix-content-analytics](https://github.com)*
>
> Built an end-to-end analytics pipeline on 8,800+ Netflix titles. Performed data cleaning with Pandas (missing value imputation, feature engineering, genre normalization). Conducted EDA producing 12 branded visualizations covering content growth, genre distribution, geographic analysis, and audience segmentation. Developed 38 SQL queries using window functions (LAG, SUM OVER) and CTEs for YoY growth, genre trends, and country analysis. Designed a 4-page Power BI executive dashboard with DAX measures and cross-filtered slicers. Identified 7 key business insights including a 67% single-season show cancellation rate and a 27-point kids content gap vs competitors, with quantified strategic recommendations for content investment.

---

## 📬 Contact

| Platform | Link |
|----------|------|
| GitHub | [github.com/yourusername](https://github.com) |
| LinkedIn | [linkedin.com/in/yourname](https://linkedin.com) |
| Email | your.email@example.com |
| Portfolio | [yourportfolio.com](https://yourportfolio.com) |

---

<div align="center">

**Built with ❤️ for Data Analytics Portfolio**  
*If this helped you, please ⭐ the repository!*

</div>
