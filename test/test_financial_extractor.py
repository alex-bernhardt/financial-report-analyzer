from pathlib import Path
from src.analyzers.financial_extractor import FinancialExtractor

filing_path = Path("data/raw/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt")
extractor = FinancialExtractor(filing_path)

# Nutze die NEUE Methode
metrics = extractor.get_clean_metrics()

print("\n📊 Cleaned Financial Metrics (Top 3 per category):")
print("=" * 60)
for metric_name, values in metrics.items():
    print(f"\n{metric_name.replace('_', ' ').title()}:")
    for i, value in enumerate(values, 1):
        print(f"  #{i}: ${value:,.0f} million")
