from pathlib import Path
from src.ingest.tabular import profile_tabular
from src.ingest.readme import profile_readme
from src.extract.collect_entities import collect_entities
from src.extract.collect_evidence import collect_evidence
from src.extract.match_entities import match_entities
from src.extract.save_entities import save_entities
from src.extract.save_evidence import save_evidence
from src.extract.save_readme_profile import save_readme_profile
from src.extract.save_tabular_profile import save_tabular_profile
from src.extract.save_matches import save_matches
from src.models_pipeline import PipelineResult

def run_pipeline(
    tabular_file: str,
    readme_file: str,
    *,
    prompt_set: str="baseline",
    output_dir: Path,
) -> None:

    # get information about the tabular data file
    tabular_profile = profile_tabular(tabular_file)

    save_tabular_profile(
        tabular_profile,
        output_dir / "tabular_profile.json"
    )

    # get the full text of the readme file and some additional information
    readme_profile = profile_readme(readme_file)

    save_readme_profile(
        readme_profile,
        output_dir / "readme_profile.json"
    )

    # This code takes the column header names, adds them to a prompt and
    # generates a list of entities present in the readme file.
    entities = collect_entities(
        readme_profile,
        tabular_profile,
        prompt_set=prompt_set,
    )

    save_entities(
        entities,
        output_dir / "entities.json"
        )

    print("\nThe entities found in the Readme:")
    for entity in entities:
        print(entity.name)

    # This code takes each entity and searches the readme with a prompt
    # and generates evidence for each entity but does not classify what type 
    # of evidence it has found.
    all_evidence=collect_evidence(
        readme_profile,
        entities,
        prompt_set=prompt_set,
        output_dir=output_dir,
    )

    save_evidence(
        all_evidence,
        output_dir / "evidence.json"
    )

    print("\nEvidence found:")

    for evidence in all_evidence:
        print("\n---")
        print("Entity:", evidence.entity_name)
        print("Evidence Text:", evidence.evidence_text)
        print("Evidence Section:", evidence.source_section)

    # This code takes entities and tabular profile extracted from the data table
    # and matches them to entities extracted from the readme text file
    matches = match_entities(
        entities,
        all_evidence,
        tabular_profile,
        prompt_set=prompt_set,
        output_dir=output_dir,
    )

    save_matches(
        matches,
        output_dir / "matches.json"
    )

    return PipelineResult(
        entities=entities,
        evidence=all_evidence,
        matches=matches,
    )


if __name__ == "__main__":
    run_pipeline(
        r"data\input\test_data\cfia_vibrio_data_public.csv",
        r"data\input\test_data\READMEvib.txt",
        output_dir=Path("data/intermediate")
        )