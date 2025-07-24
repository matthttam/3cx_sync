import tkinter as tk
from unittest.mock import MagicMock, patch
from app.app import App
from app.windows import Window
from sync.strategy.csv.sync_csv import SyncCSV


class TestApp:

    @patch("app.app.WidgetList")
    @patch.object(App, "load_theme")
    @patch.object(App, "build_gui")
    def test_init(
        self,
        mock_build_gui,
        mock_load_theme,
        mock_widget_list_class,
        mock_logger,
        mock_app_config,
    ):
        mock_widget_list = MagicMock()
        mock_widget_list_class.return_value = mock_widget_list
        app = App(logger=mock_logger, app_config=mock_app_config)
        assert app.widgets == mock_widget_list
        assert app.is_paused is False
        assert app.logger == mock_logger
        assert app.sync == None
        assert app.sync_thread == None
        assert isinstance(app, tk.Tk)
        assert isinstance(app, Window)
        mock_load_theme.assert_called_once()
        mock_build_gui.assert_called_once()


    @patch("app.app.sv_ttk")
    @patch("app.app.darkdetect")
    @patch("app.app.platform")
    def test_load_theme_windows(self, mock_platform, mock_darkdetect, mock_sv_ttk, app):
        mock_platform.system = MagicMock(return_value="Windows")
        mock_darkdetect.theme = MagicMock(return_value="dark")
        
        app.load_theme()

        mock_sv_ttk.set_theme.assert_called_once_with("dark")


    @patch("app.app.platform")
    def test_load_theme_clam(self, mock_platform, app):
        mock_platform.system = MagicMock(side_effect="Linux")

        app.style = MagicMock()
        app.style.theme_names.return_value = ["clam", "alt"]
        app.load_theme()

        app.style.theme_use.assert_called_once_with("clam")


    @patch("app.app.platform")
    def test_load_theme_default(self, mock_platform, app):
        mock_platform.system = MagicMock(side_effect="Linux")
        app.style = MagicMock()
        app.style.theme_names.return_value = ["default"]

        app.load_theme()

        app.style.theme_use.assert_called_once_with("default")

    @patch("app.app.platform")
    def test_load_theme_none_available(self, mock_platform, app):
        mock_platform.system = MagicMock(side_effect="Linux")
        app.style = MagicMock()
        app.style.theme_names.return_value = ["alt", "classic"]
        
        app.load_theme()

        app.style.theme_use.assert_not_called()


    @patch("app.app.WindowAppConfig")
    def test_show_window_app_config(self, window_app_config, app):
        app.show_WindowAppConfig()
        window_app_config.assert_called_once_with(app, app.app_config)

    @patch("app.app.CSVMapping")
    @patch("app.app.WindowCSVMapping")
    def test_show_window_csv_mapping(self, window_csv_mapping, mock_csv_mapping_class, app):
        app.app_config.config_path = "/test/path"
        mock_csv_mapping = MagicMock()
        mock_csv_mapping_class.return_value = mock_csv_mapping

        app.show_WindowCSVMapping()
        mock_csv_mapping_class.assert_called_once_with(config_path="/test/path")
        window_csv_mapping.assert_called_once_with(app, csv_mapping=mock_csv_mapping)

    @patch.object(App, "destroy")
    def test_handle_exit_click(self, mock_destroy, app):
        app.handle_exit_click()
        mock_destroy.assert_called_once()

    @patch("app.app.run_sync")
    @patch("app.app.Thread")
    @patch("app.app.WindowSync")
    def test_handle_csv_sync_click(self, mock_window_sync_class, mock_thread, mock_run_sync, app):
        mock_sync_thread = MagicMock()
        mock_thread.return_value = mock_sync_thread

        mock_window_sync = MagicMock()
        mock_window_sync_class.return_value = mock_window_sync

        app.handle_csv_sync_click()

        assert app.sync_thread == mock_sync_thread
        kwargs = {
            "sync_source_class": SyncCSV,
            "logger": app.logger,
            "on_sync_initialized": app.on_sync_initialized,
            "config_path": app.app_config.config_path,
        }
        mock_thread.assert_called_once_with(target=mock_run_sync, kwargs=kwargs)

        mock_window_sync_class.assert_called_once_with(app)
        mock_window_sync.periodic_update.assert_called_once()
        app.sync_thread.start.assert_called_once()

    def test_export_app_config(self, app):
        app._export_app_config("fake_dir")
        app.app_config.save_to.assert_called_once_with("fake_dir")

    @patch("app.app.CSVMapping")
    def test_export_csv_mapping(self, mock_csv_mapping_class, app):
        app.app_config.config_path.return_value = None
        mock_csv_mapping = MagicMock()
        mock_csv_mapping_class.return_value = mock_csv_mapping
        app._export_csv_mapping("fake_dir")
        mock_csv_mapping.load.assert_called_once()
        mock_csv_mapping.save_to.assert_called_once_with("fake_dir")

    def test_toggle_sync_state_is_paused(self, app):
        mock_sync = MagicMock()
        app.sync = mock_sync
        app.sync.is_paused = True
        app.toggle_sync_state()
        mock_sync.resume.assert_called_once()
        mock_sync.pause.assert_not_called()

    def test_toggle_sync_state_is_not_paused(self, app):
        mock_sync = MagicMock()
        app.sync = mock_sync
        app.sync.is_paused = False
        app.toggle_sync_state()
        mock_sync.resume.assert_not_called()
        mock_sync.pause.assert_called_once()

    def test_toggle_sync_state_sync_is_none(self, app):
        # Basically just make sure no errors are raised and nothing is returned.
        app.sync = None
        assert app.toggle_sync_state() is None

    def test_terminate_sync_sync_is_none(self, app):
        # Basically just make sure no errors are raised and nothing is returned.
        app.sync = None
        assert app.terminate_sync() is None

    def test_terminate_sync(self, app):
        mock_sync = MagicMock()
        app.sync = mock_sync

        app.terminate_sync()

        mock_sync.terminate.assert_called_once()
        mock_sync.running_event.set.assert_called_once()

    @patch("app.app.askdirectory")
    @patch.object(App, "_export_app_config")
    @patch.object(App, "_export_csv_mapping")
    def test_handle_csv_export_configs_click(
        self, mock_export_csv_mapping, mock_export_app_config, mock_askdirectory, app
    ):
        mock_askdirectory.return_value = "fake_dir"
        app.handle_csv_export_configs_click()
        mock_askdirectory.assert_called_once()
        mock_export_app_config.assert_called_once_with("fake_dir")
        mock_export_csv_mapping.assert_called_once_with("fake_dir")

    @patch("app.app.askdirectory")
    @patch.object(App, "_export_app_config")
    @patch.object(App, "_export_csv_mapping")
    def test_handle_csv_export_configs_click_no_directory(
        self, mock_export_csv_mapping, mock_export_app_config, mock_askdirectory, app
    ):
        mock_askdirectory.return_value = ""
        app.handle_csv_export_configs_click()
        mock_askdirectory.assert_called_once()
        mock_export_app_config.assert_not_called()
        mock_export_csv_mapping.assert_not_called()

    def test_on_sync_initialized(self, app):
        mock_sync = MagicMock()
        app.on_sync_initialized(mock_sync)
        assert app.sync == mock_sync
