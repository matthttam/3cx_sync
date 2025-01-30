from enum import StrEnum
import logging


class LogLevel(StrEnum):
    CRITICAL = "critical"
    FATAL = "fatal"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class TextWindowHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

        # Configure tags for different log levels
        self.text_widget.tag_configure(LogLevel.CRITICAL, foreground="red")
        self.text_widget.tag_configure(LogLevel.FATAL, foreground="red")
        self.text_widget.tag_configure(LogLevel.ERROR, foreground="orange")
        self.text_widget.tag_configure(LogLevel.WARNING, foreground="darkorange")
        self.text_widget.tag_configure(LogLevel.INFO, foreground="green")
        self.text_widget.tag_configure(LogLevel.DEBUG, foreground="blue")

    def emit(self, record):
        try:
            msg = self.format(record)
            # tag = self.get_log_level_tag()
            self.text_widget.insert("end", msg + "\n", LogLevel[record.levelname])
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

    def remove_text_window_handler(self, text_widget):
        for handler in self.logger.handlers:
            if isinstance(handler, TextWindowHandler) and handler.text_widget == text_widget:
                self.logger.removeHandler(handler)

    def log(self, log_level, message, *args, **kwargs) -> None:
        """Logs a message using the specified method after checking if sync should pause.

        Args:
            method (str): The logging method to call (e.g., 'info', 'error').
            message (str): The message to log.
            *args: Positional arguments for the logger method.
            **kwargs: Keyword arguments for the logger method.
        """
        try:
            log_method = getattr(self.logger, log_level)
            log_method(message, *args, **kwargs)
        except AttributeError:
            raise ValueError(f"Invalid logging method: {log_level}")
