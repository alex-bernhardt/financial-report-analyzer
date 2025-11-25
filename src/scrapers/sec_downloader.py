from sec_edgar_downloader import Downloader
from pathlib import Path

class SECDownloader:
    """Helper class to easily download SEC filings (10-K, 10-Q, etc.) for a specific company.

    The SEC requires a user-agent (company name + email) to identify who is making requests.
    This class wraps sec-edgar-downloader and stores all filings in a clean folder structure.

    Args:
        company_name (str): Your name or company name (used as user-agent).
        email (str): Your real email address (required by SEC EDGAR rules).

    Example:
        >>> dl = SECDownloader("Alex Bernhardt", "alex.bernhardt@example.com")
        >>> dl.download_10k("AAPL", num_filings=3)
    """
    
    def __init__(self, company_name: str, email: str):
        self.company_name = company_name
        self.download_folder = Path("data/raw")
        self.download_folder.mkdir(parents=True, exist_ok=True)
        
        # Downloader speichert automatisch in: data/raw/sec-edgar-filings/...
        self.downloader = Downloader(
            company_name, 
            email, 
            download_folder=str(self.download_folder)
        )
        
    def download_10k(self, ticker: str, num_filings: int = 1):
        """Download the latest 10-K annual report(s) for a given ticker symbol.

        Files are saved to data/raw/<ticker>/10-K/... (one subfolder per filing).

        Args:
            ticker (str): Stock ticker symbol in uppercase (e.g. "MSFT", "TSLA").
            num_filings (int, optional): How many of the most recent 10-K filings to download.
                Defaults to 1 (only the latest).

        Returns:
            list[Path]: List of paths to the downloaded filing folders.

        Raises:
            ValueError: If the ticker is empty or no filings were found.

        Example:
            >>> paths = dl.download_10k("GOOGL", num_filings=2)
            >>> print(paths[0])
            data/raw/GOOGL/10-K/0001652044-23-000016
        """
        if not ticker or not ticker.isalpha():
            raise ValueError("Ticker must be a valid non-empty string (e.g. 'AAPL')")

        print(f"Downloading {num_filings} latest 10-K filing(s) for {ticker}...")
        self.downloader.get("10-K", ticker, limit=num_filings)

        # Der Downloader erstellt automatisch: sec-edgar-filings/TICKER/10-K/
        filing_path = self.download_folder / "sec-edgar-filings" / ticker / "10-K"
        
        if not filing_path.exists():
            raise ValueError(f"No 10-K filings found for ticker {ticker}")
        
        filing_dirs = sorted(
            filing_path.glob("*"),
            key=lambda p: p.name,
            reverse=True
        )[:num_filings]

        print(f"✅ Successfully downloaded {len(filing_dirs)} filing(s) to {filing_path}")
        return filing_dirs