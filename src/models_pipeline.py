from dataclasses import dataclass

from src.extract.models_entities import DiscoveredEntity
from src.extract.models_evidence import EvidenceRecord
from src.extract.models_column_match import ColumnMatch
from src.extract.build_column_contexts import build_column_contexts


@dataclass
class PipelineResult:
    entities: list[DiscoveredEntity]
    evidence: list[EvidenceRecord]
    matches: list[ColumnMatch]
    contexts: list[ColumnContext]