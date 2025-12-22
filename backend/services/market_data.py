import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

class MarketDataService:
    def __init__(self):
        # Principales índices europeos
        self.indices = {
            "IBEX 35": "^IBEX",
            "DAX 40": "^GDAXI",
            "CAC 40": "^FCHI",
            "FTSE 100": "^FTSE",
            "EURO STOXX 50": "^STOXX50E"
        }

    def get_indices_summary(self) -> List[Dict]:
        """Obtiene un resumen actual de los principales índices."""
        summary = []
        for name, ticker in self.indices.items():
            try:
                ticker_obj = yf.Ticker(ticker)
                # Obtenemos info rápida
                info = ticker_obj.info
                # O usamos history para datos más recientes si info falla o es lenta
                hist = ticker_obj.history(period="1d")
                
                if not hist.empty:
                    last_close = hist['Close'].iloc[-1]
                    prev_close = hist['Open'].iloc[-1] # Simplificación, mejor usar prev close real
                    # Intentar obtener previousClose de info si está disponible
                    previous_close = info.get('previousClose', hist['Open'].iloc[0])
                    
                    change = last_close - previous_close
                    change_percent = (change / previous_close) * 100
                    
                    summary.append({
                        "name": name,
                        "ticker": ticker,
                        "price": round(last_close, 2),
                        "change": round(change, 2),
                        "change_percent": round(change_percent, 2),
                        "currency": "EUR" # Asumimos EUR/GBP según corresponda pero hardcodeamos para demo
                    })
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                
        return summary

    def get_historical_data(self, ticker: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """Obtiene datos históricos para un ticker específico."""
        try:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching history for {ticker}: {e}")
            return None
