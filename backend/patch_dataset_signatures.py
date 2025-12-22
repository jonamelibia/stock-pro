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

dataset_path = "chronos-forecasting/src/chronos/chronos2/dataset.py"

# Use substrings to avoid indentation issues
replace_in_file(dataset_path, "TensorOrArray | Mapping[str, TensorOrArray]", "Union[TensorOrArray, Mapping[str, TensorOrArray]]")
replace_in_file(dataset_path, "TensorOrArray | Mapping[str, TensorOrArray | None]", "Union[TensorOrArray, Mapping[str, Optional[TensorOrArray]]]")
replace_in_file(dataset_path, "str | DatasetMode", "Union[str, DatasetMode]")
replace_in_file(dataset_path, "dict[str, TensorOrArray | None]", "dict[str, Optional[TensorOrArray]]")
replace_in_file(dataset_path, "dict[str, TensorOrArray | Mapping[str, TensorOrArray]]", "dict[str, Union[TensorOrArray, Mapping[str, TensorOrArray]]]")
replace_in_file(dataset_path, "dict[str, np.ndarray | dict[str, np.ndarray]]", "dict[str, Union[np.ndarray, dict[str, np.ndarray]]]")
replace_in_file(dataset_path, "dict[str, torch.Tensor | int | list[tuple[int, int]] | None]", "dict[str, Optional[Union[torch.Tensor, int, list[tuple[int, int]]]]]")

# Fix broken multiline signature in dataset.py
replace_in_file(dataset_path, "| Sequence[Mapping[str, Union[TensorOrArray, Mapping[str, Optional[TensorOrArray]]]]],", ", Sequence[Mapping[str, Union[TensorOrArray, Mapping[str, Optional[TensorOrArray]]]]]],")

# Remaining type hints
replace_in_file(dataset_path, "torch.Tensor | None", "Optional[torch.Tensor]") # _construct_slice
replace_in_file(dataset_path, "TensorOrArray | dict[str, TensorOrArray]", "Union[TensorOrArray, dict[str, TensorOrArray]]") # convert_inputs cast


# tuple patch
replace_in_file(dataset_path, "tuple[list[dict[str, np.ndarray | dict[str, np.ndarray]]], list[str], list[str], list[str]]", "tuple[list[dict[str, Union[np.ndarray, dict[str, np.ndarray]]]], list[str], list[str], list[str]]")

# Patch df_utils.py
df_utils_path = "chronos-forecasting/src/chronos/df_utils.py"
replace_in_file(df_utils_path, "from typing import TYPE_CHECKING", "from typing import TYPE_CHECKING, Union, Optional")
replace_in_file(df_utils_path, "future_df: \"pd.DataFrame | None\"", "future_df: \"Optional[pd.DataFrame]\"")
replace_in_file(df_utils_path, "tuple[\"pd.DataFrame\", \"pd.DataFrame | None\"]", "tuple[\"pd.DataFrame\", Optional[\"pd.DataFrame\"]]")
replace_in_file(df_utils_path, "tuple[\"pd.DataFrame\", \"pd.DataFrame | None\", str, list[int], np.ndarray]", "tuple[\"pd.DataFrame\", Optional[\"pd.DataFrame\"], str, list[int], np.ndarray]")

# Return type of convert_df_input_to_list_of_dicts_input
replace_in_file(df_utils_path, ") -> tuple[list[dict[str, np.ndarray | dict[str, np.ndarray]]], np.ndarray, dict[str, \"pd.DatetimeIndex\"]]:", ") -> tuple[list[dict[str, Union[np.ndarray, dict[str, np.ndarray]]]], np.ndarray, dict[str, \"pd.DatetimeIndex\"]]:")

# Local variables
replace_in_file(df_utils_path, "inputs: list[dict[str, np.ndarray | dict[str, np.ndarray]]] = []", "inputs: list[dict[str, Union[np.ndarray, dict[str, np.ndarray]]]] = []")
replace_in_file(df_utils_path, "task: dict[str, np.ndarray | dict[str, np.ndarray]]", "task: dict[str, Union[np.ndarray, dict[str, np.ndarray]]]")

print("df_utils patching complete.")
