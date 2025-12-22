from transformers import AutoModelForSeq2SeqLM
import torch

try:
    print("Loading Amazon Chronos model...")
    model_name = "amazon/chronos-t5-small"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
    print("Model loaded successfully!")
    print(model)
except Exception as e:
    print(f"Error loading model: {e}")
