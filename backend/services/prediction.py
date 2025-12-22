import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta

class PredictionService:
    def __init__(self):
        self.model = LinearRegression()

    def predict_trend(self, data: pd.Series, days_ahead: int = 30) -> pd.DataFrame:
        """
        Predice la tendencia futura usando Regresión Lineal.
        Devuelve un DataFrame con fechas futuras y precios estimados.
        """
        # Preparar datos
        df = data.reset_index()
        # Asumiendo que el índice o la primera columna es Fecha
        # Necesitamos convertir fechas a ordinales para regresión
        if 'Date' in df.columns:
            date_col = 'Date'
        else:
            date_col = df.columns[0]
            
        df['DateOrdinal'] = pd.to_datetime(df[date_col]).map(pd.Timestamp.toordinal)
        
        X = df[['DateOrdinal']].values
        y = df['Close'].values if 'Close' in df.columns else df.iloc[:, 1].values # Fallback

        # Entrenar
        self.model.fit(X, y)

        # Predecir futuro
        last_date = pd.to_datetime(df[date_col].iloc[-1])
        future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
        future_ordinals = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
        
        predictions = self.model.predict(future_ordinals)
        
        return pd.DataFrame({
            "Date": future_dates,
            "PredictedClose": predictions
        })
