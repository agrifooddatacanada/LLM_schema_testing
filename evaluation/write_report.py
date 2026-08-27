import re
from pathlib import Path
from src.models_pipeline import PipelineResult

def safe_filename(text: str) -> str:
    return re.sub(
        r"[^a-zA-Z0-9_-]",
        "_",
        text
    )

def write_report(
    result: PipelineResult,
    dataset_name: str,
    prompt_set: str,
    report_file: Path,
) -> None:

    lines = []

    lines.append("# Experiment Report")
    lines.append("")
    lines.append(f"Dataset: {dataset_name}")
    lines.append(f"Prompt Set: {prompt_set}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")

    lines.append(f"Entities: {len(result.entities)}")
    lines.append(f"Evidence Records: {len(result.evidence)}")
    lines.append(f"Matches: {len(result.matches)}")
    lines.append("")

    lines.append("## Entities")
    lines.append("")

    for entity in result.entities:
        lines.append(f"- {entity.name}")
    
    lines.append("")
    lines.append("## Matches")
    lines.append("")

    for match in result.matches:
        column_name = match.column_name or "[NO MATCH]"

        lines.append(
            f"- {match.entity_name} -> {column_name}"
        )

    lines.append("")

    lines.append("")
    lines.append("## Unmatched Entities")
    lines.append("")

    for match in result.matches:

        if match.column_name is None:

            lines.append(
                f"- {match.entity_name}"
            )

    lines.append("")

    lines.append("")
    lines.append("## Match Rationales")
    lines.append("")

    for match in result.matches:

        lines.append(
            f"### {match.entity_name}"
        )

        lines.append("")

        lines.append(
            f"Matched Column: {match.column_name}"
        )

        lines.append("")

        lines.append(match.llm_rationale)

        lines.append("")

    lines.append("")
    lines.append("## Evidence")
    lines.append("")

    for entity in result.entities:

        lines.append(f"### {entity.name}")
        lines.append("")

        for evidence in result.evidence:

            if evidence.entity_name == entity.name:

                lines.append(
                    f"- {evidence.evidence_text}"
                )

        lines.append("")

    report_file.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )