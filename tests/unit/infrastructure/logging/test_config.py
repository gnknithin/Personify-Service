from personify.infrastructure.logging.config import (
    BRIEF_FORMATTER,
    CONSOLE_HANDLER,
    DETAILED_FORMATTER,
    DISABLE_EXISTING_LOGGER,
    ERROR_LOGGER_FILENAME,
    FILE_HANDLER,
    FORMATTERS,
    HANDLERS,
    LOGGERS,
    PERSONIFY_LOGGER,
    PERSONIFY_LOGGER_CONFIG,
    ROOT,
    VERSION,
)
from tests.unit.abstract_unit_test import AbstractUnitTest


class TestLoggingConfig(AbstractUnitTest):
    def test_personify_logger_config(self):
        # Arrange
        # Act
        _sut = PERSONIFY_LOGGER_CONFIG
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 6

        assert "version" in _sut
        assert _sut["version"] is not None
        assert isinstance(_sut["version"], int)
        assert _sut["version"] == 1

        assert "disable_existing_loggers" in _sut
        assert _sut["disable_existing_loggers"] is not None
        assert isinstance(_sut["disable_existing_loggers"], bool)
        assert _sut["disable_existing_loggers"] is False

        assert "formatters" in _sut
        assert _sut["formatters"] is not None
        assert isinstance(_sut["formatters"], dict)
        assert len(_sut["formatters"]) == 2

        assert "brief" in _sut["formatters"]
        assert _sut["formatters"]["brief"] is not None
        assert isinstance(_sut["formatters"]["brief"], dict)
        assert len(_sut["formatters"]["brief"]) == 2
        assert "format" in _sut["formatters"]["brief"]
        assert isinstance(_sut["formatters"]["brief"]["format"], str)
        assert (
            _sut["formatters"]["brief"]["format"]
            == "%(asctime)s %(name)s %(levelname)s : %(message)s"
        )
        assert "datefmt" in _sut["formatters"]["brief"]
        assert isinstance(_sut["formatters"]["brief"]["datefmt"], str)
        assert _sut["formatters"]["brief"]["datefmt"] == "%Y-%m-%d %H:%M:%S"

        assert "detailed" in _sut["formatters"]
        assert _sut["formatters"]["detailed"] is not None
        assert isinstance(_sut["formatters"]["detailed"], dict)
        assert len(_sut["formatters"]["detailed"]) == 2
        assert "format" in _sut["formatters"]["detailed"]
        assert isinstance(_sut["formatters"]["detailed"]["format"], str)
        assert (
            _sut["formatters"]["detailed"]["format"]
            == 'time="%(asctime)s" logger="%(name)s" level="%(levelname)s" file="%(filename)s" lineno=%(lineno)d function="%(funcName)s" %(message)s'
        )
        assert "datefmt" in _sut["formatters"]["detailed"]
        assert isinstance(_sut["formatters"]["detailed"]["datefmt"], str)
        assert _sut["formatters"]["detailed"]["datefmt"] == "%Y-%m-%d %H:%M:%S"

        assert "handlers" in _sut
        assert _sut["handlers"] is not None
        assert isinstance(_sut["handlers"], dict)
        assert len(_sut["handlers"]) == 2

        assert "console" in _sut["handlers"]
        assert _sut["handlers"]["console"] is not None
        assert isinstance(_sut["handlers"]["console"], dict)
        assert len(_sut["handlers"]["console"]) == 4
        assert "class" in _sut["handlers"]["console"]
        assert isinstance(_sut["handlers"]["console"]["class"], str)
        assert _sut["handlers"]["console"]["class"] == "logging.StreamHandler"
        assert "level" in _sut["handlers"]["console"]
        assert isinstance(_sut["handlers"]["console"]["level"], str)
        assert _sut["handlers"]["console"]["level"] == "INFO"
        assert "formatter" in _sut["handlers"]["console"]
        assert isinstance(_sut["handlers"]["console"]["formatter"], str)
        assert _sut["handlers"]["console"]["formatter"] == "brief"
        assert "stream" in _sut["handlers"]["console"]
        assert isinstance(_sut["handlers"]["console"]["stream"], str)
        assert _sut["handlers"]["console"]["stream"] == "ext://sys.stdout"

        assert "file" in _sut["handlers"]
        assert _sut["handlers"]["file"] is not None
        assert isinstance(_sut["handlers"]["file"], dict)
        assert len(_sut["handlers"]["file"]) == 5
        assert "class" in _sut["handlers"]["file"]
        assert isinstance(_sut["handlers"]["file"]["class"], str)
        assert (
            _sut["handlers"]["file"]["class"] == "logging.handlers.RotatingFileHandler"
        )
        assert "level" in _sut["handlers"]["file"]
        assert isinstance(_sut["handlers"]["file"]["level"], str)
        assert _sut["handlers"]["file"]["level"] == "DEBUG"
        assert "formatter" in _sut["handlers"]["file"]
        assert isinstance(_sut["handlers"]["file"]["formatter"], str)
        assert _sut["handlers"]["file"]["formatter"] == "detailed"
        assert "filename" in _sut["handlers"]["file"]
        assert isinstance(_sut["handlers"]["file"]["filename"], str)
        assert _sut["handlers"]["file"]["filename"] == "/tmp/personify.log"
        assert "backupCount" in _sut["handlers"]["file"]
        assert isinstance(_sut["handlers"]["file"]["backupCount"], int)
        assert _sut["handlers"]["file"]["backupCount"] == 3

        assert "loggers" in _sut
        assert _sut["loggers"] is not None
        assert isinstance(_sut["loggers"], dict)
        assert len(_sut["loggers"]) == 1
        assert "personify" in _sut["loggers"]
        assert _sut["loggers"]["personify"] is not None
        assert isinstance(_sut["loggers"]["personify"], dict)
        assert len(_sut["loggers"]["personify"]) == 3
        assert "level" in _sut["loggers"]["personify"]
        assert isinstance(_sut["loggers"]["personify"]["level"], str)
        assert _sut["loggers"]["personify"]["level"] == "DEBUG"
        assert "handlers" in _sut["loggers"]["personify"]
        assert isinstance(_sut["loggers"]["personify"]["handlers"], list)
        assert len(_sut["loggers"]["personify"]["handlers"]) == 2
        assert "console" in _sut["loggers"]["personify"]["handlers"]
        assert "file" in _sut["loggers"]["personify"]["handlers"]
        assert "propagate" in _sut["loggers"]["personify"]
        assert isinstance(_sut["loggers"]["personify"]["propagate"], bool)
        assert _sut["loggers"]["personify"]["propagate"] is False

        assert "root" in _sut
        assert _sut["root"] is not None
        assert isinstance(_sut["root"], dict)
        assert "level" in _sut["root"]
        assert _sut["root"]["level"] is not None
        assert isinstance(_sut["root"]["level"], str)
        assert _sut["root"]["level"] == "WARNING"
        assert "handlers" in _sut["root"]
        assert _sut["root"]["handlers"] is not None
        assert isinstance(_sut["root"]["handlers"], list)
        assert len(_sut["root"]["handlers"]) == 1
        assert "console" in _sut["root"]["handlers"]

    def test_root(self):
        # Arrange
        # Act
        _sut = ROOT
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert "level" in _sut
        assert _sut["level"] is not None
        assert isinstance(_sut["level"], str)
        assert _sut["level"] == "WARNING"
        assert "handlers" in _sut
        assert _sut["handlers"] is not None
        assert isinstance(_sut["handlers"], list)
        assert len(_sut["handlers"]) == 1
        assert "console" in _sut["handlers"]

    def test_loggers(self):
        # Arrange
        # Act
        _sut = LOGGERS
        # Assert
        assert _sut is not None
        assert len(_sut) == 1
        assert isinstance(_sut, dict)
        assert "personify" in _sut
        assert _sut["personify"] is not None
        assert isinstance(_sut["personify"], dict)
        assert len(_sut["personify"]) == 3
        assert "level" in _sut["personify"]
        assert isinstance(_sut["personify"]["level"], str)
        assert _sut["personify"]["level"] == "DEBUG"
        assert "handlers" in _sut["personify"]
        assert isinstance(_sut["personify"]["handlers"], list)
        assert len(_sut["personify"]["handlers"]) == 2
        assert "console" in _sut["personify"]["handlers"]
        assert "file" in _sut["personify"]["handlers"]
        assert "propagate" in _sut["personify"]
        assert isinstance(_sut["personify"]["propagate"], bool)
        assert _sut["personify"]["propagate"] is False

    def test_handlers(self):
        # Arrange
        # Act
        _sut = HANDLERS
        # Assert
        assert _sut is not None
        assert len(_sut) == 2
        assert "console" in _sut
        assert _sut["console"] is not None
        assert isinstance(_sut["console"], dict)
        assert len(_sut["console"]) == 4
        assert "class" in _sut["console"]
        assert isinstance(_sut["console"]["class"], str)
        assert _sut["console"]["class"] == "logging.StreamHandler"
        assert "level" in _sut["console"]
        assert isinstance(_sut["console"]["level"], str)
        assert _sut["console"]["level"] == "INFO"
        assert "formatter" in _sut["console"]
        assert isinstance(_sut["console"]["formatter"], str)
        assert _sut["console"]["formatter"] == "brief"
        assert "stream" in _sut["console"]
        assert isinstance(_sut["console"]["stream"], str)
        assert _sut["console"]["stream"] == "ext://sys.stdout"
        assert "file" in _sut
        assert _sut["file"] is not None
        assert isinstance(_sut["file"], dict)
        assert len(_sut["file"]) == 5
        assert "class" in _sut["file"]
        assert isinstance(_sut["file"]["class"], str)
        assert _sut["file"]["class"] == "logging.handlers.RotatingFileHandler"
        assert "level" in _sut["file"]
        assert isinstance(_sut["file"]["level"], str)
        assert _sut["file"]["level"] == "DEBUG"
        assert "formatter" in _sut["file"]
        assert isinstance(_sut["file"]["formatter"], str)
        assert _sut["file"]["formatter"] == "detailed"
        assert "filename" in _sut["file"]
        assert isinstance(_sut["file"]["filename"], str)
        assert _sut["file"]["filename"] == "/tmp/personify.log"
        assert "backupCount" in _sut["file"]
        assert isinstance(_sut["file"]["backupCount"], int)
        assert _sut["file"]["backupCount"] == 3

    def test_formatters(self):
        # Arrange
        # Act
        _sut = FORMATTERS
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 2

        assert "brief" in _sut
        assert _sut["brief"] is not None
        assert isinstance(_sut["brief"], dict)
        assert len(_sut["brief"]) == 2
        assert "format" in _sut["brief"]
        assert isinstance(_sut["brief"]["format"], str)
        assert (
            _sut["brief"]["format"]
            == "%(asctime)s %(name)s %(levelname)s : %(message)s"
        )
        assert "datefmt" in _sut["brief"]
        assert isinstance(_sut["brief"]["datefmt"], str)
        assert _sut["brief"]["datefmt"] == "%Y-%m-%d %H:%M:%S"

        assert "detailed" in _sut
        assert _sut["detailed"] is not None
        assert isinstance(_sut["detailed"], dict)
        assert len(_sut["detailed"]) == 2
        assert "format" in _sut["detailed"]
        assert isinstance(_sut["detailed"]["format"], str)
        assert (
            _sut["detailed"]["format"]
            == 'time="%(asctime)s" logger="%(name)s" level="%(levelname)s" file="%(filename)s" lineno=%(lineno)d function="%(funcName)s" %(message)s'
        )
        assert "datefmt" in _sut["detailed"]
        assert isinstance(_sut["detailed"]["datefmt"], str)
        assert _sut["detailed"]["datefmt"] == "%Y-%m-%d %H:%M:%S"

    def test_personify_logger(self):
        # Arrange
        # Act
        _sut = PERSONIFY_LOGGER
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 3
        assert "level" in _sut
        assert isinstance(_sut["level"], str)
        assert _sut["level"] == "DEBUG"
        assert "handlers" in _sut
        assert isinstance(_sut["handlers"], list)
        assert len(_sut["handlers"]) == 2
        assert "console" in _sut["handlers"]
        assert "file" in _sut["handlers"]
        assert "propagate" in _sut
        assert isinstance(_sut["propagate"], bool)
        assert _sut["propagate"] is False

    def test_file_handler(self):
        # Arrange
        # Act
        _sut = FILE_HANDLER
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 5
        assert "class" in _sut
        assert isinstance(_sut["class"], str)
        assert _sut["class"] == "logging.handlers.RotatingFileHandler"
        assert "level" in _sut
        assert isinstance(_sut["level"], str)
        assert _sut["level"] == "DEBUG"
        assert "formatter" in _sut
        assert isinstance(_sut["formatter"], str)
        assert _sut["formatter"] == "detailed"
        assert "filename" in _sut
        assert isinstance(_sut["filename"], str)
        assert _sut["filename"] == "/tmp/personify.log"
        assert "backupCount" in _sut
        assert isinstance(_sut["backupCount"], int)
        assert _sut["backupCount"] == 3

    def test_error_logger_filename(self):
        # Arrange
        # Act
        _sut = ERROR_LOGGER_FILENAME
        # Assert
        assert _sut is not None
        assert isinstance(_sut, str)
        assert _sut == "/tmp/personify.log"

    def test_console_handler(self):
        # Arrange
        # Act
        _sut = CONSOLE_HANDLER
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 4
        assert "class" in _sut
        assert isinstance(_sut["class"], str)
        assert _sut["class"] == "logging.StreamHandler"
        assert "level" in _sut
        assert isinstance(_sut["level"], str)
        assert _sut["level"] == "INFO"
        assert "formatter" in _sut
        assert isinstance(_sut["formatter"], str)
        assert _sut["formatter"] == "brief"
        assert "stream" in _sut
        assert isinstance(_sut["stream"], str)
        assert _sut["stream"] == "ext://sys.stdout"

    def test_detailed_formatters(self) -> None:
        # Arrange
        # Act
        _sut = DETAILED_FORMATTER
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 2
        assert "format" in _sut
        assert isinstance(_sut["format"], str)
        assert (
            _sut["format"]
            == 'time="%(asctime)s" logger="%(name)s" level="%(levelname)s" file="%(filename)s" lineno=%(lineno)d function="%(funcName)s" %(message)s'
        )
        assert "datefmt" in _sut
        assert isinstance(_sut["datefmt"], str)
        assert _sut["datefmt"] == "%Y-%m-%d %H:%M:%S"

    def test_brief_formatters(self) -> None:
        # Arrange
        # Act
        _sut = BRIEF_FORMATTER
        # Assert
        assert _sut is not None
        assert isinstance(_sut, dict)
        assert len(_sut) == 2
        assert "format" in _sut
        assert isinstance(_sut["format"], str)
        assert _sut["format"] == "%(asctime)s %(name)s %(levelname)s : %(message)s"
        assert "datefmt" in _sut
        assert isinstance(_sut["datefmt"], str)
        assert _sut["datefmt"] == "%Y-%m-%d %H:%M:%S"

    def test_disable_existing_logger(self) -> None:
        # Arrange
        # Act
        _sut = DISABLE_EXISTING_LOGGER
        # Assert
        assert _sut is not None
        assert isinstance(_sut, bool)
        assert _sut is False

    def test_version(self) -> None:
        # Arrange
        # Act
        _sut = VERSION
        # Assert
        assert _sut is not None
        assert isinstance(_sut, int)
        assert _sut == 1

    # def test_filters(self) -> None:
    #     # Arrange
    #     # Act
    #     _sut = FILTERS
    #     # Assert
    #     assert _sut is not None
    #     assert isinstance(_sut, dict)
    #     assert len(_sut) == 0
