from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import List, Dict
import numpy as np


class SentimentAnalyzer:
    """
    Analyzes sentiment of financial text using FinBERT.
    """
    
    def __init__(self):
        print("Loading FinBERT model...")
        
        # 1. Lade FinBERT Tokenizer und Modell
        model_name = "ProsusAI/finbert"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # 2. Model in Evaluation-Modus (kein Training, kein Dropout)
        self.model.eval()
        
        # Reihenfolge der Labels bei FinBERT: positive, negative, neutral
        self.labels = ["positive", "negative", "neutral"]
        
        print("FinBERT erfolgreich geladen!")
    
    def analyze_text(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single text.
        """
        # Tokenisierung
        inputs = self.tokenizer(
            text,
            max_length=512,
            truncation=True,
            padding=True,
            return_tensors="pt"
        )
        
        # Kein Gradientenberechnung nötig (spart Speicher & ist schneller)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Softmax über die Logits → Wahrscheinlichkeiten
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        probs = probabilities[0].cpu().numpy()  # [positive, negative, neutral]
        
        # Scores zuordnen
        scores = {
            "positive": float(probs[0]),
            "negative": float(probs[1]),
            "neutral":  float(probs[2])
        }
        
        # Dominantes Sentiment bestimmen
        dominant_sentiment = max(scores, key=scores.get)
        scores["sentiment"] = dominant_sentiment
        
        return scores
    
    def analyze_risks(self, risk_paragraphs: List[str]) -> List[Dict]:
        """
        Analyze sentiment for multiple risk paragraphs.
        """
        results = []
        
        print(f"Analysiere Sentiment von {len(risk_paragraphs)} Risiko-Absätzen...")
        
        for i, para in enumerate(risk_paragraphs):
            # Sentiment analysieren
            sentiment = self.analyze_text(para)
            
            # Vorschau des Textes (erste 100 Zeichen)
            preview = para.strip().replace("\n", " ")[:100]
            if len(para) > 100:
                preview += "..."
            
            # Ergebnis zusammenstellen
            result = {
                "paragraph_number": i + 1,
                "text_preview": preview,
                "positive": sentiment["positive"],
                "negative": sentiment["negative"],
                "neutral":  sentiment["neutral"],
                "sentiment": sentiment["sentiment"]
            }
            results.append(result)
            
            # Fortschrittsanzeige alle 5 Absätze
            if (i + 1) % 5 == 0 or (i + 1) == len(risk_paragraphs):
                print(f"  → {i + 1}/{len(risk_paragraphs)} Absätze analysiert...")
        
        return results
    
    def get_overall_risk_score(self, sentiment_results: List[Dict]) -> float:
        """
        Calculate overall risk score (0-100) based on sentiment analysis.
        Höher = mehr negative Stimmung = höheres Risiko
        """
        if not sentiment_results:
            return 0.0
        
        # Extrahiere die Scores
        negatives = [r["negative"] for r in sentiment_results]
        positives = [r["positive"] for r in sentiment_results]
        neutrals  = [r["neutral"]  for r in sentiment_results]
        
        avg_negative = np.mean(negatives)
        avg_positive = np.mean(positives)
        avg_neutral  = np.mean(neutrals)
        
        # Gewichtete Risikobewertung
        raw_score = (
            avg_negative * 100 +      # Negativ treibt Risiko hoch
            avg_positive * (-50) +    # Positiv mindert das Risiko
            avg_neutral  * 10         # Neutral leicht risikobeitragend
        )
        
        risk_score = np.clip(raw_score, 0, 100)
        
        return round(float(risk_score), 2)