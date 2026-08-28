from dataclasses import dataclass, field

from src.metadata.models_description import DescriptionMetadata
from src.metadata.models_unit import UnitMetadata


@dataclass
class MetadataResult:
    descriptions: list[DescriptionMetadata]
    units: list[UnitMetadata] = field(default_factory=list)