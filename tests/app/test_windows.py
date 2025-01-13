import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.windows import WindowAppConfig, WidgetList, PopupWindow, WindowSync, Window, WindowCSVMapping
from sync.logging import LogLevel
from tkinter.scrolledtext import ScrolledText


class TestWindow:

    def test_window_default_row_and_column_are_zero(self, window):
        assert window._current_row == 0
        assert window._current_column == 0

    @patch.object(Window, "reset_row")
    @patch.object(Window, "reset_column")
    def test_reset_row_and_column(self, mock_reset_column, mock_reset_row, window):
        window.reset_row_and_column()
        mock_reset_column.assert_called_once_with()
        mock_reset_row.assert_called_once_with()

    @patch.object(Window, "reset_column")
    def test_increment_row_dont_reset_column(self, mock_reset_column, window):
        window._current_row = 4
        window.increment_row(reset_column=False)
        assert window._current_row == 5
        mock_reset_column.assert_not_called()

    @patch.object(Window, "reset_column")
    def test_increment_row_reset_column(self, mock_reset_column, window):
        window._current_row = 4
        window.increment_row(reset_column=True)
        assert window._current_row == 5
        mock_reset_column.assert_called_once_with()

    def test_get_current_row(self, window):
        window._current_row = 1000
        assert window.get_current_row() == 1000

    @patch.object(Window, "increment_row")
    def test_get_next_row_no_increment(self, mock_increment_row, window):
        # Get Current Row actually returns the pointer row and then increments
        window._current_row = 1000
        assert window.get_next_row(increment=False) == 1000
        mock_increment_row.assert_not_called()

    @patch.object(Window, "increment_row")
    def test_get_next_row_increment(self, mock_increment_row, window):
        # Get Current Row actually returns the pointer row and then increments
        window._current_row = 1000
        assert window.get_next_row(increment=True) == 1000
        mock_increment_row.assert_called_once_with()

    def test_increment_column(self, window):
        window._current_column = 1000
        window.increment_column()
        window.get_current_column() == 1001

    def test_reset_column(self, window):
        window._current_column = 1000
        window.reset_column()
        window.get_current_column() == 0

    def test_get_current_column(self, window):
        window._current_column = 1000
        assert window.get_current_column() == 1000

    @patch.object(Window, "increment_column")
    def test_get_next_column_no_increment(self, mock_increment_column, window):
        window._current_column = 1000
        assert window.get_next_column(increment=False) == 1000
        mock_increment_column.assert_not_called()

    @patch.object(Window, "increment_column")
    def test_get_next_column_increment(self, mock_increment_column, window):
        window._current_column = 1000
        assert window.get_next_column(increment=True) == 1000
        mock_increment_column.assert_called_once_with()


class TestPopupWindow:
    @patch.object(PopupWindow, "grab_set")
    @patch.object(PopupWindow, "focus_force")
    def test_popup_window(self, mock_focus_force, mock_grab_set, root):
        window = PopupWindow(master=root)
        mock_focus_force.assert_called_once_with()
        mock_grab_set.assert_called_once_with()
        window.destroy()


class TestWindowAppConfig:
    @patch.object(WindowAppConfig, "build_gui")
    @patch.object(WindowAppConfig, "initialize_variables")
    def test_init(self, mock_initialize_variables, mock_build_gui, mock_app_config, root):
        window = WindowAppConfig(master=root, app_config=mock_app_config)
        assert isinstance(window, PopupWindow)
        assert isinstance(window.widgets, WidgetList)
        assert window.app_config == mock_app_config
        mock_initialize_variables.assert_called_once_with()
        mock_build_gui.assert_called_once_with()

    @pytest.mark.parametrize(
            'mock_app_config',
            [{
                "3cx": {
                    "scheme": None,
                    "domain": None,
                    "port": None,
                    "username": None,
                    "password": None,
                    "store_credential_securely": None,
                },
                "app": {
                    "logout_hotdesk_on_disable": None,
                }
            }],
            indirect=True
    )
    def test_initialize_variables_blank(self, mock_app_config, root):
        window = WindowAppConfig(master=root, app_config=mock_app_config)
        assert isinstance(window.vars, dict)
        assert isinstance(window.vars['3cx']['scheme'], tk.StringVar)
        assert window.vars['3cx']['scheme'].get() == ""
        assert isinstance(window.vars['3cx']['domain'], tk.StringVar)
        assert window.vars['3cx']['domain'].get() == ""
        assert isinstance(window.vars['3cx']['port'], tk.StringVar)
        assert window.vars['3cx']['port'].get() == ""
        assert isinstance(window.vars['3cx']['username'], tk.StringVar)
        assert window.vars['3cx']['username'].get() == ""
        assert isinstance(window.vars['3cx']['password'], tk.StringVar)
        assert window.vars['3cx']['password'].get() == ""
        assert isinstance(window.vars['3cx']['store_credential_securely'], tk.BooleanVar)
        assert window.vars['3cx']['store_credential_securely'].get() is False
        assert isinstance(window.vars['app']['logout_hotdesk_on_disable'], tk.BooleanVar)
        assert window.vars['app']['logout_hotdesk_on_disable'].get() is False

    @pytest.mark.parametrize(
            'mock_app_config',
            [{
                "3cx": {
                    "scheme": "test_scheme",
                    "domain": "test_domain",
                    "port": "test_port",
                    "username": "username",
                    "password": "password",
                    "store_credential_securely": True,
                },
                "app": {
                    "logout_hotdesk_on_disable": True,
                }
            }],
            indirect=True
    )
    def test_initialize_variables_with_values(self, mock_app_config, root):
        window = WindowAppConfig(master=root, app_config=mock_app_config)
        assert isinstance(window.vars, dict)
        assert isinstance(window.vars['3cx']['scheme'], tk.StringVar)
        assert window.vars['3cx']['scheme'].get() == "test_scheme"
        assert isinstance(window.vars['3cx']['domain'], tk.StringVar)
        assert window.vars['3cx']['domain'].get() == "test_domain"
        assert isinstance(window.vars['3cx']['port'], tk.StringVar)
        assert window.vars['3cx']['port'].get() == "test_port"
        assert isinstance(window.vars['3cx']['username'], tk.StringVar)
        assert window.vars['3cx']['username'].get() == "username"
        assert isinstance(window.vars['3cx']['password'], tk.StringVar)
        assert window.vars['3cx']['password'].get() == "password"
        assert isinstance(window.vars['3cx']['store_credential_securely'], tk.BooleanVar)
        assert window.vars['3cx']['store_credential_securely'].get() is True
        assert isinstance(window.vars['app']['logout_hotdesk_on_disable'], tk.BooleanVar)
        assert window.vars['app']['logout_hotdesk_on_disable'].get() is True

    @patch("app.windows.messagebox.showinfo")
    @patch("app.windows.TCX_API_Connection")
    def test_handle_test_connection_success(self, mock_api, mock_messagebox_showinfo, window_app_config):
        mock_api.return_value = mock_api
        window_app_config.widgets.btn_test.invoke()
        mock_api.authenticate.assert_called_once_with(
            username=window_app_config.app_config["3cx"]["username"],
            password=window_app_config.app_config["3cx"]["password"]
        )
        mock_messagebox_showinfo.assert_called_once_with(title="Success", message="Test Successful")

    @patch("app.windows.messagebox.showinfo")
    @patch("app.windows.TCX_API_Connection")
    def test_handle_test_connection_failure(self, mock_api, mock_messagebox_showinfo, window_app_config):
        mock_api.return_value = mock_api
        e = Exception("Authentication Failed")
        mock_api.authenticate.side_effect = e
        window_app_config.widgets.btn_test.invoke()
        mock_api.authenticate.assert_called_once_with(
            username=window_app_config.app_config["3cx"]["username"],
            password=window_app_config.app_config["3cx"]["password"]
        )
        mock_messagebox_showinfo.assert_called_once_with(title="Failure", message=f"Test Failed. {e}")

    def test_btn_cancel_click_is_dirty_confirm_discard(self, window_app_config):
        with patch.object(window_app_config, "destroy") as mock_destroy:
            window_app_config.app_config.is_dirty = True
            window_app_config.confirm_discard_changes = MagicMock()
            window_app_config.confirm_discard_changes.return_value = True
            window_app_config.widgets.btn_cancel.invoke()
            window_app_config.confirm_discard_changes.assert_called_once_with()
            window_app_config.app_config.load.assert_called_once_with()
            mock_destroy.assert_called_once_with()

    def test_btn_cancel_click_is_dirty_dont_discard(self, window_app_config):
        with patch.object(window_app_config, "destroy") as mock_destroy:
            window_app_config.app_config.is_dirty = True
            window_app_config.confirm_discard_changes = MagicMock()
            window_app_config.confirm_discard_changes.return_value = False
            window_app_config.widgets.btn_cancel.invoke()
            window_app_config.app_config.load.assert_not_called()
            mock_destroy.assert_not_called()

    def test_btn_cancel_click_clean(self, window_app_config):
        with patch.object(window_app_config, "destroy") as mock_destroy:
            window_app_config.app_config.is_dirty = False
            window_app_config.confirm_discard_changes = MagicMock()
            window_app_config.widgets.btn_cancel.invoke()
            window_app_config.confirm_discard_changes.assert_not_called()
            window_app_config.app_config.load.assert_called_once_with()
            mock_destroy.assert_called_once_with()

    @patch("app.windows.messagebox")
    def test_confirm_discard_changes_messagebox(self, mock_messagebox, window_app_config):
        window_app_config.confirm_discard_changes()
        mock_messagebox.askyesno.assert_called_once_with("Unsaved Changes", "Discard unsaved changes?")

    def test_btn_apply_click(self, window_app_config):
        window_app_config.save_config = MagicMock()
        window_app_config.widgets.btn_apply.invoke()
        window_app_config.save_config.assert_called_once_with()

    def test_btn_save_click(self, window_app_config):
        window_app_config.save_config = MagicMock()
        window_app_config.destroy = MagicMock()
        window_app_config.handle_save_click()
        window_app_config.save_config.assert_called_once()
        window_app_config.destroy.assert_called_once()

    @patch("app.windows.messagebox")
    def test_save_config_success(self, mock_messagebox, window_app_config):
        window_app_config.save_config()
        window_app_config.app_config.save.assert_called_once_with()
        mock_messagebox.showinfo.assert_called_once_with(title="Saved!", message="Config saved!")

    @patch("app.windows.messagebox")
    def test_save_config_failure(self, mock_messagebox, window_app_config):
        e = Exception("Failed to save!")
        window_app_config.app_config.save.side_effect = e
        window_app_config.save_config()
        window_app_config.app_config.save.assert_called_once_with()
        mock_messagebox.showerror.assert_called_once_with(title="Error!", message=f"{e}")


class TestWindowCSVMapping:
    @patch("app.windows.WidgetList")
    @patch("app.windows.CSVMapping")
    @patch.object(WindowCSVMapping, "initialize_variables")
    @patch.object(WindowCSVMapping, "build_gui")
    def test_init(self, mock_build_gui, mock_initialize_variables,
                  mock_csv_mapping_class, mock_widget_list_class, root):
        mock_widget_list = MagicMock()
        mock_widget_list_class.return_value = mock_widget_list
        mock_csv_mapping = MagicMock()
        mock_csv_mapping_class.return_value = mock_csv_mapping
        window_csv_mapping = WindowCSVMapping(master=root)
        assert window_csv_mapping.widgets == mock_widget_list
        assert window_csv_mapping.mapping == mock_csv_mapping
        mock_initialize_variables.assert_called_once_with()
        mock_build_gui.assert_called_once_with()

    @patch("app.windows.messagebox")
    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_save_click(self, mock_destroy, mock_set_mapping_values, mock_messagebox, window_csv_mapping):
        window_csv_mapping.mapping = MagicMock()
        window_csv_mapping.widgets.btn_save.invoke()
        mock_set_mapping_values.assert_called_once_with()
        mock_messagebox.showinfo.assert_called_once_with(title="Saved!", message="Config saved!")
        mock_destroy.assert_called_once_with()

    def test_set_mapping_values(self):
        ...

    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "confirm_discard_changes")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_cancel_click_dirty_confirm_discard_changes(
            self, mock_destroy, mock_confirm_discard_changes, mock_set_mapping_values, window_csv_mapping):
        window_csv_mapping.mapping = MagicMock()
        window_csv_mapping.mapping.is_dirty = True
        mock_confirm_discard_changes.return_value = True
        window_csv_mapping.handle_cancel_click()
        mock_set_mapping_values.assert_called_once_with()
        window_csv_mapping.mapping.load.assert_called_once_with()
        mock_destroy.assert_called_once_with()

    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "confirm_discard_changes")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_cancel_click_dirty_dont_discard_changes(
            self, mock_destroy, mock_confirm_discard_changes, mock_set_mapping_values, window_csv_mapping):
        window_csv_mapping.mapping = MagicMock()
        window_csv_mapping.mapping.is_dirty = True
        mock_confirm_discard_changes.return_value = False
        window_csv_mapping.handle_cancel_click()
        mock_set_mapping_values.assert_called_once_with()
        window_csv_mapping.mapping.load.assert_not_called()
        mock_destroy.assert_not_called()

    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "confirm_discard_changes")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_cancel_click_not_dirty(
            self, mock_destroy, mock_confirm_discard_changes, mock_set_mapping_values, window_csv_mapping):
        window_csv_mapping.mapping = MagicMock()
        window_csv_mapping.mapping.is_dirty = False
        window_csv_mapping.handle_cancel_click()
        mock_confirm_discard_changes.assert_not_called()
        mock_set_mapping_values.assert_called_once_with()
        window_csv_mapping.mapping.load.assert_called_once_with()
        mock_destroy.assert_called_once_with()

    @patch("app.windows.messagebox")
    def test_confirm_discard_changes(self, mock_messagebox, window_csv_mapping):
        window_csv_mapping.confirm_discard_changes()
        mock_messagebox.askyesno.assert_called_once_with("Unsaved Changes", "Discard unsaved changes?")

    @patch("app.windows.askopenfilename")
    def test_browse_file_csv(self, mock_askopenfilename, window_csv_mapping):
        window_csv_mapping.var_csv_mapping_import_file_path = MagicMock()
        test_filename = 'test_filename.csv'
        mock_askopenfilename.return_value = test_filename
        window_csv_mapping.browse_file_csv()
        mock_askopenfilename.assert_called_once_with(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        window_csv_mapping.var_csv_mapping_import_file_path.set.assert_called_once_with(test_filename)

    def test_initialize_mapping_field_sets(self):
        ...


class TestWindowSync:
    @patch("app.windows.WidgetList")
    @patch.object(WindowSync, "build_gui")
    def test_init(self, mock_build_gui, mock_widget_list_class, root, mock_logger):
        mock_widget_list = mock_widget_list_class.return_value
        mock_widget_list.txt_output = MagicMock(spec=ScrolledText)

        window = WindowSync(master=root, logger=mock_logger)

        assert window.logger == mock_logger
        assert window.widgets == mock_widget_list
        assert window.is_paused is False
        assert window.sync_running is False

        mock_build_gui.assert_called_once_with()
        mock_logger.add_text_window_handler.assert_called_once_with(mock_widget_list.txt_output)

    @patch("app.windows.Thread")
    @patch.object(WindowSync, "periodic_update")
    def test_start_sync(self, mock_periodic_update, mock_thread_class, window_sync):
        mock_sync_thread = MagicMock()
        mock_thread_class.return_value = mock_sync_thread
        mock_master_run_sync_in_thread = window_sync.master.run_sync_in_thread = MagicMock()
        window_sync.start_sync()

        mock_thread_class.assert_called_once_with(target=mock_master_run_sync_in_thread)
        mock_sync_thread.start.assert_called_once_with()
        mock_periodic_update.assert_called_once_with()
        assert window_sync.sync_running is True

    def test_pause_sync(self, window_sync):
        window_sync.widgets.btn_pause_resume = MagicMock()
        window_sync.master.sync = MagicMock()
        window_sync.sync_running = True
        window_sync.is_paused = False
        window_sync.handle_pause_resume()
        # Test is_paused has flipped
        assert window_sync.is_paused is True
        window_sync.logger.log.assert_called_once_with(LogLevel.INFO, "Paused by user")
        window_sync.master.sync.pause_sync.assert_called_once_with()
        window_sync.widgets.btn_pause_resume.configure.assert_called_once_with(text="Resume")

    def test_resume_sync(self, window_sync):
        window_sync.widgets.btn_pause_resume = MagicMock()
        window_sync.master.sync = MagicMock()
        window_sync.sync_running = True
        window_sync.is_paused = True
        window_sync.handle_pause_resume()
        # Test is_paused has flipped
        assert window_sync.is_paused is False
        window_sync.logger.log.assert_called_once_with(LogLevel.INFO, "Resumed by user")
        window_sync.master.sync.resume_sync.assert_called_once_with()
        window_sync.widgets.btn_pause_resume.configure.assert_called_once_with(text="Pause")

    def test_pause_sync_not_running(self, window_sync):
        # If the sync isn't running then is_paused shouldn't change
        window_sync.sync_running = False
        originally_paused = window_sync.is_paused
        window_sync.handle_pause_resume()
        assert originally_paused == window_sync.is_paused

    @patch.object(WindowSync, "update")
    @patch.object(WindowSync, "after")
    def test_periodic_update(self, mock_after, mock_update, window_sync):
        window_sync.sync_running = True
        window_sync.periodic_update()
        mock_update.assert_called_once_with()
        mock_after.assert_called_once_with(100, window_sync.periodic_update)

    @patch.object(WindowSync, "update")
    @patch.object(WindowSync, "after")
    def test_periodic_update_not_running(self, mock_after, mock_update, window_sync):
        window_sync.sync_running = False
        window_sync.periodic_update()
        mock_update.assert_not_called()
        mock_after.assert_not_called()
