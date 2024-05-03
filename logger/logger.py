import json
import logging
import logging.config
import os

__all__ = ["logger"]

from logger.formatter import ColoredFormatter


def setup_logging():
    log_config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(log_config_path, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
        print("Logging configuration loaded successfully!")
    except Exception as e:
        logging.basicConfig(level=logging.INFO)

    console_handler = logging.getLogger('MyAppLogger').handlers[0]  # assuming it's the second handler
    console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))


setup_logging()

logger = logging.getLogger("AdCraftAI")
