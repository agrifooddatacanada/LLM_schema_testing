from datetime import datetime
from pathlib import Path
from evaluation.collect_prompts import get_prompt_sets
from evaluation.collect_evaluation_datasets import get_datasets
from src.orchestrator import run_pipeline
from evaluation.write_report import (write_report, safe_filename,)
from evaluation.csv_runs_report_writer import write_runs_csv
from src.metadata.run_metadata_pipeline import run_metadata_pipeline
from evaluation.models_experiment_result import ExperimentResult
from evaluation.markdown_runs_report_writer import write_runs_report

prompt_sets = get_prompt_sets()
dataset_sets = get_datasets()

run_id = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

run_root = (
    Path("evaluation/runs")
    / run_id
)

print(f"Experiment Run: {run_id}")

all_results = []

for prompt_set in prompt_sets:

    for dataset in dataset_sets:
        print(
            f"Running dataset={dataset.name}"
            f"prompt_set={prompt_set}"
        )

        output_dir = (
            run_root
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
        )

        metadata_result = run_metadata_pipeline(
            result.contexts,
            prompt_set=prompt_set,
        )

        all_results.append(
            ExperimentResult(
                dataset_name=dataset.name,
                prompt_set=prompt_set,
                metadata=metadata_result,
            )
        )


        report_name = (
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
        )


print("\nEXPERIMENT RESULTS")

for result in all_results:

    print("\n====================")
    print(f"Dataset: {result.dataset_name}")
    print(f"Prompt: {result.prompt_set}")

    print("\nDescriptions:")

    for description in result.metadata.descriptions:
        print(
            f"  {description.column_name}: "
            f"{description.description}"
        )

    print("\nUnits:")

    for unit in result.metadata.units:
        print(
            f"  {unit.column_name}: "
            f"{unit.unit}"
        )


write_runs_report(
    all_results,
    run_root / "comparison_report.md",
)


write_runs_csv(
    all_results,
    run_root / "comparison_report.csv",
    )