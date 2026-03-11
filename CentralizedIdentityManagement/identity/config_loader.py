
import yaml
from pathlib import Path


def load_initial_config():
    config_path = Path("config/initial_config.yaml")

    if not config_path.exists():
        raise RuntimeError("initial_config.yaml not found")

    with open(config_path, "r") as file:
        return yaml.safe_load(file)
