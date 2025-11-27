# Financial Report Analyzer

A Python tool that automatically downloads annual and quarterly reports (e.g., 10-K / 10-Q) of U.S. companies, extracts the most important financial metrics, detects trends, highlights risks, and presents everything clearly in an interactive dashboard or PDF report — in just a few minutes instead of hours of manual Excel work.

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/DEIN-USERNAME/financial-report-analyzer
cd financial-report-analyzer
pip install -r requirements.txt
```

### Usage

**Option 1: Financial Metrics Only (⚡ 30 seconds)**
```bash
python main.py AAPL
```
**Output:** CSV with Revenue, Net Income, Total Assets

**Option 2: Complete AI Analysis (🤖 ~3 minutes)**
```bash
python main.py AAPL --full-analysis
```
**Output:**
- 📊 Financial metrics (CSV)
- 📄 AI risk analysis report (TXT)
- 🎯 FinBERT sentiment scores
- 🔍 130+ critical keyword findings
- ⚠️ Risk score (0-100 scale)

**Custom Parameters:**
```bash
python main.py GOOGL --full-analysis --company-name "Your Name" --email "your@email.com"
```

### 📊 Sample Output

**AAPL Analysis Results:**
```
================================================================================
         RISK ANALYSIS REPORT: AAPL
================================================================================
OVERALL RISK SCORE: 65.2 / 100   →   HIGH RISK

SENTIMENT ANALYSIS:
  Analyzed Paragraphs: 30
  Average: 63.3% Negative | 33.9% Neutral | 2.8% Positive
  
KEYWORD FINDINGS:
  Total Keywords: 130
  Top Categories: Financial (32), Market (26), Legal (26)
  Top Keywords: "financial condition" (23x), "reputation" (14x)
  
TOP RISK:
  "Design and manufacturing defects" → 94.4% Negative Sentiment
  
RECOMMENDATION:
  HIGH RISK detected - Immediate analysis of financial, market, and legal areas recommended
================================================================================
```

---

## 🎯 Business Problem

Manually analyzing financial reports is extremely time-consuming: A single 10-K report often has 100–300 pages, with key figures and risks scattered throughout the document.  
Analysts, investors, and controllers spend hours—or even days—searching for numbers, comparing them, and spotting red flags, all under time pressure and with a high risk of errors. Smaller companies and private investors especially cannot afford expensive professional tools like Bloomberg or Capital IQ.

## 💡 Solution

My analyzer automates exactly this repetitive work:
- Automatically downloads the latest SEC filings (10-K, 10-Q, 8-K) directly from EDGAR
- Extracts balance sheets, income statements, cash flow statements, and over 50 key financial metrics
- Uses NLP to analyze risk sections and management commentary
- Automatically compares the company with industry peers
- Outputs everything as an interactive dashboard or clean PDF report

## 🚀 Key Features

- [ ] SEC EDGAR Web Scraper (with rate-limiting & caching)
- [ ] Financial Metrics Extraction (XBRL + PDF text parsing)
- [ ] NLP-based Sentiment Analysis & Risk Highlighting
- [ ] Risk Classification Model (“low / medium / high risk”)
- [ ] Interactive Dashboard (Streamlit or Plotly Dash)
- [ ] Peer Company Comparison & Benchmarking

## 🛠️ Tech Stack

- Python 3.11+
- sec-edgar-downloader + BeautifulSoup / Playwright
- pandas & numpy for data crunching
- XBRL parsing (python-xbrl or Arelle)
- spaCy / Hugging Face transformers for NLP
- Streamlit (fast and beautiful dashboards)
- scikit-learn for classification models
- GitHub Actions for automated testing

## 📈 Expected Impact

Reduces the time required to analyze a full annual report from an average of 4–8 hours to under 5 minutes — with higher accuracy and consistent methodology.  
Perfect for retail investors, students, startups, and small analyst teams who otherwise can’t access expensive professional tools.

## 📊 What Makes This Project Special

**Business Impact:**
- Reduces 4-8 hours of manual analysis to **< 5 minutes**
- AI-powered insights using **FinBERT** (1.8M financial texts trained)
- Actionable recommendations for investors & analysts

**Technical Highlights:**
- End-to-end ML pipeline (Data → NLP → Scoring → Reporting)
- Production-ready error handling & logging
- Modular, extensible architecture
- Professional documentation

**Perfect for:**
- 🎓 AI/Data Science students building portfolios
- 💼 Consulting internship applications (McKinsey, BCG, Deloitte)
- 📊 Finance/FinTech roles
- 🤖 ML Engineering positions

---
*Developed by Alex Bernhardt