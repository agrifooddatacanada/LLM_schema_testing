from dataclasses import dataclass

@dataclass
class EvidenceRecord:
    entity_name: str
    evidence_text: str
    source_section: str
    source_file: str