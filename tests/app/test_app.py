import os
import sys
import tkinter as tk
from unittest.mock import MagicMock, patch
from app.app import App
from app.windows import Window


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
        assert app.sync_running is False
        assert app.logger == mock_logger
        assert isinstance(app, tk.Tk)
        assert isinstance(app, Window)
        mock_load_theme.assert_called_once_with()
        mock_build_gui.assert_called_once_with()

    @patch("app.app.ttk.Style")
    @patch.object(App, "get_theme_path")
    def test_load_theme(self, mock_get_theme_pack, mock_style_class, app):
        mock_style = MagicMock()
        mock_style_class.return_value = mock_style
        mock_theme_pack = MagicMock()
        mock_get_theme_pack.return_value = mock_theme_pack
        app.tk = MagicMock()
        app.load_theme()
        app.tk.call.assert_any_call("source", mock_theme_pack)
        mock_style.theme_use.assert_called_once()
        mock_style.configure.assert_called_once()

    def test_get_theme_path_pyinstaller(self, app):
        """Test get_theme_path when running in a PyInstaller bundle."""
        # Add _MEIPASS attribute temporarily
        setattr(sys, "_MEIPASS", "/mock/pyinstaller/path")
        try:
            theme_path = app.get_theme_path()
            expected_path = os.path.join(
                "/mock/pyinstaller/path",
                "themes",
                "Forest-ttk-theme-1.0",
                "forest-light.tcl",
            )
            assert theme_path == expected_path
        finally:
            # Clean up the attribute to avoid side effects
            delattr(sys, "_MEIPASS")

    def test_get_theme_path_script(self, app):
        """Test get_theme_path when running as a script."""
        with patch("os.path.dirname", return_value="/mock/script/path"):
            theme_path = app.get_theme_path()
            expected_path = os.path.join(
                "/mock/script/path",
                "themes",
                "Forest-ttk-theme-1.0",
                "forest-light.tcl",
            )
            assert theme_path == expected_path

    @patch("app.app.WindowAppConfig")
    def test_show_window_app_config(self, window_app_config, app):
        app.show_WindowAppConfig()
        window_app_config.assert_called_once_with(app, app.app_config)

    @patch("app.app.WindowCSVMapping")
    def test_show_window_csv_mapping(self, window_csv_mapping, app):
        app.show_WindowCSVMapping()
        window_csv_mapping.assert_called_once_with(app)

    @patch.object(App, "destroy")
    def test_handle_exit_click(self, mock_destroy, app):
        app.handle_exit_click()
        mock_destroy.assert_called_once_with()

    @patch("app.app.WindowSync")
    def test_handle_csv_sync_click(self, mock_window_sync_class, app):
        mock_window_sync = MagicMock()
        mock_window_sync_class.return_value = mock_window_sync
        app.handle_csv_sync_click()
        mock_window_sync_class.assert_called_once_with(app)
        mock_window_sync.start_sync.assert_called_once_with()

    # @patch("app.app.App.CSVMapping")
    def test_export_app_config(self, app):
        app._export_app_config("fake_dir")
        app.app_config.save_to.assert_called_once_with("fake_dir")

    @patch("app.app.CSVMapping")
    def test_export_csv_mapping(self, mock_csv_mapping_class, app):
        mock_csv_mapping = MagicMock()
        mock_csv_mapping_class.return_value = mock_csv_mapping
        app._export_csv_mapping("fake_dir")
        mock_csv_mapping.load.assert_called_once_with()
        mock_csv_mapping.save_to.assert_called_once_with("fake_dir")
