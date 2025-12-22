import pandas as pd
import numpy as np
import torch
from chronos import ChronosPipeline
from typing import Optional
import datetime

class PredictionService:
    def __init__(self, model_name: str = "amazon/chronos-t5-tiny", device: str = "cpu"):
        if torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"
            
    def __init__(self):
        try:
            # Load Chronos model (Bolt Small for faster/lighter inference)
            self.pipeline = ChronosPipeline.from_pretrained(
                "autogluon/chronos-bolt-small",
                device_map="auto",  # Use GPU if available, else CPU
                torch_dtype=torch.float32, # Ensure compat
            )
            print("Chronos Bolt Small model loaded successfully.")
        except Exception as e:
            print(f"Error loading Chronos model: {e}")
            self.pipeline = None

    def _log(self, message):
        with open("prediction_debug.log", "a") as f:
            f.write(f"{datetime.datetime.now()}: {message}\n")

    def predict_trend(self, data: pd.Series, days_ahead: int = 30) -> pd.DataFrame:
        """
        Predice la tendencia futura usando Amazon Chronos.
        """
        if self.pipeline is None:
            self._log("Pipeline is None. Attempting to reload...")
            self._load_model()
            if self.pipeline is None:
                self._log("Model still not loaded, using linear fallback.")
                print("Model not loaded, using linear fallback.")
                return self._predict_linear_fallback(data, days_ahead)

        try:
            # Prepare DataFrame for Chronos
            # data is a Series with DatetimeIndex (usually)
            df = pd.DataFrame({
                "timestamp": data.index,
                "target": data.values,
                "id": "series_1" # Dummy ID
            })
            
            # Ensure timestamp is datetime
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            
            # Predict
            self._log(f"Running prediction for {days_ahead} days ahead with input shape {df.shape}")
            forecast_df = self.pipeline.predict_df(
                df=df,
                id_column="id",
                timestamp_column="timestamp",
                target="target",
                prediction_length=days_ahead
            )
            
            # Extract results
            # Expected columns: id, timestamp, target_name, predictions, 0.1, ...
            # We want Date, PredictedClose
            
            result_df = pd.DataFrame({
                "Date": forecast_df["timestamp"],
                "PredictedClose": forecast_df["predictions"]
            })
            
            self._log("Prediction successful.")
            return result_df

        except Exception as e:
            self._log(f"Prediction error with Chronos: {e}")
            print(f"Prediction error with Chronos: {e}")
            # Fallback
            return self._predict_linear_fallback(data, days_ahead)
        
    def _predict_linear_fallback(self, data, days_ahead):
        # Fallback simple: Linear Projection using numpy polyfit
        try:
            y = data.values
            x = np.arange(len(y))
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            
            last_x = x[-1]
            future_x = np.arange(last_x + 1, last_x + 1 + days_ahead)
            future_y = p(future_x)
            
            last_date = data.index[-1] if isinstance(data.index, pd.DatetimeIndex) else pd.to_datetime(data.index.values[-1])
            if not isinstance(last_date, pd.Timestamp):
                 last_date = pd.Timestamp(datetime.datetime.now())
    
            future_dates = [last_date + datetime.timedelta(days=i) for i in range(1, days_ahead + 1)]
            
            return pd.DataFrame({
                "Date": future_dates,
                "PredictedClose": future_y
            })
        except Exception as e:
            print(f"Fallback prediction error: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Fallback error: {e}")
            return pd.DataFrame(columns=["Date", "PredictedClose"])

