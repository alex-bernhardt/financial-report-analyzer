import pandas as pd
from pathlib import Path
from datetime import datetime

class DataStorage:
    """
    Saves extracted financial metrics to CSV files for further analysis.
    """
    
    def __init__(self, output_folder: str = "data/processed"):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
    
    def save_metrics(self, ticker: str, metrics: dict) -> Path:
        """
        Save financial metrics to a CSV file.
        
        Args:
            ticker (str): Company ticker symbol (e.g., "AAPL")
            metrics (dict): Dictionary with metric names and values
        
        Returns:
            Path: Path to the saved CSV file
        
        TODO: Deine Aufgabe!
        
        1. Erstelle einen DataFrame aus dem metrics Dictionary
           Tipp: Für jede Metrik (z.B. net_sales) sollte es eine Row geben
           Columns: ['metric_name', 'value_1', 'value_2', 'value_3']
        
        2. Füge zusätzliche Columns hinzu:
           - 'ticker': Der ticker
           - 'timestamp': datetime.now()
        
        3. Speichere als CSV: f"{ticker}_financial_metrics.csv"
        
        4. Return den Pfad zur gespeicherten Datei
        """
        rows = []
        data = pd.DataFrame
        for metric_name, values in metrics.items():
            padded_values = values + [None] * (3 - len(values)) 
            row = {
                'metric_name': metric_name.replace('_', ' ').title(), 
                'value_1': padded_values[0] if len(padded_values) > 0 else None,
                'value_2': padded_values[1] if len(padded_values) > 1 else None,
                'value_3': padded_values[2] if len(padded_values) > 2 else None,
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        df['ticker'] = ticker.upper()
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        column_order = ['ticker', 'timestamp', 'metric_name', 
                            'value_1', 'value_2', 'value_3']
        
        df = df[column_order]

        filename = f"{ticker.upper()}_financial_metrics.csv"
        filepath = self.output_folder / filename
        df.to_csv(filepath, index=False)

        return filepath