from dataclasses import dataclass
from pathlib import Path

@dataclass
class Dataset:
    name: str
    tabular_file: Path
    readme_file: Path