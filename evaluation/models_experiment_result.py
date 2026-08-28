from dataclasses import dataclass

from src.metadata.models_metadata_result import MetadataResult


@dataclass
class ExperimentResult:
    dataset_name: str
    prompt_set: str
    metadata: MetadataResult
