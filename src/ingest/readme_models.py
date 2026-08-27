from dataclasses import dataclass

@dataclass
class ReadmeProfile:
    source_file: str
    content: str
    character_count: int
    line_count: int