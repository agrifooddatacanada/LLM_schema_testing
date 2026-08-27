from dataclasses import asdict
import json

from ingest.tabular import profile_tabular

def run_pipeline(file_path: str) -> None:
    profile = profile_tabular(file_path)

    print(f"File: {profile.source_file}")

    print(json.dumps(asdict(profile), indent=2))

    print("\nColumns:")
    for column in profile.columns:
        print(f" - {column.column_name}")


if __name__ == "__main__":
    run_pipeline(r"data\input\vibrio\cfia_vibrio_data_public.csv")