from pathlib import Path
from evaluation.model_dataset import Dataset

REQUIRED_DATASETS = [
    "README.txt",
    "data.csv",
]

def get_datasets() -> list:
    datasets_dir = Path("evaluation/datasets")

    datasets = []
    validation_errors = []

    for folder in datasets_dir.iterdir():

        if not folder.is_dir():
            continue
        
        if folder.name.startswith("_"):
            print(f"Skipping dataset: {folder.name}")
            continue

        missing = [
            filename
            for filename in REQUIRED_DATASETS
            if not (folder / filename).exists()
        ]

        if missing:
            validation_errors.append(
                {
                    "dataset_set": folder.name,
                    "missing": missing,
                }
            )
            continue

        datasets.append(
            Dataset(
                name=folder.name,
                tabular_file=folder / "data.csv",
                readme_file=folder / "README.txt",
            )
        )

    if validation_errors:
        lines = ["Dataset validation failed."]

        for error in validation_errors:
            lines.append("")
            lines.append(
                f"Dataset set: {error['dataset_set']}"
            )

            for filename in error["missing"]:
                lines.append(f"  - {filename}")

        raise FileNotFoundError("\n".join(lines))

    return datasets