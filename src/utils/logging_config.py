import json
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def setup_logging():
    """Set up console and file logging."""
    config_path = PROJECT_ROOT / "config" / "config.json"

    with config_path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    log_file = PROJECT_ROOT / config.get("log_file", "logs/app.log")
    log_file.parent.mkdir(parents=True, exist_ok=True)

    level_name = config.get("log_level", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True
    )