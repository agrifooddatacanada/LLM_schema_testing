from pathlib import Path
from dataclasses import asdict
import json

from src.ingest.readme_models import ReadmeProfile

def read_text_file(path: Path) -> str:
    for encoding in ["utf-8", "cp1252", "latin-1"]:
        try:
            with path.open("r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            pass

    raise ValueError(f"Could not decode {path}")


def profile_readme(
    readme_path: str | Path, 
    output_path: str | Path | None = None,
) -> ReadmeProfile:

    path = Path(readme_path)

    if path.suffix.lower() != ".txt":
        raise ValueError(f"Unsupported readme file type: {path}")

    content = read_text_file(path)

    profile = ReadmeProfile(
        source_file=str(path),
        content=content,
        character_count=len(content),
        line_count=len(content.splitlines()),
    )

    if output_path is not None:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with output.open("w", encoding="utf-8") as handle:
            json.dump(asdict(profile), handle, indent=2)

    return profile