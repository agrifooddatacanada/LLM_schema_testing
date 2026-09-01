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

        lines.append(f"# Dataset: {escape_markdown(dataset_name)}")
        lines.append("")
        lines.append("## Schema Metadata")
        lines.append("")
        lines.append(
            "| Config | Model | Temperature | Prompt Set | Title | Description | Elapsed Seconds |"
        )
        lines.append(
            "|--------|-------|-------------|------------|-------|-------------|-------------|"
        )

        for result in results:

            if result.dataset_name != dataset_name:
                continue

            title = ""
            description = ""
            elapsed_seconds = ""

            if result.metadata.schema_metadata:
                title = result.metadata.schema_metadata.title
                description = result.metadata.schema_metadata.description
                elapsed_seconds = result.elapsed_seconds

            lines.append(
                f"| {escape_markdown(result.experiment_config.name)} "
                f"| {escape_markdown(result.experiment_config.model)} "
                f"| {result.experiment_config.temperature} "
                f"| {escape_markdown(result.prompt_set)} "
                f"| {escape_markdown(title)} "
                f"| {escape_markdown(description)} "
                f"| {elapsed_seconds:.2f} seconds"
            )

        lines.append("")

        column_names = set()

        for result in results:

            if result.dataset_name != dataset_name:
                continue

            column_names.update(
                attribute.column_name
                for attribute in result.metadata.attributes
            )
            
            column_names.update(
                description.column_name
                for description in result.metadata.descriptions
            )

            column_names.update(
                unit.column_name
                for unit in result.metadata.units
            )

            column_names.update(
                datatype.column_name
                for datatype in result.metadata.datatypes
            )

        for column_name in sorted(column_names):

            lines.append(
                f"## Column: {escape_markdown(column_name)}"
            )
            lines.append("")

            lines.append(
                "| Config | Model | Temperature | Prompt Set | Attribute | Description | Unit | Datatype |"
            )
            lines.append(
                "|--------|-------|-----|------------|-----------|-------------|------|----------|"
            )

            for result in results:

                if result.dataset_name != dataset_name:
                    continue

                description_text = ""
                unit_text = ""
                datatype_text = ""
                attribute_text = ""

                
                for attribute in result.metadata.attributes:
                    if attribute.column_name == column_name:
                        attribute_text = attribute.attribute
                        break

                for description in result.metadata.descriptions:
                    if description.column_name == column_name:
                        description_text = description.description
                        break

                for unit in result.metadata.units:
                    if unit.column_name == column_name:
                        unit_text = unit.unit
                        break

                for datatype in result.metadata.datatypes:
                    if datatype.column_name == column_name:
                        datatype_text = datatype.datatype
                        break

                lines.append(
                    f"| {escape_markdown(result.experiment_config.name)} "
                    f"| {escape_markdown(result.experiment_config.model)} "
                    f"| {result.experiment_config.temperature} "
                    f"| {escape_markdown(result.prompt_set)} "
                    f"| {escape_markdown(attribute_text)} "
                    f"| {escape_markdown(description_text)} "
                    f"| {escape_markdown(unit_text)} "
                    f"| {escape_markdown(datatype_text)} |"
                )

            lines.append("")
            lines.append("---")
            lines.append("")

    report_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )