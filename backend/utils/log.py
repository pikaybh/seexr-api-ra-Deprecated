"""
Custom Logger Utility

Version: 2.2.1
Author: @pikaybh
License: MIT License

Usage:
This module provides a customizable logging system with support for different logging levels, file-based logging, and stream-based logging. 
It allows developers to configure logging settings through an abstract base class and extend them as needed.

Example:
    from logger_module import get_logger
    logger = get_logger("app")
    logger.info("Application started.")
"""

import os
import logging
from functools import wraps
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional



SELF_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SELF_DIR)
LOG_DIR = "logs"
EXT = ".log"


class LoggerConfig(ABC):
    """
    Abstract Base Class for logger configuration.
    Defines the required properties for configuring a logger.
    """

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Specifies a prefix (directory) for the log file path."""
        pass

    @property
    @abstractmethod
    def ext(self) -> str:
        """Specifies the extension for the log file (e.g., .log)."""
        pass

    @property
    @abstractmethod
    def file_format(self) -> str:
        """Specifies the format for log messages in the log file."""
        pass

    @property
    @abstractmethod
    def file_encoding(self) -> str:
        """Specifies the encoding to use for the log file."""
        pass

    @property
    @abstractmethod
    def file_handler_level(self) -> int:
        """Defines the logging level for the file handler."""
        pass

    @property
    @abstractmethod
    def stream_format(self) -> str:
        """Specifies the format for log messages in the stream handler."""
        pass

    @property
    @abstractmethod
    def stream_handler_level(self) -> int:
        """Defines the logging level for the stream handler."""
        pass


class DefaultLoggerConfig(LoggerConfig):
    """
    Default configuration for logger.
    Provides default values for file and stream handlers.
    """

    @property
    def prefix(self) -> str:
        return LOG_DIR

    @property
    def ext(self) -> str:
        return EXT

    @property
    def file_format(self) -> str:
        return r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname)s: %(message)s'

    @property
    def file_encoding(self) -> str:
        return 'utf-8-sig'

    @property
    def file_handler_level(self) -> int:
        return logging.DEBUG

    @property
    def stream_format(self) -> str:
        return r'%(message)s'

    @property
    def stream_handler_level(self) -> int:
        return logging.INFO


class CustomLogger(logging.Logger):
    """
    Custom Logger class to expose internal variables.
    Extends the logging.Logger class to include attributes for configuration details.
    """
    def __init__(self, name: str, config: LoggerConfig, file_path: str):
        super().__init__(name)
        self.prefix = config.prefix
        self.ext = config.ext
        self.file_path = file_path
        self.file_format = config.file_format
        self.file_encoding = config.file_encoding
        self.file_handler_level = config.file_handler_level
        self.stream_format = config.stream_format
        self.stream_handler_level = config.stream_handler_level

    def _create_log_decorator(self, log_func, level: str, message_format: Optional[str] = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)
                fmt = message_format or "{func_name}: {result}"
                log_func(fmt.format(
                    func_name=func.__name__,
                    result=result,
                    args=args,
                    kwargs=kwargs
                ))
                return result
            return wrapper
        return decorator if message_format else decorator

    def pinfo(self, message_format: Optional[str] = None) -> Callable:
        if isinstance(message_format, Callable):
            return self._create_log_decorator(self.info, "INFO")(message_format)
        return self._create_log_decorator(self.info, "INFO", message_format)

    def pdebug(self, message_format: Optional[str] = None) -> Callable:
        if isinstance(message_format, Callable):
            return self._create_log_decorator(self.debug, "DEBUG")(message_format)
        return self._create_log_decorator(self.debug, "DEBUG", message_format)

    def pwarn(self, message_format: Optional[str] = None) -> Callable:
        if isinstance(message_format, Callable):
            return self._create_log_decorator(self.warning, "WARNING")(message_format)
        return self._create_log_decorator(self.warning, "WARNING", message_format)

    def perror(self, message_format: Optional[str] = None) -> Callable:
        if isinstance(message_format, Callable):
            return self._create_log_decorator(self.error, "ERROR")(message_format)
        return self._create_log_decorator(self.error, "ERROR", message_format)


def get_logger(name: str, root: Optional[str] = ROOT_DIR, config: Optional[LoggerConfig] = DefaultLoggerConfig()) -> CustomLogger:
    """Creates and configures a logger with both file and stream handlers."""
    file_path = os.path.join(root, config.prefix, name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    logger = CustomLogger(name, config, file_path)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(logger.file_path, encoding=config.file_encoding)
    file_handler.setLevel(config.file_handler_level)
    file_handler.setFormatter(logging.Formatter(config.file_format))
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(config.stream_handler_level)
    stream_handler.setFormatter(logging.Formatter(config.stream_format))
    logger.addHandler(stream_handler)

    return logger


__all__ = ["get_logger", "LoggerConfig", "DefaultLoggerConfig", "CustomLogger"]