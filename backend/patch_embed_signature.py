import os

def replace_in_file(filepath, old, new):
    with open(filepath, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}: replaced '{old}' with '{new}'")
    else:
        print(f"Skipped {filepath}: '{old}' not found")

pipeline_path = "chronos-forecasting/src/chronos/chronos2/pipeline.py"

# embed method inputs fix
# Currently: Union[TensorOrArray , Sequence[TensorOrArray], batch_size:
# Target: Union[TensorOrArray , Sequence[TensorOrArray]], batch_size:
replace_in_file(pipeline_path, ", Sequence[TensorOrArray], batch_size:", ", Sequence[TensorOrArray]], batch_size:")

print("Embed signature patching complete.")
