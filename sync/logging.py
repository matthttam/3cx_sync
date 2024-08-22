import logging


class TextWindowHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        try:
            msg = self.format(record)
            self.text_widget.insert('end', msg + '\n')
            self.text_widget.yview('end')
        except Exception:
            self.handleError(record)


class SyncLogger:
    """Class to initialize and configure logging to a file and a Tkinter text widget."""

    logger_name = '3cxSync'

    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def addFileHandler(self, path='app.log'):
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(self.default_format)
        file_handler.setFormatter(file_formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)

    def addTextWindowHandler(self, text_widget):
        text_window_handler = TextWindowHandler(text_widget)
        text_window_handler.setLevel(logging.DEBUG)
        text_window_formatter = logging.Formatter(self.default_format)
        text_window_handler.setFormatter(text_window_formatter)
        self.logger.addHandler(text_window_handler)

    @staticmethod
    def get_logger():
        """Returns the configured logger instance."""
        # return self.logger
        return logging.getLogger(SyncLogger.logger_name)
