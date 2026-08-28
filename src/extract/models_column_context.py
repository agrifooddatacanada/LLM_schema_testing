from dataclasses import dataclass

from src.extract.models_evidence import EvidenceRecord
from src.ingest.tabular_models import ColumnProfile

@dataclass
class ColumnContext:
    column_profile: ColumnProfile
    matches: list[ColumnMatch]
    evidence: list[EvidenceRecord]