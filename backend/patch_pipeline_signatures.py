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

# Imports
replace_in_file(pipeline_path, "from typing import TYPE_CHECKING, Callable, Literal, Mapping, Sequence, Union, Optional", "from typing import TYPE_CHECKING, Callable, Literal, Mapping, Sequence, Union, Optional") # Ensure imported (already patched?)
replace_in_file(pipeline_path, "from typing import TYPE_CHECKING, Callable, Literal, Mapping, Sequence", "from typing import TYPE_CHECKING, Callable, Literal, Mapping, Sequence, Union, Optional")

# 1. Start of inputs
replace_in_file(pipeline_path, "inputs: TensorOrArray", "inputs: Union[TensorOrArray")
# 2. Middle Sequence (shared)
replace_in_file(pipeline_path, "| Sequence[TensorOrArray]", ", Sequence[TensorOrArray]")
# 3. End of fit inputs (with Optional) - 6 brackets
replace_in_file(pipeline_path, "| Sequence[Mapping[str, TensorOrArray | Mapping[str, TensorOrArray | None]]],", ", Sequence[Mapping[str, Union[TensorOrArray, Mapping[str, Optional[TensorOrArray]]]]]],")
# 4. End of predict inputs (no Optional) - 5 brackets
replace_in_file(pipeline_path, "| Sequence[Mapping[str, TensorOrArray | Mapping[str, TensorOrArray]]],", ", Sequence[Mapping[str, Union[TensorOrArray, Mapping[str, TensorOrArray]]]]],")

# Validation inputs fixes
replace_in_file(pipeline_path, "validation_inputs: Union[TensorOrArray", "validation_inputs: Optional[Union[TensorOrArray")
# Line 104 exact match (no comma at end)
replace_in_file(pipeline_path, "| Sequence[Mapping[str, TensorOrArray | Mapping[str, TensorOrArray | None]]]", ", Sequence[Mapping[str, Union[TensorOrArray, Mapping[str, Optional[TensorOrArray]]]]]")

# Ensure predict Mapping line (with comma) IS replaced.
# In previous run, I used strict string with closing brackets. 
# "        | Sequence[Mapping[str, TensorOrArray | Mapping[str, TensorOrArray]]]," -> "        , Sequence[Mapping[str, Union[TensorOrArray, Mapping[str, TensorOrArray]]]]],"
# I need to verify if this ran. It printed "Patched ... replaced ...".
# So predict should be fine (5 brackets? Sequence, Mapping, Union, Mapping, InputsUnion. Yes 5). 
# Wait, predict input union needs 5 brackets.
# My replacement had `]]]]],`. 
# Optional(1) - NO Optional in predict.
# Sequence(1) Mapping(1) Union(1) Mapping(1) Union(Inputs)(1). Total 5.
# Mapping[str, Union[T, Mapping[str, T]]]
# Mapping(inner) ]
# Union ]
# Mapping(outer) ]
# Sequence ]
# Union(inputs) ]
# So 5 is correct.

print("Pipeline signature patching complete.")
