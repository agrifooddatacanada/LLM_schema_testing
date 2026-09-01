from dataclasses import dataclass
from src.metadata.models_metadata_result import MetadataResult
from evaluation.models_experiment_config import ExperimentConfig

@dataclass
class ExperimentResult:
    dataset_name: str
    prompt_set: str
    experiment_config: ExperimentConfig
    metadata: MetadataResult
    elapsed_seconds: float
