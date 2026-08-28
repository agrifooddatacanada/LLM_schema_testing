from src.extract.models_column_context import ColumnContext
from src.metadata.extract_descriptions import extract_descriptions
from src.metadata.extract_units import extract_units
from src.metadata.models_metadata_result import MetadataResult

def run_metadata_pipeline(
    contexts: list[ColumnContext],
    *,
    prompt_set: str,
) -> MetadataResult:

    descriptions = extract_descriptions(
        contexts,
        prompt_set=prompt_set,
    )

    units = extract_units(
        contexts,
        prompt_set=prompt_set,
    )

    print("\nUnits:")

    for unit in units:
        print(
            f"{unit.column_name}: "
            f"{unit.unit}"
        )

    return MetadataResult(
        descriptions=descriptions,
        units=units,
    )