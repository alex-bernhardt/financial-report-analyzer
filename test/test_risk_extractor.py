from pathlib import Path
from src.analyzers.risk_extractor import RiskExtractor

# Test mit Apple
filing_path = Path("data/raw/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt")
extractor = RiskExtractor(filing_path)

# Extrahiere Risk Section
risk_text = extractor.find_risk_section()

if risk_text:
    
    # Extrahiere einzelne Risiken
    paragraphs = extractor.extract_risk_paragraphs(risk_text)
    print(f"\n📋 First risk paragraph:")
    print(paragraphs[0] if paragraphs else "No paragraphs found")
else:
    print("❌ Could not find Risk Factors section")