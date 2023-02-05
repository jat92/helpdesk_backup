import logging
import logging.config
import logging.handlers
import yaml
import os

log_config_file = os.getenv("LOG_CONFIG_FILE", "logger.yaml")
log_config = yaml.safe_load(open(log_config_file, "r"))
logging.config.dictConfig(log_config)
logging.getLogger().handlers.clear()  # This stops duplicate logging
