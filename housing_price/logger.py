from datetime import datetime
import logging.config
import os
import sys


default_format = "%(asctime)s.%(msecs)03d %(levelname)s " \
                "%(filename)s %(lineno)s- %(message)s"
default_time_format = "%Y-%m-%dT%H:%M:%S"
default_stream_handler = logging.StreamHandler(sys.stdout)
default_stream_handler.setFormatter(logging.Formatter(
    fmt=default_format, datefmt=default_time_format))

file_name = "LOG_" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": file_name,
            'when': 'D',
            'interval': 1,
            'backupCount': 7,
        }
    },
    "loggers": {
        "": {
            "handlers": ["file_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
        'werkzeug': {
            'level': 'ERROR',
        },
    },
}
# fmt: on
logging.config.dictConfig(logging_config)
logger = logging.getLogger("housing_price")

