import logging
import re
import traceback
from threading import Lock
from typing import Any, Dict

import aiotask_context as context
import logfmt

LOG_CONTEXT = 'log_context'


class LoggerMeta(type):
    _instances:Dict[Any,Any] = dict()

    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Logger(metaclass=LoggerMeta):

    @staticmethod
    def __get_log_context() -> Dict[Any,Any]:
        log_context: Any = context.get(LOG_CONTEXT)
        if log_context is None:
            log_context = dict()
            context.set(LOG_CONTEXT, log_context)

        return log_context

    @staticmethod
    def set_log_context(**kwargs: Any) -> None:
        log_context = Logger.__get_log_context()
        log_context.update(kwargs)

    @staticmethod
    def clean_log_context() -> None:
        log_context = Logger.__get_log_context()
        log_context.clear()

    @staticmethod
    def log(
        logger: logging.Logger,
        lvl: int,
        include_context: bool = False,
        **kwargs: Any
    ) -> None:
        all_info = {
            **Logger.__get_log_context(), **kwargs} if include_context else kwargs
        info = {
            k: v for k, v in all_info.items()
            if k not in ['exc_info', 'stack_info', 'extra']
        }

        exc_info = all_info.get('exc_info')
        # stack_info = all_info.get('stack_info', False)
        # extra = all_info.get('extra', {})

        if exc_info:
            trace: Any = '\t'.join(traceback.format_exception(*exc_info))
            info['trace'] = re.sub(r'[\r\n]+', '\t', trace)

        msg = next(logfmt.format(info))
        logger.log(
            lvl,
            msg,
            # exc_info=exc_info,
            # stack_info=stack_info,
            # extra=extra
        )
