from pathlib import Path
from src.analyzers.risk_extractor import RiskExtractor
from src.analyzers.sentiment_analyzer import SentimentAnalyzer

# Extract risks
filing_path = Path("data/raw/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt")
risk_extractor = RiskExtractor(filing_path)
risk_paragraphs = risk_extractor.extract_risk_paragraphs(max_paragraphs=5)  

print(f"\n✅ Extracted {len(risk_paragraphs)} risk paragraphs")

# Analyze sentiment
analyzer = SentimentAnalyzer()
results = analyzer.analyze_risks(risk_paragraphs)

# Show results
print("\n📊 Sentiment Analysis Results:")
print("=" * 60)
for result in results:
    print(f"\nParagraph {result['paragraph_number']}:")
    print(f"Preview: {result['text_preview']}...")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Scores: Positive={result['positive']:.2f}, Negative={result['negative']:.2f}, Neutral={result['neutral']:.2f}")

# Overall score
overall_score = analyzer.get_overall_risk_score(results)
print(f"\n🎯 Overall Risk Score: {overall_score:.1f}/100")