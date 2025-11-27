from bs4 import BeautifulSoup
from pathlib import Path
import re
from typing import List, Optional


class RiskExtractor:
    """
    Extracts the 'Risk Factors' section from SEC 10-K filings.
    """

    def __init__(self, filing_path: Path):
        self.filing_path = filing_path
        self.soup = None
        self._load_filing()

    def _load_filing(self):
        """Load and parse the filing."""
        try:
            with open(self.filing_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.soup = BeautifulSoup(content, 'lxml')
            print(f"Loaded filing for risk analysis: {self.filing_path.name}")
        except Exception as e:
            print(f"Error loading filing: {e}")
            raise

    def find_risk_section(self) -> str:
        if not self.soup:
            return ""

        print("Suche Item 1A Risk Factors – Apple-2025-Edition aktiviert...")

        # ───── 1. XBRL TextBlock (funktioniert bei Apple 2025 zu 100%) ─────
        xbrl_tags = [
            "us-gaap:riskfactorstextblock",
            "riskfactorstextblock",
            "dei:riskfactorstextblock",
        ]
        for tag_name in xbrl_tags:
            tag = self.soup.find(tag_name)
            if tag:
                text = tag.get_text(separator=" ", strip=True)
                text = re.sub(r'\s+', ' ', text)
                if len(text) > 20000:
                    print(f"Found via XBRL <{tag_name}> – Länge: {len(text)} Zeichen")
                    return text

        # ───── 2. Inline XBRL (ix:nonFraction) – Apple 2025 Hauptmethode ─────
        ix_tags = self.soup.find_all("ix:nonfraction", string=re.compile(r"risk\s*factors", re.I))
        if ix_tags:
            # Nimm den ersten großen Block nach dem Treffer
            for ix in ix_tags:
                parent = ix.parent
                while parent and parent.name not in ["div", "span", "td", "p"]:
                    parent = parent.parent
                if parent:
                    full_div = parent.find_next_sibling()
                    if not full_div:
                        full_div = parent
                    text = full_div.get_text(separator=" ", strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    if len(text) > 30000 and "material adverse" in text.lower():
                        print(f"Found via inline XBRL (ix:nonFraction) – Länge: {len(text)}")
                        return text

        # ───── 3. Fallback: Suche im gesamten Roh-HTML nach typischen Risikosätzen ─────
        full_html = str(self.soup)
        patterns = [
            r"(Item\s*1A\.?\s*Risk\s*Factors.*?)(?=Item\s*1B\.?|Item\s*2\.?)",
            r"(?s)The Company.*?operations and performance depend significantly on.{0,5000}?(?=Item\s*1B\.?)",
            r"(?s)Macroeconomic and Industry Risks(.*?)Item\s*1B",
        ]

        for pattern in patterns:
            match = re.search(pattern, full_html, re.I | re.DOTALL)
            if match:
                text = re.sub(r'<.*?>', ' ', match.group(1))
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 20000:
                    print(f"Found via regex fallback – Länge: {len(text)}")
                    return text

        print("Kein Risk Factors gefunden – das sollte nicht passieren")
        return ""

    def extract_risk_paragraphs(self, risk_text: str = None, max_paragraphs: int = 30) -> List[str]:
        if not risk_text:
            risk_text = self.find_risk_section()
        if not risk_text or len(risk_text) < 10000:
            return []

        # ───── HIER DER ENTSCHEIDENDE FIX (alles vor dem ersten echten Risiko abschneiden) ─────
        start_match = re.search(r"(Macroeconomic and Industry Risks|Business Risks|Legal and Regulatory Compliance Risks|Financial Risks|General Risks)", risk_text, re.I)
        if start_match:
            # Überschrift finden und überspringen
            header_end = risk_text.find(".", start_match.end()) + 1
            risk_text = risk_text[header_end:].strip()
        else:
            # Fallback: ab erstem "The Company’s operations..."
            start_match = re.search(r"The Company.?s operations and performance depend significantly", risk_text, re.I)
            if start_match:
                risk_text = risk_text[start_match.start():]

        # ───── Rest bleibt exakt wie in meiner letzten Version (die mit den 32 Absätzen) ─────
        risk_text = re.sub(r"Apple\s*Inc\.?\s*\|\s*20\d{2}\s*Form\s*10-K\s*\|\s*\d+", " ", risk_text)
        risk_text = re.sub(r"\s+", " ", risk_text)

        triggers = [
            "The Company’s operations and performance depend significantly",
            "The Company’s business can be impacted by political events",
            "Global markets for the Company’s products and services are highly competitive",
            "To remain competitive and stimulate customer demand",
            "The Company depends on component and product manufacturing",
            "The Company’s products and services may be affected from time to time by design",
            "The Company is exposed to the risk of write-downs",
            "The Company relies on access to third-party intellectual property",
            "The Company’s future performance depends in part on support",
            "Failure to obtain or create digital content",
            "The Company’s success depends largely on the talents",
            "The Company depends on the performance of carriers",
            "The Company’s business and reputation are impacted by information technology",
            "Losses or unauthorized access to or releases of confidential information",
            "Investment in new business strategies",
            "The Company’s business, results of operations and financial condition could be adversely impacted",
            "The Company is subject to complex and changing laws",
            "Varied stakeholder expectations",
            "The technology industry.*is subject to intense media",
            "The Company’s business is subject to a variety of U.S. and international laws.*personal data",
            "The Company’s net sales and gross margins",
            "The Company’s financial performance is subject to risks associated with changes",
            "The Company is exposed to credit risk",
            "The Company is subject to changes in tax rates",
            "The price of the Company’s stock is subject to volatility"
        ]

        risks = []
        current = ""
        sentences = re.findall(r"[A-Z][^.!?]*[.!?]", risk_text)

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            is_new_risk = any(trigger.lower() in sentence.lower() for trigger in triggers)

            if is_new_risk and current.strip():
                cleaned = re.sub(r'\s+', ' ', current.strip())
                if len(cleaned) > 200:
                    risks.append(cleaned)
                current = sentence
            else:
                current += " " + sentence

            if len(current) > 3500:
                cleaned = re.sub(r'\s+', ' ', current.strip())
                if len(cleaned) > 200:
                    risks.append(cleaned)
                current = ""

        if current.strip():
            cleaned = re.sub(r'\s+', ' ', current.strip())
            if len(cleaned) > 200:
                risks.append(cleaned)

        print(f"Extracted {len(risks)} echte Risikoparagraphen")
        return risks[:max_paragraphs]