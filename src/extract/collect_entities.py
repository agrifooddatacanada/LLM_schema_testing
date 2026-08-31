from src.extract.models_entities import DiscoveredEntity
from src.llm.client import llm_generate
from src.llm.load_prompt import load_prompt
from src.extract.json_utils import parse_json_response
from evaluation.models_experiment_config import ExperimentConfig

def collect_entities(
    readme_profile,
    tabular_profile,
    *,
    prompt_set: str,
    experiment_config: ExperimentConfig
) -> list:

    ### Build Column Text
    column_text = "\n".join(
        column.column_name
        for column in tabular_profile.columns
    )

    template = load_prompt(
        prompt_set,
        "discover_entities.txt",
    )

    prompt = template.format(
        document=readme_profile.content,
        columns=column_text
    )

    print("sending to LLM to search for entities")
    response=llm_generate(
        prompt,
        model=experiment_config.model,
        temperature=experiment_config.temperature,
        max_tokens=1000
    )

    entity_data=parse_json_response(
        response
    )

    entities = []

    for item in entity_data:
        entities.append(
            DiscoveredEntity(
               name=item["entity_name"]
            )
        )

    return entities