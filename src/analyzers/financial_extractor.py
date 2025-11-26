from bs4 import BeautifulSoup
from pathlib import Path
import re

class FinancialExtractor:
    """
    Extracts important numbers from the HTML/XML File and returns it
    Inputs:
        search_text (str): The text (or part of it) to search for inside <td> or <a> tags.
    """
    
    def __init__(self, filing_path: Path):
        self.filing_path = filing_path
        self.soup = None
        self._load_filing()
    
    def _load_filing(self):
        """Load and parse the HTML/XML filing."""
        with open(self.filing_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.soup = BeautifulSoup(content, 'lxml')
        print(f"✅ Loaded filing: {self.filing_path.name}")
    
    def extract_metric(self, search_text: str) -> list:
        """
        Searches for the search_text in <td> or <a> tags and returns the numbers 
        from the <td class="nump"> elements in the same table row(s).

        Args:
            search_text (str): The text (or part of it) to search for inside <td> or <a> tags.

        Returns:
            List[float]: List of all numeric values found in <td class="nump"> cells 
                        of the matching rows.
        """
        soup = self.soup if hasattr(self, 'soup') else BeautifulSoup(self.html, 'html.parser')
        results = []

        for tag in soup.find_all(['td', 'a'], string=re.compile(re.escape(search_text), re.IGNORECASE)):
            row = tag.find_parent('tr')
            if not row:
                continue
            num_cells = row.find_all('td', class_='nump')

            for cell in num_cells:
                text = cell.get_text(strip=True)
                cleaned = text.replace(',', '').strip()
                cleaned = cleaned.replace('\xa0', '')  # non-breaking space

                try:
                    value = float(cleaned)
                    results.append(value)
                except ValueError:
                    continue

        return results
    
    def get_basic_metrics(self) -> dict:
        """
        Extract the most important financial metrics using multiple possible keywords.
        """
        searches = {
            "net_sales":          ["Net sales", "Total net sales", "Revenue", "Total revenue"],
            "total_assets":       ["Total assets"],
            "total_liabilities":  ["Total liabilities"],
            "shareholders_equity":["Stockholders' equity", "Total stockholders' equity", "Shareholders' equity"],
            "net_income":         ["Net income", "Net earnings", "Net profit", "Net loss"],
            "operating_income":   ["Operating income", "Income from operations"],
            "gross_profit":       ["Gross profit"],
            "cash_and_equivalents": ["Cash and cash equivalents"],
        }

        metrics = {}

        for key, keywords in searches.items():
            for keyword in keywords:
                values = self.extract_metric(keyword)
                if values:
                    metrics[key] = values
                    break  

        return metrics
    
    def get_clean_metrics(self) -> dict:
        """
        Get cleaned, deduplicated financial metrics.
        Takes the 3 LARGEST unique values (assumption: larger = annual data).
        
        Returns:
            dict: Cleaned metrics with max 3 values per metric
        """
        raw_metrics = self.get_basic_metrics()
        cleaned = {}
        
        for metric_name, values in raw_metrics.items():
            # Entferne Duplikate
            unique_values = list(set(values))
            
            # Sortiere nach Größe (größte = wahrscheinlich Jahresdaten)
            unique_values.sort(reverse=True)
            
            # Nimm die Top 3 größten Werte
            # (Für die meisten Metriken sind größere Werte = neuere/vollständige Daten)
            cleaned_values = unique_values[:3]
            
            if cleaned_values:
                cleaned[metric_name] = cleaned_values
        
        return cleaned
    
    def extract_metric_with_years(self, search_text: str) -> dict:
        """
        Extract metric values WITH their corresponding years.
        
        Returns:
            dict: {year: value} mapping, e.g., {2025: 416161, 2024: 391035, ...}
        
        TODO für später: Das werden wir in Phase 2 implementieren!
        """
        # Für jetzt: Return empty dict
        # In Phase 2 werden wir die Table Headers parsen
        return {}