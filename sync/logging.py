from enum import StrEnum
import logging


class LogLevel(StrEnum):
    CRITICAL = 'critical'
    FATAL = 'fatal'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'


class TextWindowHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        try:
            msg = self.format(record)
            self.text_widget.insert("end", msg + "\n")
            self.text_widget.yview("end")
        except Exception:
            self.handleError(record)


class SyncLogger:
    """Class to initialize and configure logging to a file and a Tkinter text widget."""

    logger_name = "3cxSync"

    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def add_file_handler(self, path="app.log"):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(self.default_format)
        file_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)

    def add_text_window_handler(self, text_widget):
        text_window_handler = TextWindowHandler(text_widget)
        text_window_handler.setLevel(logging.DEBUG)
        text_window_formatter = logging.Formatter(self.default_format)
        text_window_handler.setFormatter(text_window_formatter)
        self.logger.addHandler(text_window_handler)

    def log(self, log_level, message, *args, **kwargs) -> None:
        """Logs a message using the specified method after checking if sync should pause.

        Args:
            method (str): The logging method to call (e.g., 'info', 'error').
            message (str): The message to log.
            *args: Positional arguments for the logger method.
            **kwargs: Keyword arguments for the logger method.
        """
        log_method = getattr(self.logger, log_level, None)
        if callable(log_method):
            log_method(message, *args, **kwargs)
        else:
            raise ValueError(f"Invalid logging method: {log_level}")

    @staticmethod
    def get_logger() -> logging.Logger:
        """Returns the configured logger instance."""
        return logging.getLogger(SyncLogger.logger_name)
