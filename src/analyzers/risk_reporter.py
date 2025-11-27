from typing import Dict, List
from datetime import datetime
from pathlib import Path
import numpy as np


class RiskReporter:
    """
    Generates comprehensive risk analysis reports.
    """
    
    def _get_risk_level(self, score: float) -> str:
        if score <= 30:
            return "LOW"
        elif score <= 60:
            return "MEDIUM"
        else:
            return "HIGH"

    def _get_recommendation(self, score: float, top_categories: List[str]) -> str:
        level = self._get_risk_level(score)
        if level == "LOW":
            return "Das Unternehmen zeigt ein niedriges Risikoprofil. Weiter beobachten, aber keine akute Handlung erforderlich."
        elif level == "MEDIUM":
            cats = ", ".join(top_categories[:2]) if top_categories else "verschiedene Risiken"
            return f"Mittleres Risiko erkannt – insbesondere in den Bereichen {cats}. Empfehlung: Detaillierte Prüfung der Risikofaktoren und Monitoring der Entwicklung."
        else:
            cats = ", ".join(top_categories[:3]) if top_categories else "mehrere kritische Bereiche"
            return f"HOHES RISIKO! Dringende Handlungsempfehlung: Sofortige Analyse der Bereiche {cats}, mögliche Reduzierung der Position oder Absicherung."

    def generate_report(
        self, 
        ticker: str,
        sentiment_results: List[Dict],
        keyword_results: Dict,
        overall_risk_score: float
    ) -> str:
        """
        Generate a formatted risk analysis report.
        """
        report = []
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report.append("=" * 80)
        report.append(f"         RISK ANALYSIS REPORT: {ticker.upper()}")
        report.append("=" * 80)
        report.append(f"Generiert am: {now}")
        report.append("")

        # 1. OVERALL RISK SCORE
        risk_level = self._get_risk_level(overall_risk_score)
        risk_emoji = "Low Risk" if risk_level == "LOW" else "Medium Risk" if risk_level == "MEDIUM" else "High Risk"
        
        report.append("OVERALL RISK SCORE")
        report.append("-" * 40)
        report.append(f"Score: {overall_risk_score:.1f} / 100   →   {risk_level} RISK {risk_emoji}")
        report.append("")

        # 2. SENTIMENT ANALYSIS SUMMARY
        total_paragraphs = len(sentiment_results)
        if total_paragraphs > 0:
            avg_neg = np.mean([r["negative"] for r in sentiment_results])
            avg_pos = np.mean([r["positive"] for r in sentiment_results])
            avg_neu = np.mean([r["neutral"]  for r in sentiment_results])
            
            # Riskiest paragraph (höchster negative score)
            riskiest = max(sentiment_results, key=lambda x: x["negative"])
            
            report.append("SENTIMENT ANALYSIS SUMMARY")
            report.append("-" * 40)
            report.append(f"Analysierte Absätze: {total_paragraphs}")
            report.append(f"Durchschnitt:  Positiv {avg_pos:.1%}  |  Negativ {avg_neg:.1%}  |  Neutral {avg_neu:.1%}")
            report.append("")
            report.append("Riskoreichster Absatz (Preview):")
            report.append(f"   → Negativ-Score: {riskiest['negative']:.1%}")
            report.append(f"   → \"{riskiest['text_preview']}\"")
            report.append("")

        # 3. KEYWORD ANALYSIS SUMMARY
        total_kw = keyword_results.get("total_keywords", 0)
        by_cat = keyword_results.get("by_category", {})
        top_keywords = keyword_results.get("top_keywords", [])
        
        # Top categories nach Häufigkeit
        top_cats = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)[:3]
        top_cat_names = [cat for cat, count in top_cats]
        
        report.append("KEYWORD ANALYSIS SUMMARY")
        report.append("-" * 40)
        report.append(f"Gefundene kritische Keywords: {total_kw}")
        if top_cats:
            report.append("Top Risikokategorien:")
            for cat, count in top_cats:
                cat_name = cat.replace("_", " ").title()
                report.append(f"   • {cat_name}: {count} Erwähnungen")
        if top_keywords:
            report.append("")
            report.append("Top 5 Keywords:")
            for kw, count in top_keywords[:5]:
                report.append(f"   • \"{kw}\" → {count}x")
        report.append("")

        # 4. DETAILED FINDINGS – Top 3 riskiest paragraphs
        top_riskiest = sorted(sentiment_results, key=lambda x: x["negative"], reverse=True)[:3]
        
        report.append("TOP 3 RISKOREICHSTE ABSÄTZE")
        report.append("-" * 40)
        for i, para in enumerate(top_riskiest, 1):
            report.append(f"{i}. Absatz #{para['paragraph_number']} – Negativ: {para['negative']:.1%}")
            report.append(f"   Sentiment: {para['sentiment'].upper()}")
            report.append(f"   → \"{para['text_preview']}\"")
            report.append("")

        # 5. RECOMMENDATIONS
        recommendation = self._get_recommendation(overall_risk_score, top_cat_names)
        
        report.append("ZUSAMMENFASSUNG & EMPFEHLUNG")
        report.append("-" * 40)
        report.append(recommendation)
        report.append("")
        report.append("Ende des Berichts.")
        report.append("=" * 80)

        return "\n".join(report)
    
    def save_report(self, report: str, ticker: str, output_dir: str = "data/processed") -> Path:
        """
        Save report to file.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"{ticker.upper()}_risk_report_{datetime.now().strftime('%Y%m%d')}.txt"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Bericht gespeichert: {filepath}")
        return filepath