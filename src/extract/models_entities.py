from dataclasses import dataclass

@dataclass
class DiscoveredEntity:
    name: str

@dataclass
class HarmonizedEntity:
    canonical_name: str
    source_terms: list[str]