from datetime import datetime
import logging.config
import os
import sys


def load_logger_config():
    default_format = "%(asctime)s.%(msecs)03d %(levelname)s " \
                    "%(filename)s %(lineno)s- %(message)s"
    default_time_format = "%Y-%m-%dT%H:%M:%S"
    default_stream_handler = logging.StreamHandler(sys.stdout)
    default_stream_handler.setFormatter(logging.Formatter(
        fmt=default_format, datefmt=default_time_format))

    file_name = "LOG_" + str(datetime.now())
    file_name = file_name.replace(" ", "_").replace(":", "_").replace(".", "_") + ".log"
    file_name = r"logs\\" + file_name

    # fmt: off
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": default_format,
                "datefmt": default_time_format,
            },
        },
        "handlers": {
            "file_handler": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.FileHandler",
                "filename": file_name,
            },
            "null": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.NullHandler",
            }
        },
        "loggers": {
            "": {
                "handlers": ["file_handler"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
    # fmt: on
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger("housing_price")

    return logger

