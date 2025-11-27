import re
from typing import List, Dict
from collections import Counter


class KeywordScanner:
    """
    Scans risk text for critical keywords and phrases.
    """
    
    def __init__(self):
        # Kategorisierte Risk Keywords (alle werden später in lowercase umgewandelt)
        self.keyword_categories = {
            "legal": [
                "litigation", "lawsuit", "legal proceedings", "investigation",
                "regulatory", "compliance", "violation", "penalty", "fine", "sanction"
            ],
            "financial": [
                "bankruptcy", "insolvency", "liquidity", "debt", "credit risk",
                "cash flow", "financial condition", "impairment", "write-down", "default"
            ],
            "operational": [
                "supply chain", "disruption", "shortage", "delay", "manufacturing",
                "quality", "defect", "recall", "dependency", "outage"
            ],
            "cybersecurity": [
                "cybersecurity", "data breach", "hack", "ransomware", "unauthorized access",
                "malware", "security incident", "cyber attack", "phishing"
            ],
            "market": [
                "competition", "market share", "pricing pressure", "demand",
                "recession", "economic downturn", "inflation", "tariff", "volatility"
            ],
            "reputation": [
                "reputation", "brand", "customer satisfaction", "trust",
                "negative publicity", "adverse media", "scandal", "boycott"
            ]
        }
        
        # Pre-compile regex patterns für bessere Performance bei vielen Texten
        self.patterns = {}
        for category, keywords in self.keyword_categories.items():
            # Escape Sonderzeichen und erstelle Pattern für ganze Wörter/Phrasen
            escaped = [re.escape(k.lower()) for k in keywords]
            # \b für Wortgrenzen (damit "fine" nicht in "define" matcht)
            pattern = r'\b(?:' + '|'.join(escaped) + r')\b'
            self.patterns[category] = re.compile(pattern, re.IGNORECASE)

    def scan_text(self, text: str) -> Dict[str, List[str]]:
        """
        Scan text for keywords in each category.
        Returns only categories where at least one keyword was found.
        """
        text_lower = text.lower()
        found = {}

        for category, pattern in self.patterns.items():
            matches = pattern.findall(text_lower)
            if matches:
                # Entferne Duplikate pro Kategorie, behalte Original-Schreibweise bei
                unique_matches = []
                for match in matches:
                    # Finde die originale Schreibweise im Text
                    original = None
                    for keyword in self.keyword_categories[category]:
                        if keyword.lower() == match.lower():
                            # Suche nach exakter Schreibweise im Originaltext
                            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                                original = keyword
                                break
                    if original and original not in unique_matches:
                        unique_matches.append(original)
                
                if unique_matches:
                    found[category] = unique_matches

        return found

    def scan_risks(self, risk_paragraphs: List[str]) -> Dict:
        """
        Scan all risk paragraphs and aggregate results.
        """
        category_counts = Counter()
        keyword_counter = Counter()
        keyword_details = {cat: [] for cat in self.keyword_categories}  # Für detaillierte Liste
        
        print(f"Scanning {len(risk_paragraphs)} Absätze nach Risiko-Keywords...")

        for i, para in enumerate(risk_paragraphs):
            found_in_para = self.scan_text(para)
            
            for category, keywords in found_in_para.items():
                count = len(keywords)
                category_counts[category] += count
                
                for kw in keywords:
                    keyword_counter[kw] += 1
                    if kw not in keyword_details[category]:
                        keyword_details[category].append(kw)
            
            # Fortschritt alle 10 Absätze
            if (i + 1) % 10 == 0 or i == len(risk_paragraphs) - 1:
                print(f"  → {i + 1}/{len(risk_paragraphs)} Absätze gescannt...")

        # Nur Kategorien mit Treffern anzeigen
        active_details = {k: v for k, v in keyword_details.items() if v}

        return {
            "total_keywords": sum(category_counts.values()),
            "by_category": dict(category_counts),
            "top_keywords": keyword_counter.most_common(10),
            "keyword_details": active_details
        }


# Beispiel zum Testen
if __name__ == "__main__":
    scanner = KeywordScanner()
    
    sample_texts = [
        "The company faces litigation and regulatory investigations in multiple jurisdictions.",
        "A data breach exposed customer information, leading to reputational damage.",
        "Supply chain disruptions and inflation are affecting margins.",
        "High debt levels and liquidity concerns have been raised by analysts."
    ]
    
    result = scanner.scan_risks(sample_texts)
    
    print("\nRisiko-Keyword-Analyse abgeschlossen!")
    print(f"Gesamt gefundene Keywords: {result['total_keywords']}")
    print(f"Nach Kategorie: {result['by_category']}")
    print(f"Top 10 Keywords: {result['top_keywords']}")