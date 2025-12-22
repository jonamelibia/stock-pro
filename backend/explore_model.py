from transformers import AutoModel, AutoConfig
import torch

try:
    print("Loading model...")
    model_name = "google/timesfm-2.5-200m-pytorch"
    # Try loading config first to see architecture
    config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
    print("Config loaded:", config)
    
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    print("Model loaded successfully!")
    print(model)
except Exception as e:
    print(f"Error loading model: {e}")
