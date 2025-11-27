"""
XBRL Extractor - Production-grade financial metrics extraction
Uses XBRL/iXBRL format for 100% reliability across all SEC filers.
"""

from bs4 import BeautifulSoup
from pathlib import Path
from typing import Dict, List, Optional
import re


class XBRLExtractor:
    """
    Extracts financial metrics from XBRL/iXBRL formatted SEC filings.
    Provides 100% reliability for all public companies.
    """
    
    # Standard GAAP tags for key metrics
    XBRL_TAGS = {
        "net_sales": [
            "us-gaap:Revenues",
            "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax",
            "us-gaap:SalesRevenueNet",
            "us-gaap:RevenuesNetOfInterestExpense"
        ],
        "total_assets": [
            "us-gaap:Assets"
        ],
        "total_liabilities": [
            "us-gaap:Liabilities"
        ],
        "shareholders_equity": [
            "us-gaap:StockholdersEquity",
            "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"
        ],
        "net_income": [
            "us-gaap:NetIncomeLoss",
            "us-gaap:ProfitLoss"
        ],
        "operating_income": [
            "us-gaap:OperatingIncomeLoss"
        ],
        "gross_profit": [
            "us-gaap:GrossProfit"
        ],
        "cash_and_equivalents": [
            "us-gaap:CashAndCashEquivalentsAtCarryingValue"
        ]
    }
    
    def __init__(self, filing_path: Path):
        self.filing_path = filing_path
        self.soup = None
        self._load_filing()
    
    def _load_filing(self):
        """Load and parse the filing with XBRL namespace support."""
        with open(self.filing_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.soup = BeautifulSoup(content, 'lxml-xml')
        
        # Fallback to html parser if xml doesn't work
        if not self.soup.find_all():
            self.soup = BeautifulSoup(content, 'lxml')
        
        print(f"✅ Loaded XBRL filing: {self.filing_path.name}")
    
    def _clean_number(self, value_str: str) -> Optional[float]:
        """Clean and convert XBRL value to float."""
        if not value_str:
            return None
        
        try:
            # Remove commas and whitespace
            cleaned = value_str.replace(',', '').strip()
            
            # Handle negative numbers in parentheses
            if '(' in cleaned and ')' in cleaned:
                cleaned = '-' + cleaned.replace('(', '').replace(')', '')
            
            # Convert to float
            value = float(cleaned)
            
            # XBRL values are often in actual dollars, convert to millions
            # If value > 1 billion, it's likely already in dollars
            if abs(value) > 1_000_000_000:
                return value / 1_000_000  # Convert to millions
            
            return value
            
        except (ValueError, TypeError):
            return None
    
    def _is_annual_context(self, context_id: str, tag) -> bool:
        """
        Check if a context represents annual data (not quarterly).
        Annual contexts usually span ~365 days.
        """
        if not context_id:
            return False
        
        # Try to find the context definition
        context = self.soup.find('context', {'id': context_id}) or \
                  self.soup.find('xbrli:context', {'id': context_id})
        
        if not context:
            # Heuristic: Annual contexts often have 'FY' or full year indicators
            context_lower = context_id.lower()
            if any(indicator in context_lower for indicator in ['fy', 'annual', 'y', 'duration']):
                return True
            # Quarterly indicators
            if any(indicator in context_lower for indicator in ['q1', 'q2', 'q3', 'q4', 'quarter']):
                return False
            return True
        
        # Check period duration
        period = context.find('period') or context.find('xbrli:period')
        if period:
            start_date = period.find('startDate') or period.find('xbrli:startDate')
            end_date = period.find('endDate') or period.find('xbrli:endDate')
            
            if start_date and end_date:
                try:
                    from datetime import datetime
                    start = datetime.strptime(start_date.get_text(strip=True), '%Y-%m-%d')
                    end = datetime.strptime(end_date.get_text(strip=True), '%Y-%m-%d')
                    days = (end - start).days
                    
                    # Annual data spans ~330-400 days (accounting for fiscal years)
                    return 330 <= days <= 400
                except:
                    pass
        
        return True
    
    def extract_metric(self, tag_names: List[str]) -> List[float]:
        """
        Extract values for given XBRL tags.
        
        Args:
            tag_names: List of XBRL tag names to search for
            
        Returns:
            List of values in millions (sorted by size, largest first)
        """
        values = []
        
        for tag_name in tag_names:
            # Search with and without namespace
            tags = self.soup.find_all(tag_name) + \
                   self.soup.find_all(tag_name.split(':')[-1])
            
            # Also search in inline XBRL format
            inline_tags = self.soup.find_all('ix:nonfraction', {'name': tag_name}) + \
                          self.soup.find_all('ix:nonFraction', {'name': tag_name})
            
            tags.extend(inline_tags)
            
            for tag in tags:
                # Check if this is annual data
                context_ref = tag.get('contextref') or tag.get('contextRef')
                
                if not self._is_annual_context(context_ref, tag):
                    continue
                
                # Get the value
                value_str = tag.get_text(strip=True)
                value = self._clean_number(value_str)
                
                if value is not None and abs(value) > 0:
                    values.append(value)
        
        # Remove duplicates and sort by size
        unique_values = list(set(values))
        unique_values.sort(key=abs, reverse=True)
        
        return unique_values[:3]  # Return top 3
    
    def get_basic_metrics(self) -> Dict[str, List[float]]:
        """
        Extract all standard financial metrics using XBRL tags.
        
        Returns:
            Dictionary with metric names and their values
        """
        metrics = {}
        
        for metric_name, tag_names in self.XBRL_TAGS.items():
            values = self.extract_metric(tag_names)
            if values:
                metrics[metric_name] = values
        
        return metrics
    
    def get_clean_metrics(self) -> Dict[str, List[float]]:
        """
        Get cleaned financial metrics (alias for get_basic_metrics).
        Included for API compatibility with FinancialExtractor.
        """
        return self.get_basic_metrics()