# Financial Report Analyzer 🔍📊

Ein Python-Tool, das Jahres- und Quartalsberichte (z. B. 10-K / 10-Q) von Unternehmen automatisch herunterlädt, die wichtigsten Finanzkennzahlen extrahiert, Trends erkennt, Risiken markiert und alles übersichtlich als Dashboard oder PDF-Report ausgibt – in wenigen Minuten statt stundenlangem Excel-Geklicke.

## 🎯 Business Problem

Die manuelle Analyse von Finanzberichten ist extrem zeitaufwendig: Ein einziger 10-K-Report hat oft 100–300 Seiten, wichtige Kennzahlen und Risiken sind über den ganzen Text verstreut.  
Analysten, Investoren und Controller verbringen Stunden oder sogar Tage damit, Zahlen rauszusuchen, zu vergleichen und rote Flaggen zu erkennen – bei hoher Fehlerquote und immer unter Zeitdruck. Gerade kleinere Firmen und Privatpersonen können sich teure Tools wie Bloomberg oder Capital IQ oft nicht leisten.

## 💡 Solution

Mein Analyzer übernimmt genau diese Routinearbeit automatisch:
- Lädt die aktuellsten SEC-Filings (10-K, 10-Q, 8-K) direkt von EDGAR herunter
- Extrahiert automatisch Bilanz, GuV, Cashflow und über 50 wichtige Kennzahlen
- Nutzt NLP, um Risikoparagraphen und Management-Kommentare zu analysieren
- Vergleicht das Unternehmen automatisch mit Branchen-Peers
- Spuckt alles als interaktives Dashboard oder sauberen PDF-Report aus

## 🚀 Key Features (geplant)

- [ ] SEC Edgar Web Scraper (mit Rate-Limiting & Caching)
- [ ] Financial Metrics Extraction (XBRL + PDF Text Parsing)
- [ ] NLP-based Sentiment Analysis & Risk Highlighting
- [ ] Risk Classification Model („low / medium / high risk“)
- [ ] Interactive Dashboard (Streamlit oder Plotly Dash)
- [ ] Peer Company Comparison & Benchmarking

## 🛠️ Tech Stack

- Python 3.11+
- sec-edgar-downloader + BeautifulSoup / Playwright
- pandas & numpy für die Zahlen
- XBRL parsing (python-xbrl oder arelle)
- spaCy / transformers (Hugging Face) für NLP
- Streamlit (für schnelles schönes Dashboard)
- scikit-learn für einfache Klassifizierungsmodelle
- GitHub Actions für automatische Tests

## 📈 Expected Impact

Reduziert die Analysezeit eines kompletten Jahresberichts von durchschnittlich 4–8 Stunden auf unter 5 Minuten – bei höherer Genauigkeit und immer gleicher Methodik.  
Perfekt für Privatinvestoren, Studenten, Start-ups und kleine Analystenteams, die sonst keine teuren Profi-Tools nutzen können.

## 🏗️ Project Status

Currently in development - MVP Phase  
(Erster funktionierender Prototyp läuft schon lokal!)

---
*Developed by Alex Bernhardt – HTL-Absolvent mit Leidenschaft für KI & Finance*