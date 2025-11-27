from pathlib import Path
from src.analyzers.risk_extractor import RiskExtractor
from src.analyzers.keyword_scanner import KeywordScanner

# Extract risks
filing_path = Path("data/raw/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt")
risk_extractor = RiskExtractor(filing_path)
risk_paragraphs = risk_extractor.extract_risk_paragraphs(max_paragraphs=10)

# Scan keywords
scanner = KeywordScanner()
results = scanner.scan_risks(risk_paragraphs)

print("\n🔍 Keyword Analysis Results:")
print("=" * 60)
print(f"Total Keywords Found: {results['total_keywords']}")

print("\n📊 Keywords by Category:")
for category, count in sorted(results['by_category'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {category.capitalize()}: {count}")

print("\n🔥 Top 10 Most Frequent Keywords:")
for keyword, count in results['top_keywords']:
    print(f"  '{keyword}': {count} occurrences")