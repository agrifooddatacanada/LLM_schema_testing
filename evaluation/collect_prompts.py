from pathlib import Path

REQUIRED_PROMPTS = [
    "discover_entities.txt",
    "extract_evidence.txt",
    "matching_entities.txt",
]

def get_prompt_sets() -> list:
    prompts_dir = Path("prompts")

    prompt_sets = []
    validation_errors = []

    for folder in prompts_dir.iterdir():

        if not folder.is_dir():
            continue

        missing = [
            filename
            for filename in REQUIRED_PROMPTS
            if not (folder / filename).exists()
        ]

        if missing:
            validation_errors.append(
                {
                    "prompt_set": folder.name,
                    "missing": missing,
                }
            )
            continue

        prompt_sets.append(folder.name)

    if validation_errors:
        lines = ["Prompt validation failed."]

        for error in validation_errors:
            lines.append("")
            lines.append(
                f"Prompt set: {error['prompt_set']}"
            )

            for filename in error["missing"]:
                lines.append(f"  - {filename}")

        raise FileNotFoundError("\n".join(lines))

    return prompt_sets