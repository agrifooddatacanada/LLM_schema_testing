import csv
from pathlib import Path

def write_runs_csv(
    results,
    csv_file: Path,
) -> None:

    with open(csv_file, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dataset",
                "prompt_set",
                "column",
                "description",
                "unit",
            ],
        )

        writer.writeheader()

        for result in results:

            # build lookups so we can match descriptions and units
            descriptions = {
                d.column_name: d.description
                for d in result.metadata.descriptions
            }

            units = {
                u.column_name: u.unit
                for u in result.metadata.units
            }

            all_columns = set(descriptions.keys()) | set(units.keys())

            for column_name in sorted(all_columns):

                writer.writerow(
                    {
                        "dataset": result.dataset_name,
                        "prompt_set": result.prompt_set,
                        "column": column_name,
                        "description": descriptions.get(
                            column_name,
                            "",
                        ),
                        "unit": units.get(
                            column_name,
                            "",
                        ),
                    }
                )