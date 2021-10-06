import logging
import sys
from logging import Filter
from logging.config import dictConfig

log = logging.getLogger(__name__)
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(message)s",
        },
        "verbose": {
            "format": "[%(asctime)s.%(msecs)03d] [%(levelname)-.3s]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "debug": {
            "format": "[%(asctime)s.%(msecs)03d] [%(levelname)-.4s]: %(message)s @@@ "
            "[%(threadName)s] [%(name)s:%(lineno)s]",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "std_filter": {"()": "git_syncer.utils.logger.LevelRangeFilter", "high": logging.WARNING},
        "err_filter": {"()": "git_syncer.utils.logger.LevelRangeFilter", "low": logging.WARNING},
    },
    "handlers": {
        "simple": {
            "class": "git_syncer.utils.logging.StreamHandler",
            "formatter": "simple",
            "stream": sys.stdout,
        },
        "console_out": {
            "class": "git_syncer.utils.logging.StreamHandler",
            "filters": ["std_filter"],
            "formatter": "verbose",
            "stream": sys.stdout,
        },
        "console_err": {
            "class": "git_syncer.utils.logging.StreamHandler",
            "filters": ["err_filter"],
            "formatter": "verbose",
            "stream": sys.stderr,
        },
    },
    "root": {"handlers": ["console_out", "console_err"], "level": "DEBUG"},
    "loggers": {
        "git_syncer.utils.shell.execution": {
            "level": "DEBUG",
            "handlers": ["simple"],
            "propagate": False,
        },
    },
}


class LevelRangeFilter(Filter):
    def __init__(self, low=0, high=100):
        Filter.__init__(self)
        self.low = low
        self.high = high

    def filter(self, record):
        if self.low <= record.levelno < self.high:
            return True
        return False


def configure_logging():
    dictConfig(LOGGING_CONFIG)
    log.debug("Logging configured")


def wrap(o: object) -> str:
    return f"[{o}]"
