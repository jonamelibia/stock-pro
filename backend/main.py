from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI(
    title="Stock Pro Europe API",
    description="API para análisis y predicción de bolsas europeas",
    version="0.1.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from services.market_data import MarketDataService
from services.analysis import AnalysisService
from services.prediction import PredictionService
from pydantic import BaseModel
from typing import List, Optional

market_service = MarketDataService()
analysis_service = AnalysisService()
prediction_service = PredictionService()

@app.get("/api/indices")
def get_indices():
    return market_service.get_indices_summary()

@app.get("/api/indices/{ticker}/constituents")
def get_index_constituents(ticker: str):
    # Decodificar si viene encodes, aunque FastAPI suele manejarlo.
    # Los tickers como ^IBEX pueden necesitar codificación en URL (e.g. %5EIBEX)
    # Pero si el cliente envía el string correcto, ok.
    data = market_service.get_index_constituents(ticker)
    return data

@app.get("/api/stock/{ticker}")
def get_stock_details(ticker: str, period: str = "6mo"):
    # 1. Obtener datos históricos
    hist = market_service.get_historical_data(ticker, period=period)
    if hist is None or hist.empty:
        return {"error": "Ticker not found or no data"}
    
    # Limpieza básica para JSON (fechas a string)
    hist_reset = hist.reset_index()
    # Detectar nombre col fecha
    date_col = hist_reset.columns[0] 
    hist_reset[str(date_col)] = hist_reset[date_col].dt.strftime('%Y-%m-%d')
    
    # 2. Análisis
    rsi = analysis_service.calculate_rsi(hist['Close'])
    ma50 = analysis_service.calculate_sma(hist['Close'], window=50)
    ema20 = analysis_service.calculate_ema(hist['Close'], window=20)
    macd, signal = analysis_service.calculate_macd(hist['Close'])
    bb_upper, bb_lower = analysis_service.calculate_bollinger_bands(hist['Close'])
    
    # 2.1 Calculate Volatility and Price Targets
    volatility = analysis_service.calculate_volatility(hist['Close'])
    current_price = hist['Close'].iloc[-1]
    targets = analysis_service.calculate_price_targets(current_price, volatility)

    # 2.2 Get Fundamental Info
    info = market_service.get_stock_info(ticker)
    
    # Añadir al resultado
    hist_reset['RSI'] = rsi.values
    hist_reset['MA50'] = ma50.values
    hist_reset['EMA20'] = ema20.values
    hist_reset['MACD'] = macd.values
    hist_reset['Signal'] = signal.values
    hist_reset['BB_Upper'] = bb_upper.values
    hist_reset['BB_Lower'] = bb_lower.values
    
    # Rellenar NaN con None para JSON válido (y manejar Infinitos)
    hist_reset = hist_reset.replace([np.inf, -np.inf], np.nan)
    data_json = hist_reset.where(pd.notnull(hist_reset), None).to_dict(orient='records')
    
    return sanitize_json_output({
        "ticker": ticker,
        "details": {
            "price": current_price,
            "currency": info.get("currency", "EUR"),
            "change": info.get("regularMarketChange", 0),
            "change_percent": info.get("regularMarketChangePercent", 0)
        },
        "history": data_json,
        "kpi": info,
        "targets": targets,
        "prediction": [] # Return empty prediction initially
    })

@app.get("/api/stock/{ticker}/prediction")
def get_stock_prediction(ticker: str, period: str = "6mo"):
    # Necesitamos historia reciente para predecir
    hist = market_service.get_historical_data(ticker, period=period)
    if hist is None or hist.empty:
        return {"error": "No data for prediction"}

    # 3. Predicción
    # Update: User requested fixed 30 days prediction length due to model limitations (>64 days degrades quality)
    days_ahead = 30
    
    try:
        # Usamos todos los datos disponibles o un subset razonable
        # Para Chronos, más contexto es mejor, pero limitado a ventana de contexto del modelo
        recent_hist = hist.iloc[-200:] if len(hist) > 200 else hist
        
        predictions = prediction_service.predict_trend(recent_hist['Close'], days_ahead=days_ahead)
        
        if predictions.empty:
             return []

        predictions['Date'] = predictions['Date'].dt.strftime('%Y-%m-%d')
        
        # Limpiar predicciones
        predictions = predictions.replace([np.inf, -np.inf], np.nan)
        pred_json = predictions.where(pd.notnull(predictions), None).to_dict(orient='records')

        return sanitize_json_output(pred_json)
    except Exception as e:
        print(f"Error in prediction endpoint: {e}")
        return [] # Return empty list on error to avoid 500 in UI

# Limpieza final recursiva para asegurar que no queda ningún NaN
def sanitize_json_output(data):
    if isinstance(data, list):
        return [sanitize_json_output(item) for item in data]
    if isinstance(data, dict):
        return {k: sanitize_json_output(v) for k, v in data.items()}
    if isinstance(data, float) and (np.isnan(data) or np.isinf(data)):
        return None
    return data

