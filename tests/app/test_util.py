from unittest.mock import patch, MagicMock
from app.util import initialize_or_get_user_config_path, handle_error
from sync.logging import LogLevel


class TestUtil:
    @patch("app.util.os")
    @patch("app.util.platformdirs")
    def test_initialize_or_get_user_config_path(self, mock_platformdirs, mock_os):
        # Prepare the mock return value for user_config_dir
        user_config_dir = "/user/config/dir"
        config_file_path = "/config/file/path"
        mock_platformdirs.user_config_dir.return_value = user_config_dir
        mock_os.path.join.return_value = "/config/file/path"

        initialize_or_get_user_config_path("test_name", "test_author", "test_folder")
        mock_platformdirs.user_config_dir.assert_called_once_with("test_name", "test_author")
        mock_os.makedirs.assert_called_once_with(config_file_path, exist_ok=True)
        mock_os.path.join.assert_called_once_with(user_config_dir, "test_folder")

    @patch("app.util.tk.messagebox.showerror")
    def test_handle_error_decorator(self, mock_showerror):
        mock_logger = MagicMock()
        mock_self = MagicMock()
        mock_self.logger = mock_logger

        @handle_error
        def error_prone_method(self):
            raise ValueError("Test error")

        error_prone_method(mock_self)

        mock_showerror.assert_called_once_with("Error", "An error occurred: Test error")
        mock_logger.log.assert_called_once_with(
            LogLevel.CRITICAL, "A critical error has occurred and the application must exit. Test error"
        )
