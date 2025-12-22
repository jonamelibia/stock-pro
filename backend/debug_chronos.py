
import sys
import pandas as pd
import numpy as np
import torch
from chronos import ChronosPipeline

def test_chronos():
    print(f"Python executable: {sys.executable}")
    print(f"Torch version: {torch.__version__}")
    
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    print(f"Device: {device}")

    model_name = "amazon/chronos-t5-tiny"
    print(f"Loading model {model_name}...")
    
    try:
        pipeline = ChronosPipeline.from_pretrained(
            model_name,
            device_map=device,
            torch_dtype=torch.bfloat16 if device != "cpu" and device != "mps" else torch.float32,
        )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"FAILED to load model: {e}")
        return

    # Test prediction
    print("Testing prediction...")
    try:
        # Create dummy data
        dates = pd.date_range(start="2023-01-01", periods=100)
        values = np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.1, 100)
        
        df = pd.DataFrame({
            "timestamp": dates,
            "target": values,
            "id": "test_series"
        })
        
        forecast = pipeline.predict_df(
            df=df,
            id_column="id",
            timestamp_column="timestamp",
            target="target",
            prediction_length=10
        )
        print("Prediction successful!")
        print(forecast.head())
        
    except Exception as e:
        print(f"Prediction FAILED: {e}")

if __name__ == "__main__":
    test_chronos()
