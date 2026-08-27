from dataclasses import asdict
import json

def save_matches(
    matches,
    output_file: str,
) -> None:

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as handle:

        json.dump(
            [asdict(record) for record in matches],
            handle,
            indent=2
        )