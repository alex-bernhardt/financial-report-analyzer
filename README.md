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

**Tested with:** Apple (AAPL), Microsoft (MSFT)

## 🚀 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Analyze any US company
python main.py AAPL
python main.py TSLA
python main.py GOOGL
```

## 📊 Sample Output
```
Financial Report Analyzer
Target Company: MSFT
Latest Revenue  : $217 778M
Latest Net Income: $101 832M
Latest Total Assets: $619 003M
CSV saved to: data/processed/MSFT_financial_metrics.csv
```

---
*Developed by Alex Bernhardt – HTL graduate with a passion for AI & Finance*