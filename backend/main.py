from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Stock Pro Europe API",
    description="API para análisis y predicción de bolsas europeas",
    version="0.1.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción esto debe restringirse
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
    
    # Añadir al resultado
    hist_reset['RSI'] = rsi.values
    hist_reset['MA50'] = ma50.values
    
    # Rellenar NaN con None para JSON válido
    data_json = hist_reset.where(pd.notnull(hist_reset), None).to_dict(orient='records')
    
    # 3. Predicción
    # Usamos últimos 3 meses para la tendencia reciente
    recent_hist = hist.iloc[-90:] if len(hist) > 90 else hist
    predictions = prediction_service.predict_trend(recent_hist['Close'], days_ahead=30)
    predictions['Date'] = predictions['Date'].dt.strftime('%Y-%m-%d')
    pred_json = predictions.to_dict(orient='records')

    return {
        "ticker": ticker,
        "history": data_json,
        "prediction": pred_json
    }

