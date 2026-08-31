import json
from pathlib import Path

from evaluation.models_experiment_config import ExperimentConfig

def get_experiment_configs() -> list:

    config_dir = Path(
        "evaluation/experiment_configs"
    )

    configs = []

    for path in sorted(
        config_dir.glob("*.json")
    ):
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        configs.append(
            ExperimentConfig(**data)
        )

    return configs