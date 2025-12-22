from chronos import ChronosPipeline
import torch

try:
    print("Loading Chronos pipeline from package...")
    pipeline = ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-small",
        device_map="cpu",  # Use "cuda" for GPU
        torch_dtype=torch.bfloat16,
    )
    print("Pipeline loaded successfully!")
    print(pipeline.model)
except Exception as e:
    print(f"Error loading pipeline: {e}")
