from pathlib import Path
from evaluation.markdown_utils import escape_markdown

def write_runs_report(
    results,
    report_file: Path,
) -> None:

    lines = []

    lines.append("# Experiment Comparison Report")
    lines.append("")

    datasets = sorted(
        {
            result.dataset_name
            for result in results
        }
    )

    for dataset_name in datasets:
        lines.append("")
        lines.append(f"# Dataset: {escape_markdown(dataset_name)}")
        lines.append("")

        column_names = set()

        # collect all columns for this dataset
        for result in results:

            if result.dataset_name != dataset_name:
                continue

            for description in result.metadata.descriptions:
                column_names.add(description.column_name)
            
            for unit in result.metadata.units:
                column_names.add(unit.column_name)
            
        # generate report for each column
        for column_name in sorted(column_names):
            lines.append(f"## Column: {column_name}")

            lines.append("")
            lines.append("### Descriptions")
            lines.append("")
            lines.append("| Prompt Set | Description |")
            lines.append("|------------|-------------|")
            
            
            for result in results:

                if result.dataset_name != dataset_name:
                    continue

                description_text = ""

                for description in result.metadata.descriptions:

                    if description.column_name == column_name:
                        description_text = (
                            description.description
                        )
                        break

                lines.append(
                    f"| {result.prompt_set} | "
                    f"{description_text} |"
                )
                
            lines.append("")
            lines.append("### Units")
            lines.append("")
            lines.append("| Prompt Set | Unit |")
            lines.append("|------------|------|")

            for result in results:

                if result.dataset_name != dataset_name:
                    continue

                unit_text = ""

                for unit in result.metadata.units:

                    if unit.column_name == column_name:
                        unit_text = unit.unit

                lines.append(
                    f"| {result.prompt_set} | "
                    f"{unit_text} |"
                )
            lines.append("")
            lines.append("---")
            lines.append("")
    report_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )