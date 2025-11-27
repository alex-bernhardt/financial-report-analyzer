"""
Unified Extractor - Intelligent selection between XBRL and HTML parsing
"""

from pathlib import Path
from typing import Dict, List, Optional
from .xbrl_extractor import XBRLExtractor
from .financial_extractor import FinancialExtractor


class UnifiedExtractor:
    """
    Smart financial metrics extractor with automatic format detection.
    
    Strategy:
    1. Try XBRL first (most reliable)
    2. Fallback to HTML parsing if XBRL fails
    3. Return best available results
    """
    
    def __init__(self, filing_path: Path):
        self.filing_path = filing_path
        self.extractor = None
        self.method_used = None
        self._select_extractor()
    
    def _select_extractor(self):
        """Select the best extractor based on filing content."""
        
        # Read first 10000 chars to detect format
        with open(self.filing_path, 'r', encoding='utf-8') as f:
            content_sample = f.read(10000).lower()
        
        # Check for XBRL indicators
        has_xbrl = any(indicator in content_sample for indicator in [
            'xbrl', 'us-gaap:', 'ix:nonfraction', 'contextref', 
            '<context', 'xbrli:', 'xml version'
        ])
        
        if has_xbrl:
            try:
                print("🔍 XBRL format detected - using XBRL extractor (100% reliable)")
                self.extractor = XBRLExtractor(self.filing_path)
                self.method_used = "XBRL"
                
                # Quick validation: try to extract one metric
                test_metrics = self.extractor.get_basic_metrics()
                if test_metrics:
                    return  # XBRL works!
            except Exception as e:
                print(f"⚠️  XBRL extraction failed: {e}")
        
        # Fallback to HTML parsing
        print("🔍 Using HTML parser (works for most companies)")
        self.extractor = FinancialExtractor(self.filing_path)
        self.method_used = "HTML"
    
    def get_clean_metrics(self) -> Dict[str, List[float]]:
        """
        Extract metrics using the best available method.
        
        Returns:
            Dictionary with financial metrics
        """
        metrics = self.extractor.get_clean_metrics()
        
        if metrics:
            print(f"✅ Extracted metrics using {self.method_used} parser")
        else:
            print(f"⚠️  No metrics extracted with {self.method_used} parser")
        
        return metrics
    
    def get_extraction_method(self) -> str:
        """Return which extraction method was used."""
        return self.method_used