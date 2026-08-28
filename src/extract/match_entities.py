from src.extract.models_column_match import ColumnMatch
from src.extract.json_utils import parse_json_response
from src.llm.client import llm_generate
from src.llm.load_prompt import load_prompt

def match_entities(
        entities,
        evidence,
        tabular_profile,
        *,
        prompt_set: str,
        output_dir,
    ) -> list:

    template = load_prompt(
        prompt_set,
        "matching_entities.txt",
    )

    column_text = "\n".join(
        column.column_name
        for column in tabular_profile.columns
    )

    all_matches = []

    for entity in entities:

        entity_evidence = [
            record.evidence_text
            for record in evidence
            if record.entity_name == entity.name
        ]

        prompt = template.format(
            entity=entity.name,
            evidence="\n".join(entity_evidence),
            columns=column_text,
        )

        print(f"\n------")
        print(f"Sending to LLM for entity: {entity.name} to match column name")
        response=llm_generate(
            prompt,
            max_tokens=1000
        )
        
        try:
            column_data = parse_json_response(response)

        except Exception:
            with open(
                output_dir / "failed_column_responses.txt", 
                "a", 
                encoding="utf-8"
            ) as f:
                f.write(f"\n\n=== {entity.name} ===\n")
                f.write(f"ERROR: {e}\n\n")
                f.write(response)
            continue
        
        column_data = parse_json_response(response)

        match = ColumnMatch(
            entity_name=entity.name,
            column_name=column_data["column_name"],
            llm_rationale=column_data["rationale"],
            evidence_used=entity_evidence,
        )

        #print(f"Matched entity: {entity.name}")
        #print(f"Column selected: {column_data['column_name']}")
        #print(f"Rationale: {column_data['rationale']}")

        all_matches.append(
            match
        )

    return all_matches
