"""
Financial Report Analyzer - Main Pipeline
Usage: python main.py AAPL
"""
import sys
from pathlib import Path
from src.scrapers.sec_downloader import SECDownloader
from src.analyzers.financial_extractor import FinancialExtractor
from src.utils.data_storage import DataStorage

def analyze_company(ticker: str, company_name: str = "Investor", email: str = "investor@example.com"):
    """
    Complete pipeline to analyze a company's financial reports.
    
    Args:
        ticker: Stock ticker (e.g., "AAPL", "MSFT", "TSLA")
        company_name: Your name for SEC user-agent
        email: Your email for SEC user-agent
    
    TODO: Deine Aufgabe!
    1. Erstelle SECDownloader und lade 10-K Report
    2. Finde den Pfad zur full-submission.txt
    3. Erstelle FinancialExtractor und extrahiere Metriken
    4. Erstelle DataStorage und speichere CSV
    5. Gib eine schöne Summary aus (z.B. "Net Sales: $X billion")
    """
    ticker = ticker.upper()
    print(f"\n{'='*60}")
    print(f"Financial Report Analyzer")
    print(f"{'='*60}")
    print(f"Target Company: {ticker}")
    print(f"{'='*60}\n")

    try:
        downloader = SECDownloader(company_name, email)
        filing_paths = downloader.download_10k(ticker, num_filings=1)  

        if not filing_paths or len(filing_paths) == 0:
            print(f"Error: No 10-K downloaded for {ticker}")
            return

        filing_folder = Path(filing_paths[0])  

        if not filing_folder.exists():
            print("Error: Downloaded folder does not exist.")
            return

        filing_path = None
        for pattern in ["full-submission.txt", "full-submission.html", "*.htm", "*.html"]:
            matches = list(filing_folder.glob(pattern))
            if matches:
                filing_path = matches[0]
                break

        if not filing_path:
            print("Error: No filing document found.")
            print("Folder contains:", [p.name for p in filing_folder.iterdir()])
            return
        
        extractor = FinancialExtractor(filing_path)
        metrics = extractor.get_clean_metrics()

        if not metrics:
            print("Warning: No metrics extracted – possibly an unusual table format.")
            return

        storage = DataStorage()
        csv_path = storage.save_metrics(ticker, metrics)

        latest_sales  = metrics.get("net_sales", [None])[0]
        latest_income = metrics.get("net_income", [None])[0]
        latest_assets = metrics.get("total_assets", [None])[0]

        def fmt(value):
            return f"${value:,}M".replace(",", " ") if value else "N/A"

        print(f"Ticker          : {ticker}")
        print(f"Latest Revenue  : {fmt(latest_sales)}")
        print(f"Latest Net Income: {fmt(latest_income)}")
        print(f"Latest Total Assets: {fmt(latest_assets)}")
        print(f"\nCSV saved to:")
        print(f"   → {csv_path}")
        print("="*60)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py TICKER")
        print("Example: python main.py AAPL")
        sys.exit(1)
    
    ticker = sys.argv[1]
    analyze_company(ticker)