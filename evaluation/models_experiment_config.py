from dataclasses import dataclass


@dataclass
class ExperimentConfig:
    name: str
    model: str
    temperature: float = 0.0