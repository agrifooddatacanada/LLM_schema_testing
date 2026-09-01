from __future__ import annotations
from typing import List
from dataclasses import dataclass, field

@dataclass
class ColumnProfile:
    column_name: str
    source_position: int
    sample_values: List[str] = field(default_factory=list)
    missing_count: int = 0
    unique_count: int = 0
    inferred_datatypes: List[str] = field(default_factory=list)

@dataclass
class TabularProfile:
    source_file: str
    columns: List[ColumnProfile]
