from pathlib import Path

def load_prompt(
    prompt_set: str,
    prompt_name: str,
) -> str:

    path = Path("prompts") / prompt_set / prompt_name

    if not path.exists():
        raise FileNotFoundError(
            f"Prompt not found: {path}"
)

    return path.read_text(encoding="utf-8")