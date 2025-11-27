"""
Financial Report Analyzer - Main Pipeline
Usage:
  python main.py AAPL                    # Nur Finanzkennzahlen
  python main.py AAPL --full-analysis    # + AI-Risikoanalyse (FinBERT + Keywords + Report)
"""

import sys
import argparse
from pathlib import Path
import numpy as np

# Phase 1: Immer benötigt
from src.scrapers.sec_downloader import SECDownloader
from src.analyzers.financial_extractor import FinancialExtractor
from src.utils.data_storage import DataStorage


def analyze_financials(ticker: str, company_name: str, email: str):
    """Extrahiert und speichert Finanzkennzahlen aus dem 10-K."""
    ticker = ticker.upper()
    print(f"\n{'='*80}")
    print(f"FINANCIAL METRICS ANALYSIS: {ticker}")
    print(f"{'='*80}\n")

    try:
        downloader = SECDownloader(company_name, email)
        filing_paths = downloader.download_10k(ticker, num_filings=1)

        if not filing_paths:
            print(f"Keine 10-K gefunden für {ticker}")
            return None

        filing_folder = Path(filing_paths[0])
        filing_path = None

        # Flexibel: unterstützt .txt, .html, .htm
        for pattern in ["full-submission.txt", "*.html", "*.htm"]:
            matches = list(filing_folder.glob(pattern))
            if matches:
                filing_path = matches[0]
                break

        if not filing_path or not filing_path.exists():
            print("Fehler: Keine lesbare Filing-Datei gefunden.")
            return None

        print(f"Analysiere: {filing_path.name}")

        extractor = FinancialExtractor(filing_path)
        metrics = extractor.get_clean_metrics()

        if not metrics:
            print("Keine Finanzkennzahlen extrahiert – möglicherweise ungewöhnliches Format.")
            return filing_path  # trotzdem weiter, falls Risikoanalyse gewünscht

        storage = DataStorage()
        csv_path = storage.save_metrics(ticker, metrics)

        # Zusammenfassung
        latest_sales = metrics.get("net_sales", [None])[0]
        latest_income = metrics.get("net_income", [None])[0]
        latest_assets = metrics.get("total_assets", [None])[0]

        def fmt(val):
            return f"${val:,.0f}M" if val and val > 0 else "N/A"

        print(f"\nFINANCIAL SUMMARY")
        print(f"Latest Revenue     : {fmt(latest_sales)}")
        print(f"Latest Net Income  : {fmt(latest_income)}")
        print(f"Latest Total Assets: {fmt(latest_assets)}")
        print(f"\nCSV gespeichert → {csv_path}")

        return filing_path

    except Exception as e:
        print(f"Fehler bei der Finanzanalyse: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_risks(ticker: str, filing_path: Path):
    """Führt die komplette AI-Risikoanalyse durch."""
    print(f"\n{'='*80}")
    print(f"AI-POWERED RISK ANALYSIS: {ticker}")
    print(f"{'='*80}\n")

    try:
        # Lazy Import – Modelle nur laden, wenn wirklich benötigt!
        from src.analyzers.risk_extractor import RiskExtractor
        from src.analyzers.sentiment_analyzer import SentimentAnalyzer
        from src.analyzers.keyword_scanner import KeywordScanner
        from src.analyzers.risk_reporter import RiskReporter

        print("Schritt 1/4: Extrahiere Risikoabschnitte aus dem 10-K...")
        risk_extractor = RiskExtractor(filing_path)
        risk_paragraphs = risk_extractor.extract_risk_paragraphs(max_paragraphs=30)
        print(f"Extrahiert {len(risk_paragraphs)} Risikoabsätze\n")

        if len(risk_paragraphs) == 0:
            print("Keine Risikoabsätze gefunden – Bericht wird übersprungen.")
            return

        print("Schritt 2/4: FinBERT Sentiment-Analyse wird gestartet...")
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_results = sentiment_analyzer.analyze_risks(risk_paragraphs)
        overall_risk_score = sentiment_analyzer.get_overall_risk_score(sentiment_results)
        print(f"AI-Risikoscore: {overall_risk_score:.1f}/100\n")

        print("Schritt 3/4: Keyword-Scanning nach kritischen Themen...")
        keyword_scanner = KeywordScanner()
        keyword_results = keyword_scanner.scan_risks(risk_paragraphs)
        print(f"Gefundene kritische Keywords: {keyword_results['total_keywords']}\n")

        print("Schritt 4/4: Generiere Risikobericht...")
        reporter = RiskReporter()
        report_text = reporter.generate_report(
            ticker=ticker,
            sentiment_results=sentiment_results,
            keyword_results=keyword_results,
            overall_risk_score=overall_risk_score
        )

        report_path = reporter.save_report(report_text, ticker)
        print(f"Risikobericht gespeichert → {report_path}")

    except Exception as e:
        print(f"AI-Risikoanalyse fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(
        description="Financial Report Analyzer – Finanzkennzahlen + AI-Risikoanalyse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python main.py AAPL                    → Nur Finanzkennzahlen
  python main.py TSLA --full-analysis    → Komplettanalyse mit AI-Risikobericht
  python main.py NVDA --full-analysis --company-name "Max Mustermann" --email max@example.com
        """
    )

    parser.add_argument("ticker", type=str, help="Aktien-Ticker (z.B. AAPL, MSFT)")
    parser.add_argument("--full-analysis", action="store_true",
                        help="Aktiviert die vollständige AI-Risikoanalyse (FinBERT + Keywords + Report)")
    parser.add_argument("--company-name", type=str, default="Investor",
                        help="Dein Name/Firma für SEC User-Agent (Pflicht!)")
    parser.add_argument("--email", type=str, default="investor@example.com",
                        help="Deine E-Mail für SEC User-Agent (Pflicht!)")

    args = parser.parse_args()

    ticker = args.ticker.upper()

    # Phase 1: Finanzanalyse (immer)
    filing_path = analyze_financials(ticker, args.company_name, args.email)

    if filing_path is None:
        print(f"\nAnalyse für {ticker} fehlgeschlagen – Programm wird beendet.")
        sys.exit(1)

    # Phase 2: Risikoanalyse (optional)
    if args.full_analysis:
        analyze_risks(ticker, filing_path)

        print(f"\n{'='*80}")
        print(f"VOLLSTÄNDIGE ANALYSE FÜR {ticker} ABGESCHLOSSEN!")
        print(f"{'='*80}")
        print("Ergebnisse:")
        print("   → Finanzkennzahlen: data/processed/metrics/")
        print("   → Risikobericht:    data/processed/")
        print("   → Rohdaten:         data/raw/sec_filings/")
    else:
        print(f"\nTipp: Nutze '--full-analysis' für die komplette AI-Risikoanalyse!")
        print(f"Beispiel: python main.py {ticker} --full-analysis")

    print(f"\nDanke für die Nutzung! 🚀")


if __name__ == "__main__":
    main()