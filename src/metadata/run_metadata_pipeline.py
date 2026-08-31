from src.extract.models_column_context import ColumnContext
from evaluation.models_experiment_config import ExperimentConfig
from src.metadata.models_metadata_result import MetadataResult
from src.metadata.extract_descriptions import extract_descriptions
from src.metadata.extract_units import extract_units
from src.metadata.extract_attributes import extract_attributes
from src.metadata.extract_datatypes import extract_datatypes
from evaluation.collect_experiment_configs import get_experiment_configs

def run_metadata_pipeline(
    contexts: list[ColumnContext],
    *,
    prompt_set: str,
    experiment_config: ExperimentConfig
) -> MetadataResult:

    print("\n---")
    print("\n Sending to LLM for Metadata Extraction")

    descriptions = extract_descriptions(
        contexts,
        prompt_set=prompt_set,
        experiment_config=experiment_config,
    )

    units = extract_units(
        contexts,
        prompt_set=prompt_set,
        experiment_config=experiment_config,
    )

    attributes = extract_attributes(
        contexts,
        prompt_set=prompt_set,
        experiment_config=experiment_config,
    )

    datatypes = extract_datatypes(
        contexts,
        prompt_set=prompt_set,
        experiment_config=experiment_config,
    )

    return MetadataResult(
        descriptions=descriptions,
        units=units,
        attributes=attributes,
        datatypes=datatypes,
    )