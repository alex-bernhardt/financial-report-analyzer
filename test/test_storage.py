from pathlib import Path
from src.analyzers.financial_extractor import FinancialExtractor
from src.utils.data_storage import DataStorage

# 1. Extract Metrics
filing_path = Path("data/raw/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt")
extractor = FinancialExtractor(filing_path)
metrics = extractor.get_clean_metrics()

# 2. Save to CSV
storage = DataStorage()
saved_path = storage.save_metrics("AAPL", metrics)

print(f"✅ Metrics saved to: {saved_path}")
print(f"\n📄 Open with: start {saved_path}")  # Windows
# oder: print(f"\n📄 Open with: open {saved_path}")  # Mac