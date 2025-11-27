from pathlib import Path
from src.analyzers.risk_extractor import RiskExtractor
from src.analyzers.sentiment_analyzer import SentimentAnalyzer
from src.analyzers.keyword_scanner import KeywordScanner
from src.analyzers.risk_reporter import RiskReporter

# Company to analyze
ticker = "AAPL"
filing_path = Path(f"data/raw/sec-edgar-filings/{ticker}/10-K/0000320193-25-000079/full-submission.txt")

print(f"\n{'='*70}")
print(f"COMPLETE RISK ANALYSIS: {ticker}")
print(f"{'='*70}\n")

# Step 1: Extract Risks
print("Step 1: Extracting risk factors...")
risk_extractor = RiskExtractor(filing_path)
risk_paragraphs = risk_extractor.extract_risk_paragraphs(max_paragraphs=20)
print(f"✅ Extracted {len(risk_paragraphs)} risk paragraphs\n")

# Step 2: Sentiment Analysis
print("Step 2: Analyzing sentiment...")
sentiment_analyzer = SentimentAnalyzer()
sentiment_results = sentiment_analyzer.analyze_risks(risk_paragraphs)
overall_score = sentiment_analyzer.get_overall_risk_score(sentiment_results)
print(f"✅ Sentiment analysis complete\n")

# Step 3: Keyword Scanning
print("Step 3: Scanning for risk keywords...")
keyword_scanner = KeywordScanner()
keyword_results = keyword_scanner.scan_risks(risk_paragraphs)
print(f"✅ Found {keyword_results['total_keywords']} keywords\n")

# Step 4: Generate Report
print("Step 4: Generating risk report...")
reporter = RiskReporter()
report = reporter.generate_report(
    ticker=ticker,
    sentiment_results=sentiment_results,
    keyword_results=keyword_results,
    overall_risk_score=overall_score
)

# Display report
print("\n" + report)

# Save report
report_path = reporter.save_report(report, ticker)
print(f"\n📄 Report saved to: {report_path}")