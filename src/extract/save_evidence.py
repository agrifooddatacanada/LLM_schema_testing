from dataclasses import asdict
import json

def save_evidence(
    evidence_records,
    output_file: str,
) -> None:

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as handle:

        json.dump(
            [asdict(record) for record in evidence_records],
            handle,
            indent=2
        )