from dataclasses import dataclass

@dataclass
class ColumnMatch:
    entity_name: str
    column_name: str | None
    llm_rationale: str
    evidence_used: list[str]