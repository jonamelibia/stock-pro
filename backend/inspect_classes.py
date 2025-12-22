from transformers import AutoModel
import inspect
import sys

try:
    print("Loading base model to get module...")
    base_model = AutoModel.from_pretrained("google/timesfm-2.5-200m-pytorch", trust_remote_code=True)
    module_name = base_model.__module__
    print(f"Module: {module_name}")
    
    # Get the module object
    mod = sys.modules[module_name]
    
    print("\nClasses in module:")
    for name, obj in inspect.getmembers(mod):
        if inspect.isclass(obj):
            print(f"- {name}")
            
    if hasattr(mod, "TimesFmModelForPrediction"):
        print("\nFound TimesFmModelForPrediction!")
        PredClass = getattr(mod, "TimesFmModelForPrediction")
        print("Signature of forward:")
        print(inspect.signature(PredClass.forward))
    else:
        print("\nTimesFmModelForPrediction NOT found in module.")

except Exception as e:
    print(f"Error: {e}")
