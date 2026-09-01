import csv
from pathlib import Path

def write_schema_csv(
    results,
    csv_file: Path,
) -> None:

    with open(csv_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dataset",
                "config",
                "model",
                "temperature",
                "prompt_set",
                "title",
                "description",
                "elapsed_seconds",
            ],
        )

        writer.writeheader()

        for result in results:

            title = ""
            description = ""

            if result.metadata.schema_metadata:
                title = result.metadata.schema_metadata.title
                description = result.metadata.schema_metadata.description

            writer.writerow(
                {
                    "dataset": result.dataset_name,
                    "config": result.experiment_config.name,
                    "model": result.experiment_config.model,
                    "temperature": result.experiment_config.temperature,
                    "prompt_set": result.prompt_set,
                    "title": title,
                    "description": description,
                    "elapsed_seconds": result.elapsed_seconds,
                }
            )