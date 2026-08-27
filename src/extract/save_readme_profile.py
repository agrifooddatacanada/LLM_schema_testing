from dataclasses import asdict
import json

def save_readme_profile(
    readme_profile,
    output_file: str,
) -> None:

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as handle:

        json.dump(
            asdict(readme_profile),
            handle,
            indent=2
        )