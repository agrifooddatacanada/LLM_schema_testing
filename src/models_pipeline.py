from dataclasses import dataclass

from src.extract.models_entities import DiscoveredEntity
from src.extract.models_evidence import EvidenceRecord
from src.extract.models_column_match import ColumnMatch


@dataclass
class PipelineResult:
    entities: list[DiscoveredEntity]
    evidence: list[EvidenceRecord]
    matches: list[ColumnMatch]