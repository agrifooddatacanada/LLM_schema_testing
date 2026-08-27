from datetime import datetime
from pathlib import Path
from evaluation.collect_prompts import get_prompt_sets
from evaluation.collect_evaluation_datasets import get_datasets
from src.orchestrator import run_pipeline
from evaluation.write_report import (write_report, safe_filename,)

prompt_sets = get_prompt_sets()
dataset_sets = get_datasets()

print(dataset_sets)

run_id = datetime.now().strftime(
    "%Y-%m-%d_%H-%M-%S"
)

run_root = (
    Path("evaluation/runs")
    / run_id
)

print(f"Experiment Run: {run_id}")

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