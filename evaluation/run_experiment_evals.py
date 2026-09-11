from datetime import datetime
from pathlib import Path
import json
import time
from evaluation.collect_prompts import get_prompt_sets
from evaluation.collect_evaluation_datasets import get_datasets
from evaluation.collect_experiment_configs import get_experiment_configs
from evaluation.models_experiment_config import ExperimentConfig
from src.orchestrator import run_pipeline
from evaluation.write_report import (write_report, safe_filename,)
from evaluation.csv_runs_report_writer import write_runs_csv
from src.metadata.run_metadata_pipeline import run_metadata_pipeline
from evaluation.models_experiment_result import ExperimentResult
from evaluation.markdown_runs_report_writer import write_runs_report
from src.schemas.oca.generate_oca_schema import generate_oca_schema
from evaluation.csv_runs_schema_report_writer import write_schema_csv
from evaluation.load_reference_metadata import load_reference_metadata

prompt_sets = get_prompt_sets()
dataset_sets = get_datasets()
experiment_configs = get_experiment_configs()

run_id = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

run_root = (
    Path("evaluation/runs")
    / run_id
)

print(f"\nExperiment Run: {run_id}\n")

all_results = []
reference_datasets_loaded = set()

for experiment_config in experiment_configs:

    for prompt_set in prompt_sets:

        for dataset in dataset_sets:

            print("\n" + "=" * 80)
            print(
                f"RUNNING "
                f"dataset={dataset.name} "
                f"prompt={prompt_set} "
                f"model={experiment_config.name}"
            )
            print("=" * 80)

            if (
                dataset.reference_schema_file
                and dataset.name not in reference_datasets_loaded
            ):
                reference_metadata = load_reference_metadata(
                    dataset.reference_schema_file
                )

                reference_result = ExperimentResult(
                    dataset_name=dataset.name,
                    prompt_set="reference",
                    experiment_config=ExperimentConfig(
                        name="human",
                        model="human",
                        temperature=0.0,
                    ),
                    metadata=reference_metadata,
                    elapsed_seconds=0.0,
                    is_reference=True,
                )

                all_results.append(reference_result)
                reference_datasets_loaded.add(dataset.name)
            
            start_time = time.perf_counter()
            
            output_dir = (
                run_root
                / experiment_config.name
                / prompt_set
                / dataset.name
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            result = run_pipeline(
                tabular_file=dataset.tabular_file,
                readme_file=dataset.readme_file,
                prompt_set=prompt_set,
                output_dir=output_dir,
                experiment_config=experiment_config,
            )

            print(
                f"Entities: {len(result.entities)}"
            )

            print(
                f"Matches: {len(result.matches)}"
            )

            elapsed_seconds = time.perf_counter() - start_time

            print(f"Run took {elapsed_seconds:.2f} seconds")
