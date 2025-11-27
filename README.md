# Financial Report Analyzer

A Python tool that automatically downloads annual and quarterly reports (e.g., 10-K / 10-Q) of U.S. companies, extracts the most important financial metrics, detects trends, highlights risks, and presents everything clearly in an interactive dashboard or PDF report — in just a few minutes instead of hours of manual Excel work.

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

## 🚀 Key Features (planned)

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

## 🏗️ Project Status

✅ **MVP Complete!** 

**What works:**
- ✅ Automatic SEC 10-K filing downloads
- ✅ Financial metrics extraction (Revenue, Net Income, Assets, etc.)
- ✅ Data cleaning and deduplication
- ✅ CSV export for further analysis
- ✅ Command-line interface

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Analyze any US company
python main.py AAPL
python main.py MSFT
python main.py GOOGL
```

## ✅ Tested Companies

- ✅ **Apple (AAPL)** - Full support
- ✅ **Microsoft (MSFT)** - Full support
- ✅ **Google (GOOGL)** - Full support

## ⚠️ Known Limitations

**Current Version (MVP):**
- Uses HTML parsing which works well for most S&P 500 companies
- Some companies (e.g., Tesla) use non-standard table formats
- **Phase 2** will implement XBRL parsing for 100% reliability

## 📊 Example Output

### Command:
```bash
python main.py AAPL
```

### Result:
```
Financial Report Analyzer
Target Company: AAPL
Latest Revenue     : $209,586M
Latest Net Income  : $112,010M
Latest Total Assets: $364,980M

CSV saved to: data/processed/AAPL_financial_metrics.csv
```

## 🤖 Phase 2: AI-Powered Risk Analysis (COMPLETE!)

**NEW Features:**
- ✅ **FinBERT Sentiment Analysis** - State-of-the-art financial NLP
- ✅ **Intelligent Keyword Scanner** - 6 risk categories, 50+ keywords
- ✅ **Risk Scoring Algorithm** - 0-100 scale with automatic classification
- ✅ **Professional Report Generation** - Actionable insights & recommendations

**Usage:**
```bash
python test_full_risk_analysis.py
```

**Sample Output:**
```
OVERALL RISK SCORE: 68.7/100 → HIGH RISK
Sentiment: 66.9% Negative | 30.6% Neutral | 2.5% Positive
Keywords Found: 87 (Operational: 22, Financial: 21, Market: 17)
Top Risk: "Design and manufacturing defects" (94.4% negative)
```

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
*Developed by Alex Bernhardt – HTL graduate with a passion for AI & Finance*