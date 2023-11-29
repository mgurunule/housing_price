import logging.config
import sys


DEFAULT_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s " \
                 "%(filename)s %(lineno)s- %(message)s"
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
default_stream_handler = logging.StreamHandler(sys.stdout)
default_stream_handler.setFormatter(logging.Formatter(
    fmt=DEFAULT_FORMAT, datefmt=DEFAULT_TIME_FORMAT))


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
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "null": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.NullHandler",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
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
