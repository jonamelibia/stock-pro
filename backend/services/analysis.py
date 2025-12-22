import pandas as pd
import numpy as np
from typing import Dict, List

class AnalysisService:
    @staticmethod
    def calculate_rsi(data: pd.Series, window: int = 14) -> pd.Series:
        """Calcula el Relative Strength Index (RSI)."""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def calculate_sma(data: pd.Series, window: int) -> pd.Series:
        """Calcula la Media Móvil Simple (SMA)."""
        return data.rolling(window=window).mean()

    @staticmethod
    def calculate_ema(data: pd.Series, window: int) -> pd.Series:
        """Calcula la Media Móvil Exponencial (EMA)."""
        return data.ewm(span=window, adjust=False).mean()

    @staticmethod
    def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
        """Calcula MACD (Moving Average Convergence Divergence)."""
        exp1 = data.ewm(span=fast, adjust=False).mean()
        exp2 = data.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, window: int = 20, num_std: int = 2):
        """Calcula las Bandas de Bollinger."""
        sma = data.rolling(window=window).mean()
        std = data.rolling(window=window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return upper_band, lower_band

    @staticmethod
    def calculate_volatility(data: pd.Series, window: int = 252) -> float:
        """Calcula la volatilidad anualizada (basada en retornos logarítmicos)."""
        log_ret = np.log(data / data.shift(1))
        vol = log_ret.std() * np.sqrt(window)
        return float(vol) if not np.isnan(vol) else 0.0

    @staticmethod
    def calculate_price_targets(current_price: float, volatility: float) -> Dict[str, Dict[str, float]]:
        """
        Calcula objetivos de precio basados en volatilidad anualizada (Cono de probabilidad 1 std dev - 68%).
        Periods: 1m, 3m, 6m, 1y.
        Formula logic range: Price * exp(± vol * sqrt(t)) basically or simplified P * (1 ± vol * sqrt(t))
        """
        periods = {
            "1 Month": 1/12,
            "3 Months": 3/12,
            "6 Months": 6/12,
            "1 Year": 1.0
        }
        
        targets = {}
        for name, t_years in periods.items():
            # Standard Deviation for the period
            sigma = volatility * np.sqrt(t_years)
            
            # Simple Geometric Brownian Motion projection (Drift=0 for conservative estimate)
            # Upper/Lower bounds at 1 sigma (~68% confidence)
            
            upper = current_price * np.exp(sigma)
            lower = current_price * np.exp(-sigma)
            
            targets[name] = {
                "min": round(lower, 2),
                "mean": round(current_price, 2), # Assuming neutral drift
                "max": round(upper, 2)
            }
            
        return targets

