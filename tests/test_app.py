from unittest.mock import Mock, patch
from app.app import App


class TestApp:

    def test_init_creates_window(self):
        # Mock tk.Tk to avoid creating an actual window
        patch('tkinter.Tk', Mock())

        app = App()

        assert isinstance(app, App)
        assert app.app_config is not None

    @patch('app.app.Window3cxConfig')
    def test_show_window_3cx_config(self, window_3cx_config):
        app = App()
        app.show_Window3cxConfig()
        window_3cx_config.assert_called_once_with(master=app)

    @patch('app.app.WindowCSVMapping')
    def test_show_window_csv_mapping(self, window_csv_mapping):
        app = App()
        app.show_WindowCSVMapping()
        window_csv_mapping.assert_called_once_with(master=app)

    def test_handle_exit_click_destroys_window(self):
        # Mock destroy method
        destroy_mock = Mock()
        app = App()
        app.destroy = destroy_mock

        app.handle_exit_click()

        destroy_mock.assert_called_once_with()

    @patch('app.app.SyncCSV')
    def test_handle_csv_sync_click_creates_sync_object_and_calls_sync(self, sync_csv):
        app = App()
        text_output_mock = Mock()
        app.txt_output = text_output_mock

        app.handle_csv_sync_click()

        sync_csv.assert_called_once_with(text=text_output_mock)
        sync_csv.return_value.sync.assert_called_once_with()
