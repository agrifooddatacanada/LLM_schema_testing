from src.extract.models_column_context import ColumnContext
from src.metadata.models_datatype import DatatypeMetadata
from src.extract.json_utils import parse_json_response
from src.llm.client import llm_generate
from src.llm.load_prompt import load_prompt
from evaluation.models_experiment_config import ExperimentConfig

ALLOWED_DATATYPES = {
    "Text",
    "Numeric",
    "Boolean",
    "BinaryFile",
    "DateTime",
}

def extract_datatypes(
    contexts: list[ColumnContext],
    *,
    prompt_set: str,
    experiment_config: ExperimentConfig,
) -> list[DatatypeMetadata]:

    template = load_prompt(
        prompt_set,
        "extract_datatypes.txt",
        )

    results = []

    for context in contexts:

        datatype = (
            context.column_profile.inferred_datatypes[0]
            if context.column_profile.inferred_datatypes
            else "Text"
        )

        if datatype not in ALLOWED_DATATYPES:
            datatype = "Text"


        results.append(
            DatatypeMetadata(
                column_name=context.column_profile.column_name,
                datatype=datatype,
            )
        )

    return results