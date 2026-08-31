from src.extract.models_column_context import ColumnContext
from src.metadata.models_description import DescriptionMetadata

from src.extract.json_utils import parse_json_response
from src.llm.client import llm_generate
from src.llm.load_prompt import load_prompt
from evaluation.models_experiment_config import ExperimentConfig


def extract_descriptions(
    contexts: list[ColumnContext],
    *,
    prompt_set: str,
    experiment_config: ExperimentConfig
    ) -> list[DescriptionMetadata]:
    
    template = load_prompt(
            prompt_set,
            "extract_descriptions.txt",
        )

    descriptions = []

    for context in contexts:

        evidence_text = "\n\n".join(
            record.evidence_text
            for record in context.evidence
        )

        matched_entities = "\n".join(
            match.entity_name
            for match in context.matches
        )

        sample_values = "\n".join(
            str(value)
            for value in context.column_profile.sample_values[:5]
        )

        prompt = template.format(
            column_name=context.column_profile.column_name,
            entities=matched_entities,
            sample_values=sample_values,
            datatypes=", ".join(
                context.column_profile.inferred_datatypes
            ),
            evidence=evidence_text,
        )


        response = llm_generate(
            prompt,
            model=experiment_config.model,
            temperature=experiment_config.temperature,
            max_tokens=1000,
        )

        description_data = parse_json_response(
            response
        )

        descriptions.append(
            DescriptionMetadata(
                column_name=context.column_profile.column_name,
                description=description_data["description"],
            )
        )

    return descriptions
