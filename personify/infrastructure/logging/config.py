VERSION = 1
DISABLE_EXISTING_LOGGER = False

BRIEF_FORMATTER = {
    "format": "%(asctime)s %(name)s %(levelname)s : %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}
DETAILED_FORMATTER = {
    "format": 'time="%(asctime)s" logger="%(name)s" level="%(levelname)s" file="%(filename)s" lineno=%(lineno)d function="%(funcName)s" %(message)s',
    "datefmt": "%Y-%m-%d %H:%M:%S",
}

CONSOLE_HANDLER = {
    "class": "logging.StreamHandler",
    "level": "INFO",
    "formatter": "brief",
    "stream": "ext://sys.stdout",
}

ERROR_LOGGER_FILENAME = "/tmp/personify.log"

FILE_HANDLER = {
    "class": "logging.handlers.RotatingFileHandler",
    "level": "DEBUG",
    "formatter": "detailed",
    "filename": ERROR_LOGGER_FILENAME,
    "backupCount": 3,
}

PERSONIFY_LOGGER = {
    "level": "DEBUG",
    "handlers": ["console", "file"],
    "propagate": False,
}

FORMATTERS = {"brief": BRIEF_FORMATTER, "detailed": DETAILED_FORMATTER}

HANDLERS = {
    "console": CONSOLE_HANDLER,
    "file": FILE_HANDLER,
}

LOGGERS = {"personify": PERSONIFY_LOGGER}

ROOT = {"level": "WARNING", "handlers": ["console"]}

PERSONIFY_LOGGER_CONFIG = {
    "version": VERSION,
    "disable_existing_loggers": DISABLE_EXISTING_LOGGER,
    "formatters": FORMATTERS,
    "handlers": HANDLERS,
    "loggers": LOGGERS,
    "root": ROOT,
}
