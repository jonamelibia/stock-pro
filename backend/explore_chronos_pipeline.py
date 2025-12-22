from transformers import pipeline
import torch

try:
    print("Loading Chronos pipeline...")
    # Check if a custom pipeline file exists in the model repo
    p = pipeline("chronos-prediction", model="amazon/chronos-t5-small", trust_remote_code=True, device="cpu")
    print("Pipeline loaded!")
    print(p)
except Exception as e:
    print(f"Error loading pipeline: {e}")
