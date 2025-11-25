from src.scrapers.sec_downloader import SECDownloader

# Test mit Apple
downloader = SECDownloader("Alex Bernhardt", "alex.bernhardt@example.com")
result = downloader.download_10k("AAPL", num_filings=1)

print(f"\n📁 Dateien gespeichert in:")
for path in result:
    print(f"  → {path}")