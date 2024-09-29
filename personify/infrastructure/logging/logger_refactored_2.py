import logging
import re
import traceback
from threading import Lock
from typing import Any, Dict

import aiotask_context as context
import logfmt

LOG_CONTEXT_KEY = "log_context"


class SingletonMeta(type):
    """A metaclass for creating Singleton classes."""

    _instances: Dict[Any, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=SingletonMeta):
    """A logger class that manages logging context and messages."""

    def __init__(self):
        self.log_context: Dict[Any, Any] = {}

    def _get_log_context(self) -> Dict[Any, Any]:
        """Retrieve the current logging context, creating one if it doesn't exist."""
        if not self.log_context:
            self.log_context = context.get(LOG_CONTEXT_KEY) or {}
            context.set(LOG_CONTEXT_KEY, self.log_context)
        return self.log_context

    def set_log_context(self, **kwargs: Any) -> None:
        """Update the logging context with new key-value pairs."""
        self._get_log_context()
        self.log_context.update(kwargs)

    def clear_log_context(self) -> None:
        """Clear the current logging context."""
        self._get_log_context()
        self.log_context.clear()

    def log(
        self,
        logger: logging.Logger,
        level: int,
        include_context: bool = False,
        **kwargs: Any,
    ) -> None:
        """Log a message with optional context information."""
        context_info = self._get_log_context() if include_context else {}
        all_info = {**context_info, **kwargs}

        # Filter out unwanted keys
        filtered_info = {
            k: v
            for k, v in all_info.items()
            if k not in ["exc_info", "stack_info", "extra"]
        }

        # Handle exception info if present
        exc_info = all_info.get("exc_info")
        if exc_info:
            trace = "\t".join(traceback.format_exception(*exc_info))
            filtered_info["trace"] = re.sub(r"[\r\n]+", "\t", trace)

        # Format the log message
        msg = next(logfmt.format(filtered_info))
        logger.log(level, msg)
