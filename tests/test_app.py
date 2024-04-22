import pytest
from unittest.mock import Mock, patch
from app.app import App


class TestApp:

    @pytest.fixture
    def app(self):
        with patch("app.app.AppConfig", Mock()):
            return App()

    def test_init_creates_window(self):
        # Mock tk.Tk to avoid creating an actual window
        patch('tkinter.Tk', Mock())

        app = App()

        assert isinstance(app, App)
        assert app.app_config is not None

    @patch('app.app.Window3cxConfig')
    def test_show_window_3cx_config(self, window_3cx_config, app):
        app.show_Window3cxConfig()
        window_3cx_config.assert_called_once_with(master=app)

    @patch('app.app.WindowCSVMapping')
    def test_show_window_csv_mapping(self, window_csv_mapping, app):
        app.show_WindowCSVMapping()
        window_csv_mapping.assert_called_once_with(master=app)

    def test_handle_exit_click_destroys_window(self, app):
        destroy_mock = Mock()
        app.destroy = destroy_mock
        app.handle_exit_click()
        destroy_mock.assert_called_once_with()

    @patch('app.app.SyncCSV')
    @patch('app.app.Sync')
    def test_handle_csv_sync_click_creates_sync_object_and_calls_sync(self, sync, sync_csv, app):
        with patch.object(app, 'txt_output', Mock()) as mock_txt_output:
            app.handle_csv_sync_click()
            sync.assert_called_once_with(
                sync_source=sync_csv, text=mock_txt_output)
