from dataclasses import asdict
import json

def save_tabular_profile(
    tabular_profile,
    output_file: str,
) -> None:

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as handle:

        json.dump(
            asdict(tabular_profile),
            handle,
            indent=2
        )