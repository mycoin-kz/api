"""Logging configuration for data processing module."""

import logging.config
import os
from typing import Optional


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure logging for the data processing module.

    Args:
        log_level: Optional override for the log level
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "simple": {"format": "%(levelname)s - %(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "data_processing.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "data_processing_errors.log"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "main_module.data_processing": {
                "handlers": ["console", "file", "error_file"],
                "level": log_level or "INFO",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)
