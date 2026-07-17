# 📊 CRM Data Analysis & Product Analytics
## Online Programming School X

> **Final Project** | Data Analytics Programme
> **Author:** Vladyslava Ilchuk

---

## 🎯 About This Project

I am a data analyst who received a project from a client —
an online programming school X. The project involves working
with CRM system data that tracks lead and deal statuses.
My task was to clean and analyse this data to improve
the school's business performance.

**What makes this project unique:**
The entire analysis pipeline was built from scratch —
from raw messy CRM exports to a clean, structured dataset,
interactive Tableau dashboards, and data-driven business
recommendations with a statistically designed A/B hypothesis.

**My role:** Data Analyst
**Client:** Online Programming School X
**Tools:** Python · Pandas · Matplotlib · Seaborn · SciPy · Tableau · Excel · Google Sheets

---

## 🔗 Interactive Dashboards (Tableau Public)

> 👇 Click to explore the dashboards

🔗 **[Dashboard 1 — Business Overview](https://public.tableau.com/views/Final_Project_17835808565980/BusinessOverview?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**
> KPIs · Sales Funnel · Revenue Trend · Geographic Map · Lost Reasons

🔗 **[Dashboard 2 — Deep Dive Analysis](https://public.tableau.com/views/Final_Project_17835808565980/DeepDiveAnalysis?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**
> Unit Economics · SLA Hypothesis · Manager Performance · Campaign ROI

---

## 🎯 Project Goals

- Clean and prepare 4 raw CRM datasets
- Perform descriptive statistics and time-series analysis
- Analyse campaign effectiveness, sales team performance,
  product economics and geographic distribution
- Calculate unit economics by product
- Identify business growth points
- Formulate and statistically design an A/B test hypothesis

---

## 📊 Datasets

| Dataset  | Rows   | Description |
|----------|--------|-------------|
| Contacts | 18,548 | All leads — creation date, assigned manager |
| Calls    | 95,874 | Every call — type, duration, status, SLA |
| Spend    | 20,779 | Ad spend — source, campaign, clicks, cost |
| Deals    | 21,593 | Full pipeline — stage, product, payment, revenue |


---

## 🔑 Key Results

| Metric | Value |
|--------|-------|
| Total Leads (UA) | 18,548 |
| Buyers (B) | 839 |
| Conversion Rate (C1) | 4.52% |
| Actual Revenue | €3,502,771 |
| Contract Revenue | €6,355,601 |
| Unrealized Revenue | €2,852,830 |
| Avg Order Value (AOV) | €827 |
| Customer Acq. Cost (CAC) | €178 |
| Contribution Margin (CM) | €3,353,248 |
| CPA (cost per lead) | €8.06 |
| CPC (cost per click) | €0.30 |


---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical calculations |
| Matplotlib | Static visualisations |
| Seaborn | Statistical plots and heatmaps |
| SciPy | A/B test statistics (z-test, chi-square, Bayesian) |
| Tableau Public | Interactive dashboards |

---

## 🧹 Data Cleaning Highlights

### Technical Decisions

- **Id columns** read as `str` to prevent float64 precision loss —
  19-digit CRM identifiers silently corrupt when read as float,
  creating ~13,000 false duplicates
- **SLA column** stored as mixed `datetime.time` / `datetime.timedelta`
  (Excel exports values < 24h as time, ≥ 24h as timedelta) →
  converted to minutes via universal parsing function
- **Amount fields** contained German monetary format (`€ 3.500,00`)
  where `.` = thousands separator and `,` = decimal →
  custom parser handles both `int` and formatted strings
- **Dates** parsed with explicit `format="%d.%m.%Y"` to prevent
  day/month ambiguity
- **Level of Deutsch** was free-form text in two alphabets
  (Cyrillic + Latin: "B1", "б1", "В1", "ждёт результат B1") →
  Cyrillic-to-Latin substitution + regex extraction → A1/B1/C+

### Business Decisions (per client FAQ)

- `closing_date < created_time` (3,312 rows) → corrected logically
- `Initial Amount Paid > Offer Total` → values swapped
  (manager entered columns in wrong order)
- `Months of study = NaN + Payment Done` → filled with `0`
- `Months of study = NaN + not paid` → filled with `-1`
- `Payment Type` inferred from payment data:
  `Initial = Offer Total` → One Payment
  `Initial < Offer Total` → Recurring Payments
- `Lost Reason = NaN` → `"Not Lost"` (not missing data —
  field is only filled when deal is lost)
- `City = "-"` or blank → `"Unknown"`

---

## 💰 Revenue Calculation

Revenue reflects **actual earned revenue** not full contract value.
Formula provided by the project instructor:

**One Payment:**
```python
Revenue = Initial Amount Paid
```

**Recurring Payments:**
```python
Revenue = Initial Amount Paid
        + (Offer Total Amount − Initial Amount Paid)
          / (Course duration − 1)
          × (Months of study − 1)

# Logic:
# Month 1 is covered by the Initial payment
# Remaining (duration - 1) months split equally
# Student has completed (months_studied - 1) additional months
```

**Example:**

Initial = €500, Offer Total = €4,500
Course duration = 11 months, Months studied = 3
Revenue = 500 + (4500 - 500) / (11 - 1) × (3 - 1)
= 500 + 400 × 2
= €1,300

**Unrealized Revenue** = €6,355,601 − €3,502,771 = **€2,852,830**
Future revenue if all Recurring students complete their courses.

---

## 📈 Analysis Blocks (Notebook 05)

### 1. Descriptive Statistics
Mean, median, mode, range for all numeric fields.
Distribution analysis: Quality, Stage, Source, Product,
Payment Type, Education Type, City, Level of Deutsch.

### 2. Time Series Analysis
Monthly deal creation vs call activity (correlation analysis).
Revenue and payment dynamics by closing month.
Deal duration from creation to payment.

### 3. Campaign Effectiveness
Conversion and revenue by campaign and marketing source.
CPA, ROI, CTR, CPC by source.
Campaign ROI matrix: Spend vs Conversion (scatter).

### 4. Sales Team Performance
Top managers by revenue, conversion rate, avg SLA.
SLA distribution across the team.
Correlation between response speed and conversion.

### 5. Payments & Products
One Payment vs Recurring — revenue and conversion comparison.
Product popularity and conversion: Digital Marketing,
UX/UI Design, Web Developer.

### 6. Geographic Analysis
Lead and conversion distribution by German city.
Heatmap: City × German language level → conversion rate.

---

## 💡 Unit Economics (Notebook 06)

| Metric | Formula | Value |
|--------|---------|-------|
| UA | Total contacts | 18,548 |
| B | Valid buyers (Revenue > 0) | 839 |
| C1 | B / UA × 100 | 4.52% |
| AC | Total ad spend | €149,523 |
| AOV | Revenue / B | €4,082 |
| CAC | AC / B | €178 |
| COGS | 0 (ed-tech, no physical goods) | €0 |
| CM | Revenue − AC − COGS | €3,353,248 |
| CM1 | AOV − CAC | €3,908 |
| CLTV | AOV (single-course model) | €4,082 |
| APC | Avg transactions per buyer | 4.89 |
| CPA | AC / UA | €8.06 |
| CPC | AC / Clicks | €0.30 |

---

## 🔬 Hypothesis 1 — SLA ≤ 30 min → C1 Growth

### Observation from data

- **6,060 leads (28.1%)** received no response at all (SLA = NaN)
- Leads answered within 30 min convert significantly better
  than leads answered after hours
- Historical data simulation confirms the direction
  (chi-square test on fast vs slow SLA groups)

### HADI Cycle

| Stage | Content |
|-------|---------|
| **H** | SLA ≤ 30 min increases C1 by ≥ 1% absolute |
| **A** | Auto-SMS in 2 min + manager call ≤ 30 min + escalation if no response |
| **D** | C1 (primary), Deal Duration Days, Revenue per lead (secondary), Lost "No Answer" rate (guard rail) |
| **I** | z-test for proportions, α = 0.05, power = 0.80 |

### Test Parameters

Current C1 (p1)     : 4.52%
Target C1 (p2)      : 5.52%
MDE                 : +1.00% absolute
Sample per group    : ~5,900 leads
Full test duration  : ~232 days (at 51 leads/day)

### Why 232 days — honest statistical answer

At C1 = 4.52% and ~51 leads/day, detecting a +1% absolute
effect with 95% confidence requires ~11,800 leads total.
This is mathematically correct — the sample size formula
cannot be "shortened" by design choice.

### Professional 2-stage solution

**Stage 1 — 14-day Pilot:**
Launch 50/50 split. Measure proxy metrics:
- % of leads who answered the call in group B
- Actual SLA achieved in group B
- Bayesian PPB score after 14 days

**Stage 2 — Bayesian evaluation (day 14):**
Calculate PPB (Posterior Probability of Being Best).
If PPB > 80% → scale group B to full traffic.
If PPB < 50% → hypothesis not confirmed.

### Revenue potential

---

## 🖥️ How to Run

### Install requirements

```bash
pip install pandas numpy matplotlib seaborn scipy plotly openpyxl
```

### Execution order

```bash
# 1. Data cleaning (run in order)
jupyter notebook notebooks/01_contacts_prepare.ipynb
jupyter notebook notebooks/02_calls_prepare.ipynb
jupyter notebook notebooks/03_spend_prepare.ipynb
jupyter notebook notebooks/04_deals_prepare.ipynb

# 2. Core analysis
jupyter notebook notebooks/05_deals_science.ipynb

# 3. Unit economics & hypothesis
jupyter notebook notebooks/06_product_analytics.ipynb
```

> ⚠️ Place source `.xlsx` files in `data/raw/` before running.
> Raw data is not included in this repository (confidential).

---

## 📄 Project Documentation

📎 [project_walkthrough.pdf](docs/project_walkthrough.pdf)
Step-by-step explanation of each notebook:
what was done, why each decision was made,
and what insights were found.

---

## 👩‍💻 Author

**Vladyslava Ilchuk**
Data Analytics | IT Career Hub | 2026

[![LinkedIn](www.linkedin.com/in/vladyslava-ilchuk-91346b384)
[![Portfolio](https://vladyslava-ilchuk.github.io/vladyslava_portfolio/)

