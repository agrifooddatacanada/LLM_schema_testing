from src.metadata.models_schema_metadata import SchemaMetadata
from src.extract.json_utils import parse_json_response
from src.llm.client import llm_generate
from src.llm.load_prompt import load_prompt
from evaluation.models_experiment_config import ExperimentConfig
from src.ingest.readme_models import ReadmeProfile

def extract_schema_metadata(
    *,
    dataset_name: str,
    readme_profile: ReadmeProfile,
    column_names: list[str],
    prompt_set: str,
    experiment_config: ExperimentConfig,
) -> SchemaMetadata:

    template = load_prompt(
        prompt_set,
        "extract_schema_metadata.txt",
        )
    
    prompt = template.format(
        dataset_name=dataset_name,
        readme_content=readme_profile.content,
        column_names="\n".join(column_names),
    )

    response = llm_generate(
        prompt,
        model=experiment_config.model,
        temperature=experiment_config.temperature,
        max_tokens=1000,
    )

    data = parse_json_response(response)

    return SchemaMetadata(
        title=data.get("title", ""),
        description=data.get("description", ""),
    )
