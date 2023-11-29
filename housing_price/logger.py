from datetime import datetime
import logging.config
import os
import sys


DEFAULT_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s " \
                 "%(filename)s %(lineno)s- %(message)s"
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
default_stream_handler = logging.StreamHandler(sys.stdout)
default_stream_handler.setFormatter(logging.Formatter(
    fmt=DEFAULT_FORMAT, datefmt=DEFAULT_TIME_FORMAT))


file_name = "LOG_" + str(datetime.now())
file_name = file_name.replace(" ", "_").replace(":", "_").replace(".", "_") + ".log"
FILE_NAME = r"logs\\" + file_name

# fmt: off
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": DEFAULT_FORMAT,
            "datefmt": DEFAULT_TIME_FORMAT,
        },
    },
    "handlers": {
        "file_handler": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": FILE_NAME,
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
        "urllib3": {
            "handlers": ["null"],
            "level": "DEBUG",
            "propagate": False,
        },
        "requests_kerberos.kerberos_": {
            "handlers": ["null"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
# fmt: on
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("housing_price")

