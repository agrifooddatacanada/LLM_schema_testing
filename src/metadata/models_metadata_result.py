from dataclasses import dataclass, field

from src.metadata.models_description import DescriptionMetadata
from src.metadata.models_unit import UnitMetadata
from src.metadata.models_attribute import AttributeMetadata
from src.metadata.models_datatype import DatatypeMetadata


@dataclass
class MetadataResult:
    descriptions: list[DescriptionMetadata]
    units: list[UnitMetadata] = field(default_factory=list)
    attributes: list[AttributeMetadata] = field(default_factory=list)
    datatypes: list[DatatypeMetadata] = field(default_factory=list)