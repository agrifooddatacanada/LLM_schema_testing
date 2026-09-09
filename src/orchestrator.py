from pathlib import Path
from src.ingest.tabular import profile_tabular
from src.ingest.readme import profile_readme
from evaluation.models_experiment_config import ExperimentConfig
from src.extract.collect_entities import collect_entities
from src.extract.collect_evidence import collect_evidence
from src.extract.match_entities import match_entities
from src.extract.save_entities import save_entities
from src.extract.save_evidence import save_evidence
from src.extract.save_readme_profile import save_readme_profile
from src.extract.save_tabular_profile import save_tabular_profile
from src.extract.save_matches import save_matches
from src.models_pipeline import PipelineResult
from src.extract.build_column_contexts import build_column_contexts
from src.extract.models_column_context import ColumnContext

def ensure_directories() -> None:
    required_dirs = [
        Path("data") / "intermediate",
        Path("data") / "output",
    ]

    for directory in required_dirs:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )


def run_pipeline(
    *,
    tabular_file: str,
    readme_file: str,
    prompt_set: str="baseline",
    output_dir: Path,
    experiment_config: ExperimentConfig,
) -> PipelineResult:
    print(
        f"ENTERING run_pipeline "
        f"readme={readme_file}"
    )

    ensure_directories()
    
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
        experiment_config=experiment_config,
    )

    save_entities(
        entities,
        output_dir / "entities.json"
        )

    print(
        f"\nENTITIES "
        f"dataset={Path(readme_file).parent.name}"
    )
    for entity in entities:
        print(
            f"  [{Path(readme_file).parent.name}] "
            f"{entity.name}"
        )

    all_evidence=collect_evidence(
        readme_profile,
        entities,
        prompt_set=prompt_set,
        output_dir=output_dir,
        experiment_config=experiment_config,
    )

    save_evidence(
        all_evidence,
        output_dir / "evidence.json"
    )

    matches = match_entities(
        entities,
        all_evidence,
        tabular_profile,
        prompt_set=prompt_set,
        output_dir=output_dir,
        experiment_config=experiment_config,
    )

    save_matches(
        matches,
        output_dir / "matches.json"
    )

    contexts = build_column_contexts(
        matches,
        all_evidence,
        tabular_profile,
    )

    print(
        f"\nLEAVING run_pipeline "
        f"readme={readme_file}"
    )

    return PipelineResult(
        readme_profile=readme_profile,
        entities=entities,
        evidence=all_evidence,
        matches=matches,
        contexts=contexts,
    )


if __name__ == "__main__":
    experiment_config = ExperimentConfig(
        name="manual",
        model="Qwen2.5-Omni-7B-Q4_K_M",
        temperature=0.0,
    )

    run_pipeline(
        tabular_file=Path("data") / "input" / "test_data" / "cfia_vibrio_data_public.csv",
        readme_file=Path("data") / "input" / "test_data" / "READMEvib.txt",
        output_dir=Path("data/intermediate"),
        experiment_config=experiment_config,
    )