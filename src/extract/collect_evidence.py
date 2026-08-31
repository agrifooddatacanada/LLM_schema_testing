from pathlib import Path
from src.llm.load_prompt import load_prompt
from src.extract.models_evidence import EvidenceRecord
from src.llm.client import llm_generate
from evaluation.models_experiment_config import ExperimentConfig
from src.extract.json_utils import parse_json_response

def collect_evidence(
    readme_profile,
    entities,
    *,
    prompt_set: str,
    output_dir,
    experiment_config: ExperimentConfig
) -> list:

    all_evidence=[]

    template = load_prompt(
        prompt_set,
        "extract_evidence.txt",
    )

    for entity in entities:

        prompt = template.format(
            document=readme_profile.content,
            entity=entity.name
        )

        print(f"\nSending to LLM for entity: {entity.name}")
        response=llm_generate(
            prompt,
            model=experiment_config.model,
            temperature=experiment_config.temperature,
            max_tokens=1000
            )

        try:
            evidence_data = parse_json_response(response)

        except Exception:
            with open(
                output_dir / "failed_evidence_responses.txt", 
                "a", 
                encoding="utf-8"
            ) as f:
                f.write(f"\n\n=== {entity.name} ===\n")
                f.write(f"ERROR: {e}\n\n")
                f.write(response)
            continue


        for item in evidence_data:
            evidence=EvidenceRecord(
                entity_name=entity.name,
                evidence_text=item["evidence_text"],
                source_section=item["source_section"],
                source_file=readme_profile.source_file
            )
            print(
                f"Found {len(evidence_data)} evidence items for {entity.name}"
            )
            
            all_evidence.append(
                evidence
            )

    return all_evidence