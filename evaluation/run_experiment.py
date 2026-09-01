from datetime import datetime
from pathlib import Path
import json
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

print(f"Experiment Run: {run_id}")

all_results = []

for experiment_config in experiment_configs:

    for prompt_set in prompt_sets:

        for dataset in dataset_sets:

            print(
                f"Running config={experiment_config.name} "
                f"dataset={dataset.name} "
                f"prompt_set={prompt_set}"
            )

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

            metadata_result = run_metadata_pipeline(
                result.contexts,
                dataset_name=dataset.name,
                readme_profile=result.readme_profile,
                prompt_set=prompt_set,
                experiment_config=experiment_config,
            )

            all_results.append(
                ExperimentResult(
                    dataset_name=dataset.name,
                    prompt_set=prompt_set,
                    experiment_config=experiment_config,
                    metadata=metadata_result,
                )
            )

            report_name = (
                f"{safe_filename(experiment_config.name)}_"
                f"{safe_filename(prompt_set)}_"
                f"{safe_filename(dataset.name)}.md"
            )

            report_file = (
                run_root
                / report_name
            )

            write_report(
                result=result,
                dataset_name=dataset.name,
                prompt_set=prompt_set,
                report_file=report_file,
                experiment_config=experiment_config,
            )

            schema = generate_oca_schema(
                metadata_result,
                result.contexts,
            )

            schema_file = output_dir / f"{safe_filename(dataset.name)}_oca_package_schema.json"

            with open(schema_file, "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2)

            print(f"Schema written to {schema_file}")


write_runs_report(
    all_results,
    run_root / "schema_contents_report.md",
)

write_runs_csv(
    all_results,
    run_root / "schema_columns_report.csv",
    )

write_schema_csv(
    all_results,
    run_root / "schema_metadata_report.csv",
)
