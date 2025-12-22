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

# Patch utils.py
utils_path = "chronos-forecasting/src/chronos/utils.py"
replace_in_file(utils_path, "from typing import List", "from typing import List, Union")
replace_in_file(utils_path, "torch.Tensor | list[float]", "Union[torch.Tensor, list[float]]")
replace_in_file(utils_path, "torch.Tensor | list[float]", "Union[torch.Tensor, list[float]]") # Run twice to be sure used everywhere

# Patch config.py
config_path = "chronos-forecasting/src/chronos/chronos2/config.py"
replace_in_file(config_path, "from typing import List, Literal", "from typing import List, Literal, Optional, Union")
replace_in_file(config_path, 'attn_implementation: Literal["eager", "sdpa"] | None = None', 'attn_implementation: Optional[Literal["eager", "sdpa"]] = None')
replace_in_file(config_path, "time_encoding_scale: int | None = None", "time_encoding_scale: Optional[int] = None")

# Patch base.py
base_path = "chronos-forecasting/src/chronos/base.py"
replace_in_file(base_path, "prediction_length: int | None = None", "prediction_length: Optional[int] = None")
replace_in_file(base_path, "inputs: Union[torch.Tensor, List[torch.Tensor]]", "inputs: Union[torch.Tensor, List[torch.Tensor]]") # Already correct? check file.
# base.py line 142: prediction_length: int | None = None
# Check imports in base.py
replace_in_file(base_path, "from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union", "from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Union") 

# Patch dataset.py (defines TensorOrArray)
dataset_path = "chronos-forecasting/src/chronos/chronos2/dataset.py"
replace_in_file(dataset_path, "TensorOrArray: TypeAlias = Union[torch.Tensor, np.ndarray]", "TensorOrArray = Union[torch.Tensor, np.ndarray]") # Fix NameError
replace_in_file(dataset_path, "TensorOrArray: TypeAlias = torch.Tensor | np.ndarray", "TensorOrArray = Union[torch.Tensor, np.ndarray]") # Fallback
replace_in_file(dataset_path, "from typing import TYPE_CHECKING, Any, Iterator, Mapping, Sequence, TypeAlias, cast", "from typing import TYPE_CHECKING, Any, Iterator, Mapping, Sequence, Union, Optional, cast") # Removed TypeAlias, Added Union, Optional
replace_in_file(dataset_path, "from typing import TYPE_CHECKING, Iterator, Mapping, Sequence, TypeAlias, cast", "from typing import TYPE_CHECKING, Iterator, Mapping, Sequence, Union, Optional, cast") # Removed TypeAlias from other import
replace_in_file(dataset_path, "from typing import TYPE_CHECKING, Any, Iterator, Mapping, Sequence, TypeAlias", "from typing import TYPE_CHECKING, Any, Iterator, Mapping, Sequence, Union, Optional")
replace_in_file(dataset_path, "context_length: int | None = None", "context_length: Optional[int] = None")
replace_in_file(dataset_path, "prediction_length: int | None = None", "prediction_length: Optional[int] = None")
replace_in_file(dataset_path, "min_past: int | None = None", "min_past: Optional[int] = None")
replace_in_file(dataset_path, "mode: str | DatasetMode = DatasetMode.TRAIN", "mode: Union[str, DatasetMode] = DatasetMode.TRAIN")

# Patch pipeline.py
pipeline_path = "chronos-forecasting/src/chronos/chronos2/pipeline.py"
replace_in_file(pipeline_path, "from typing import TYPE_CHECKING, Callable, Literal, Mapping, Sequence", "from typing import TYPE_CHECKING, Callable, Literal, Mapping, Sequence, Union, Optional")
replace_in_file(pipeline_path, "context_length: int | None = None", "context_length: Optional[int] = None")
replace_in_file(pipeline_path, "prediction_length: int | None = None", "prediction_length: Optional[int] = None")
replace_in_file(pipeline_path, "min_past: int | None = None", "min_past: Optional[int] = None")
replace_in_file(pipeline_path, "lora_config: \"LoraConfig | dict | None\" = None", "lora_config: \"Union[LoraConfig, dict, None]\" = None")
replace_in_file(pipeline_path, "output_dir: Path | str | None = None", "output_dir: Optional[Union[Path, str]] = None")
replace_in_file(pipeline_path, "callbacks: list[\"TrainerCallback\"] | None = None", "callbacks: Optional[list[\"TrainerCallback\"]] = None")
replace_in_file(pipeline_path, "future_df: \"pd.DataFrame | None\" = None", "future_df: \"Optional[pd.DataFrame]\" = None")
replace_in_file(pipeline_path, "target: str | list[str] = \"target\"", "target: Union[str, list[str]] = \"target\"")
replace_in_file(pipeline_path, "finetune_kwargs: dict | None = None", "finetune_kwargs: Optional[dict] = None")
replace_in_file(pipeline_path, "save_directory: str | Path", "save_directory: Union[str, Path]")
replace_in_file(pipeline_path, "future_covariates: torch.Tensor | None", "future_covariates: Optional[torch.Tensor]")

# Patch chronos_bolt.py
bolt_path = "chronos-forecasting/src/chronos/chronos_bolt.py"
replace_in_file(bolt_path, "from typing import Literal", "from typing import Literal, Optional, Union")
replace_in_file(bolt_path, "loc_scale: tuple[torch.Tensor, torch.Tensor] | None = None", "loc_scale: Optional[tuple[torch.Tensor, torch.Tensor]] = None")
replace_in_file(bolt_path, "torch.Tensor | None", "Optional[torch.Tensor]")

# Patch chronos2/model.py
model_path = "chronos-forecasting/src/chronos/chronos2/model.py"
replace_in_file(model_path, "from typing import cast", "from typing import cast, Optional, Tuple, Union")
replace_in_file(model_path, "from typing import List, Optional, Tuple, Union", "from typing import List, Optional, Tuple, Union") # Check if Union missing
replace_in_file(model_path, "hidden_states: torch.Tensor | None = None", "hidden_states: Optional[torch.Tensor] = None")
replace_in_file(model_path, "time_self_attn_weights: torch.Tensor | None = None", "time_self_attn_weights: Optional[torch.Tensor] = None")
replace_in_file(model_path, "group_self_attn_weights: torch.Tensor | None = None", "group_self_attn_weights: Optional[torch.Tensor] = None")
replace_in_file(model_path, "last_hidden_state: torch.Tensor | None = None", "last_hidden_state: Optional[torch.Tensor] = None")
replace_in_file(model_path, "all_time_self_attn_weights: tuple[torch.Tensor, ...] | None = None", "all_time_self_attn_weights: Optional[tuple[torch.Tensor, ...]] = None")
replace_in_file(model_path, "all_group_self_attn_weights: tuple[torch.Tensor, ...] | None = None", "all_group_self_attn_weights: Optional[tuple[torch.Tensor, ...]] = None")
replace_in_file(model_path, "attention_mask: torch.Tensor | None = None", "attention_mask: Optional[torch.Tensor] = None")
replace_in_file(model_path, "position_ids: torch.Tensor | None = None", "position_ids: Optional[torch.Tensor] = None")
replace_in_file(model_path, "loss: torch.Tensor | None = None", "loss: Optional[torch.Tensor] = None")
replace_in_file(model_path, "quantile_preds: torch.Tensor | None = None", "quantile_preds: Optional[torch.Tensor] = None")
replace_in_file(model_path, "enc_time_self_attn_weights: tuple[torch.Tensor, ...] | None = None", "enc_time_self_attn_weights: Optional[tuple[torch.Tensor, ...]] = None")
replace_in_file(model_path, "enc_group_self_attn_weights: tuple[torch.Tensor, ...] | None = None", "enc_group_self_attn_weights: Optional[tuple[torch.Tensor, ...]] = None")
replace_in_file(model_path, "context_mask: torch.Tensor | None", "context_mask: Optional[torch.Tensor]")
replace_in_file(model_path, "group_ids: torch.Tensor | None", "group_ids: Optional[torch.Tensor]")
replace_in_file(model_path, "future_covariates: torch.Tensor | None", "future_covariates: Optional[torch.Tensor]")
replace_in_file(model_path, "future_covariates_mask: torch.Tensor | None", "future_covariates_mask: Optional[torch.Tensor]")
replace_in_file(model_path, "future_target: torch.Tensor | None", "future_target: Optional[torch.Tensor]")
replace_in_file(model_path, "future_target_mask: torch.Tensor | None", "future_target_mask: Optional[torch.Tensor]")
replace_in_file(model_path, "group_ids : torch.Tensor | None", "group_ids : Optional[torch.Tensor]")

# Patch chronos2/layers.py
layers_path = "chronos-forecasting/src/chronos/chronos2/layers.py"
replace_in_file(layers_path, "from dataclasses import dataclass", "from dataclasses import dataclass\nfrom typing import Optional, Tuple, Union")
replace_in_file(layers_path, "from typing import Optional, Tuple", "from typing import Optional, Tuple, Union") # Check if Union missing
replace_in_file(layers_path, "hidden_states: torch.Tensor | None = None", "hidden_states: Optional[torch.Tensor] = None")
replace_in_file(layers_path, "attn_weights: torch.Tensor | None = None", "attn_weights: Optional[torch.Tensor] = None")
replace_in_file(layers_path, "encoder_states: torch.Tensor | None = None", "encoder_states: Optional[torch.Tensor] = None")
replace_in_file(layers_path, "position_ids: torch.Tensor | None = None", "position_ids: Optional[torch.Tensor] = None")

# Patch chronos2/trainer.py
trainer_path = "chronos-forecasting/src/chronos/chronos2/trainer.py"
# trainer.py: def get_eval_dataloader(self, eval_dataset: str | Dataset | None = None) -> DataLoader:
replace_in_file(trainer_path, "eval_dataset: str | Dataset | None = None", "eval_dataset: Optional[Union[str, Dataset]] = None")
replace_in_file(trainer_path, "from typing import Any, Dict, List, Optional, Tuple, Union", "from typing import Any, Dict, List, Optional, Tuple, Union") 

# Boto utils
boto_path = "chronos-forecasting/src/chronos/boto_utils.py"
replace_in_file(boto_path, "boto3_session: boto3.Session | None = None", "boto3_session: Optional[boto3.Session] = None")

print("Manual patching complete.")
