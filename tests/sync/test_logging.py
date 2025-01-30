import pytest
import logging
from sync.logging import LogLevel, TextWindowHandler, SyncLogger
from unittest.mock import MagicMock, patch


class TestLogLevel:
    def test_invalid_value(self):
        with pytest.raises(ValueError):
            LogLevel("invalid_value")

    def test_enum_values(self):
        # Verify that the enum values are correct
        assert LogLevel.CRITICAL == "critical"
        assert LogLevel.FATAL == "fatal"
        assert LogLevel.ERROR == "error"
        assert LogLevel.WARNING == "warning"
        assert LogLevel.INFO == "info"
        assert LogLevel.DEBUG == "debug"

    def test_enum_name(self):
        # Verify that the enum names are correct
        assert LogLevel.CRITICAL.name == "CRITICAL"
        assert LogLevel.FATAL.name == "FATAL"
        assert LogLevel.ERROR.name == "ERROR"
        assert LogLevel.WARNING.name == "WARNING"
        assert LogLevel.INFO.name == "INFO"
        assert LogLevel.DEBUG.name == "DEBUG"


class TestTextWindowHandler:
    @pytest.fixture
    def mock_text_widget(self):
        # Mock the text widget
        return MagicMock()

    @pytest.fixture
    def text_window_handler(self, mock_text_widget):
        # Create an instance of the handler with the mocked text widget
        return TextWindowHandler(mock_text_widget)

    def test_init(self, mock_text_widget):
        text_window_handler = TextWindowHandler(mock_text_widget)
        assert text_window_handler.text_widget == mock_text_widget

    def test_emit_success(self, text_window_handler, mock_text_widget):
        test_message = "Test message"
        log_record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=test_message,
            args=None,
            exc_info=None,
        )
        text_window_handler.emit(log_record)

        # Check that the insert method was called with the formatted message
        mock_text_widget.insert.assert_called_once_with("end", f"{test_message}\n", LogLevel.INFO)
        mock_text_widget.yview.assert_called_once_with("end")

    @patch.object(TextWindowHandler, "handleError")
    def test_emit_with_exception_handling(self, mock_handle_error, text_window_handler):
        text_window_handler.text_widget.insert.side_effect = Exception("Insert failed")
        log_record = logging.LogRecord(
            name="test_logger",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Error message",
            args=None,
            exc_info=None,
        )

        try:
            text_window_handler.emit(log_record)
        except Exception as e:
            pytest.fail(f"emit raised an exception: {e}")
        mock_handle_error.assert_called_once_with(log_record)


class TestSyncLogger:

    @pytest.fixture
    def sync_logger(self):
        sync_logger = SyncLogger()
        sync_logger.logger = MagicMock()
        yield sync_logger

    @patch("sync.logging.logging")
    def test_init(self, mock_logging):
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        sync_logger = SyncLogger()

        mock_logging.getLogger.assert_called_once_with(SyncLogger.logger_name)
        mock_logger.setLevel.assert_called_once_with(mock_logging.DEBUG)
        sync_logger.default_format == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @patch("sync.logging.logging")
    def test_add_file_handler(self, mock_logging, sync_logger):
        test_path = "test_path"
        mock_file_handler = MagicMock()
        mock_file_formatter = MagicMock()
        mock_logging.FileHandler.return_value = mock_file_handler
        mock_logging.Formatter.return_value = mock_file_formatter

        sync_logger.add_file_handler(path=test_path)

        mock_logging.FileHandler.assert_called_once_with(test_path)
        mock_file_handler.setLevel.assert_called_once_with(mock_logging.DEBUG)
        mock_logging.Formatter.assert_called_once_with(sync_logger.default_format)
        mock_file_handler.setFormatter.assert_called_once_with(mock_file_formatter)
        sync_logger.logger.addHandler.assert_called_once_with(mock_file_handler)

    @patch("sync.logging.logging")
    @patch("sync.logging.TextWindowHandler")
    def test_add_text_window_handler(self, mock_text_window_handler_class, mock_logging, sync_logger):
        mock_text_widget = MagicMock()

        mock_text_window_handler = MagicMock()
        mock_file_formatter = MagicMock()
        mock_text_window_handler_class.return_value = mock_text_window_handler
        mock_logging.Formatter.return_value = mock_file_formatter

        sync_logger.add_text_window_handler(mock_text_widget)

        mock_text_window_handler_class.assert_called_once_with(mock_text_widget)
        mock_text_window_handler.setLevel.assert_called_once_with(mock_logging.DEBUG)
        mock_logging.Formatter.assert_called_once_with(sync_logger.default_format)
        mock_text_window_handler.setFormatter.assert_called_once_with(mock_file_formatter)
        sync_logger.logger.addHandler.assert_called_once_with(mock_text_window_handler)

    @patch("sync.logging.logging")
    def test_log_valid_level(self, mock_logging):
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        sync_logger = SyncLogger()

        # Test logging at the 'info' level
        sync_logger.log("info", "Test message")
        mock_logger.info.assert_called_once_with("Test message")

        # Test logging at the 'error' level with arguments
        sync_logger.log("error", "Test error", "arg1", key="value")
        mock_logger.error.assert_called_once_with("Test error", "arg1", key="value")

    def test_log_invalid_level_blank(self):
        sync_logger = SyncLogger()

        # Test invalid log level should raise ValueError
        with pytest.raises(ValueError, match="Invalid logging method: invalid_level"):
            sync_logger.log("invalid_level", "Test message")

    @patch("sync.logging.logging")
    def test_log_arguments_forwarding(self, mock_logging):
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        sync_logger = SyncLogger()

        # Test logging with additional arguments and keyword arguments
        sync_logger.log("info", "Test message", "arg1", key="value")
        mock_logger.info.assert_called_once_with("Test message", "arg1", key="value")
