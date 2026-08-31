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
                "config",
                "model",
                "temperature",
                "prompt_set",
                "attribute",
                "column",
                "datatype",
                "description",
                "unit",
            ],
        )

        writer.writeheader()

        for result in results:

            # build lookups so we can match descriptions and units
            attributes = {
                a.column_name: a.attribute
                for a in result.metadata.attributes
            }
            
            descriptions = {
                d.column_name: d.description
                for d in result.metadata.descriptions
            }

            units = {
                u.column_name: u.unit
                for u in result.metadata.units
            }

            datatypes = {
                dt.column_name: dt.datatype
                for dt in result.metadata.datatypes
            }

            all_columns = (
                set(descriptions.keys()) 
                | set(units.keys())
                | set(datatypes.keys())
                | set(attributes.keys())
            )

            for column_name in sorted(all_columns):

                writer.writerow(
                    {
                        "dataset": result.dataset_name,
                        "config": result.experiment_config.name,
                        "model": result.experiment_config.model,
                        "temperature": result.experiment_config.temperature,
                        "prompt_set": result.prompt_set,
                        "attribute": attributes.get(
                            column_name,
                            "",
                        ),
                        "column": column_name,
                        "datatype": datatypes.get(
                            column_name,
                            "",
                        ),
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