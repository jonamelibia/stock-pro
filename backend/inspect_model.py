from transformers import AutoModel
import inspect

model_name = "google/timesfm-2.5-200m-pytorch"
model = AutoModel.from_pretrained(model_name, trust_remote_code=True)

print("Forward signature:")
print(inspect.signature(model.forward))

print("\nMethod doc:")
print(model.forward.__doc__)
