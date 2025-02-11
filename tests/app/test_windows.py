import pytest
import tkinter as tk
from unittest.mock import PropertyMock, call, patch, MagicMock
from app.widgets import ExtensionMappingFieldSet
from app.windows import (
    WindowAppConfig,
    WidgetList,
    PopupWindow,
    WindowSync,
    Window,
    WindowCSVMapping,
)
from tkinter.scrolledtext import ScrolledText
from tkinter import Button


class TestWindow:

    def test_window_default_row_and_column_are_zero(self, window):
        assert window._current_row == 0
        assert window._current_column == 0

    @patch.object(Window, "reset_row")
    @patch.object(Window, "reset_column")
    def test_reset_row_and_column(self, mock_reset_column, mock_reset_row, window):
        window.reset_row_and_column()
        mock_reset_column.assert_called_once()
        mock_reset_row.assert_called_once()

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
        mock_reset_column.assert_called_once()

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
        mock_increment_row.assert_called_once()

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
        mock_increment_column.assert_called_once()


class TestPopupWindow:
    @patch.object(PopupWindow, "grab_set")
    @patch.object(PopupWindow, "focus_force")
    def test_popup_window(self, mock_focus_force, mock_grab_set, root):
        window = PopupWindow(master=root)
        mock_focus_force.assert_called_once()
        mock_grab_set.assert_called_once()
        window.destroy()


class TestWindowAppConfig:
    @patch.object(WindowAppConfig, "build_gui")
    @patch.object(WindowAppConfig, "initialize_variables")
    def test_init(self, mock_initialize_variables, mock_build_gui, mock_app_config, root):
        window = WindowAppConfig(master=root, app_config=mock_app_config)
        assert isinstance(window, PopupWindow)
        assert isinstance(window.widgets, WidgetList)
        assert window.app_config == mock_app_config
        mock_initialize_variables.assert_called_once()
        mock_build_gui.assert_called_once()

    @pytest.mark.parametrize(
        "mock_app_config",
        [
            {
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
                },
            }
        ],
        indirect=True,
    )
    def test_initialize_variables_blank(self, mock_app_config, root):
        window = WindowAppConfig(master=root, app_config=mock_app_config)
        assert isinstance(window.vars, dict)
        assert isinstance(window.vars["3cx"]["scheme"], tk.StringVar)
        assert window.vars["3cx"]["scheme"].get() == ""
        assert isinstance(window.vars["3cx"]["domain"], tk.StringVar)
        assert window.vars["3cx"]["domain"].get() == ""
        assert isinstance(window.vars["3cx"]["port"], tk.StringVar)
        assert window.vars["3cx"]["port"].get() == ""
        assert isinstance(window.vars["3cx"]["username"], tk.StringVar)
        assert window.vars["3cx"]["username"].get() == ""
        assert isinstance(window.vars["3cx"]["password"], tk.StringVar)
        assert window.vars["3cx"]["password"].get() == ""
        assert isinstance(window.vars["3cx"]["store_credential_securely"], tk.BooleanVar)
        assert window.vars["3cx"]["store_credential_securely"].get() is False
        assert isinstance(window.vars["app"]["logout_hotdesk_on_disable"], tk.BooleanVar)
        assert window.vars["app"]["logout_hotdesk_on_disable"].get() is False

    @pytest.mark.parametrize(
        "mock_app_config",
        [
            {
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
                },
            }
        ],
        indirect=True,
    )
    def test_initialize_variables_with_values(self, mock_app_config, root):
        window = WindowAppConfig(master=root, app_config=mock_app_config)
        assert isinstance(window.vars, dict)
        assert isinstance(window.vars["3cx"]["scheme"], tk.StringVar)
        assert window.vars["3cx"]["scheme"].get() == "test_scheme"
        assert isinstance(window.vars["3cx"]["domain"], tk.StringVar)
        assert window.vars["3cx"]["domain"].get() == "test_domain"
        assert isinstance(window.vars["3cx"]["port"], tk.StringVar)
        assert window.vars["3cx"]["port"].get() == "test_port"
        assert isinstance(window.vars["3cx"]["username"], tk.StringVar)
        assert window.vars["3cx"]["username"].get() == "username"
        assert isinstance(window.vars["3cx"]["password"], tk.StringVar)
        assert window.vars["3cx"]["password"].get() == "password"
        assert isinstance(window.vars["3cx"]["store_credential_securely"], tk.BooleanVar)
        assert window.vars["3cx"]["store_credential_securely"].get() is True
        assert isinstance(window.vars["app"]["logout_hotdesk_on_disable"], tk.BooleanVar)
        assert window.vars["app"]["logout_hotdesk_on_disable"].get() is True

    @patch("app.windows.messagebox.showinfo")
    @patch("app.windows.ThreeCXApiConnection")
    def test_handle_test_connection_success(self, mock_api, mock_messagebox_showinfo, window_app_config):
        mock_api.return_value = mock_api
        window_app_config.widgets.btn_test.invoke()
        mock_api.authenticate.assert_called_once_with(
            username=window_app_config.app_config["3cx"]["username"],
            password=window_app_config.app_config["3cx"]["password"],
        )
        mock_messagebox_showinfo.assert_called_once_with(title="Success", message="Test Successful")

    @patch("app.windows.messagebox.showinfo")
    @patch("app.windows.ThreeCXApiConnection")
    def test_handle_test_connection_failure(self, mock_api, mock_messagebox_showinfo, window_app_config):
        mock_api.return_value = mock_api
        e = Exception("Authentication Failed")
        mock_api.authenticate.side_effect = e
        window_app_config.widgets.btn_test.invoke()
        mock_api.authenticate.assert_called_once_with(
            username=window_app_config.app_config["3cx"]["username"],
            password=window_app_config.app_config["3cx"]["password"],
        )
        mock_messagebox_showinfo.assert_called_once_with(title="Failure", message=f"Test Failed. {e}")

    def test_btn_cancel_click_is_dirty_confirm_discard(self, window_app_config):
        with patch.object(window_app_config, "destroy") as mock_destroy:
            window_app_config.app_config.is_dirty = True
            window_app_config.confirm_discard_changes = MagicMock()
            window_app_config.confirm_discard_changes.return_value = True
            window_app_config.widgets.btn_cancel.invoke()
            window_app_config.confirm_discard_changes.assert_called_once()
            window_app_config.app_config.load.assert_called_once()
            mock_destroy.assert_called_once()

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
            window_app_config.app_config.load.assert_called_once()
            mock_destroy.assert_called_once()

    @patch("app.windows.messagebox")
    def test_confirm_discard_changes_messagebox(self, mock_messagebox, window_app_config):
        window_app_config.confirm_discard_changes()
        mock_messagebox.askyesno.assert_called_once_with("Unsaved Changes", "Discard unsaved changes?")

    def test_btn_apply_click(self, window_app_config):
        window_app_config.save_config = MagicMock()
        window_app_config.widgets.btn_apply.invoke()
        window_app_config.save_config.assert_called_once()

    def test_btn_save_click(self, window_app_config):
        window_app_config.save_config = MagicMock()
        window_app_config.destroy = MagicMock()
        window_app_config.handle_save_click()
        window_app_config.save_config.assert_called_once()
        window_app_config.destroy.assert_called_once()

    @patch("app.windows.messagebox")
    def test_save_config_success(self, mock_messagebox, window_app_config):
        window_app_config.save_config()
        window_app_config.app_config.save.assert_called_once()
        mock_messagebox.showinfo.assert_called_once_with(title="Saved!", message="Config saved!")

    @patch("app.windows.messagebox")
    def test_save_config_failure(self, mock_messagebox, window_app_config):
        e = Exception("Failed to save!")
        window_app_config.app_config.save.side_effect = e
        window_app_config.save_config()
        window_app_config.app_config.save.assert_called_once()
        mock_messagebox.showerror.assert_called_once_with(title="Error!", message=f"{e}")


class TestWindowCSVMapping:

    @patch("app.windows.WidgetList")
    @patch.object(WindowCSVMapping, "initialize_variables")
    @patch.object(WindowCSVMapping, "build_gui")
    def test_init(
        self,
        mock_build_gui,
        mock_initialize_variables,
        mock_widget_list_class,
        root,
    ):
        mock_widget_list = MagicMock()
        mock_widget_list_class.return_value = mock_widget_list
        mock_csv_mapping = MagicMock()
        window_csv_mapping = WindowCSVMapping(master=root, csv_mapping=mock_csv_mapping)
        assert window_csv_mapping.widgets == mock_widget_list
        assert window_csv_mapping.mapping == mock_csv_mapping
        mock_initialize_variables.assert_called_once()
        mock_build_gui.assert_called_once()

    @patch("app.windows.messagebox")
    @patch.object(WindowCSVMapping, "set_mapping_values", return_value=MagicMock())
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_save_click(self, mock_destroy, mock_set_mapping_values, mock_messagebox, window_csv_mapping):
        window_csv_mapping.widgets.btn_save.invoke()

        mock_set_mapping_values.assert_called_once()
        mock_messagebox.showinfo.assert_called_once_with(title="Saved!", message="Config saved!")
        mock_destroy.assert_called_once()

    def test_set_mapping_values(self, window_csv_mapping):
        # Mock var_csv_mapping_import_file_path.get() return value
        window_csv_mapping.var_csv_mapping_import_file_path = MagicMock()
        window_csv_mapping.var_csv_mapping_import_file_path.get.return_value = "path/to/csv"

        # Mock mapping_fields with MagicMock for each field
        mock_row_1 = MagicMock()
        mock_row_1.header.get.return_value = "Header1"
        mock_row_1.field.get.return_value = "Field1"
        mock_row_1.key.checked = True
        mock_row_1.update.checked = False
        mock_row_1.static.checked = True

        mock_row_2 = MagicMock()
        mock_row_2.header.get.return_value = "Header2"
        mock_row_2.field.get.return_value = "Field2"
        mock_row_2.key.checked = False
        mock_row_2.update.checked = True
        mock_row_2.static.checked = False

        window_csv_mapping.mapping_fields = [mock_row_1, mock_row_2]

        # Prepare mapping to be updated
        window_csv_mapping.mapping = {}

        # Call method under test
        window_csv_mapping.set_mapping_values()

        # Assertions
        expected_mapping = {
            "Extension": {
                "Path": "path/to/csv",
                "Key": "Header1",  # Only row_1 has key.checked == True
                "New": {"Field1": "Header1", "Field2": "Header2"},
                "Update": ["Field2"],  # Only row_2 has update.checked == True
                "Static": ["Field1"],  # Only row_1 has static.checked == True
            }
        }

        assert window_csv_mapping.mapping == expected_mapping

    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "confirm_discard_changes")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_cancel_click_dirty_confirm_discard_changes(
        self,
        mock_destroy,
        mock_confirm_discard_changes,
        mock_set_mapping_values,
        window_csv_mapping,
    ):
        window_csv_mapping.mapping.is_dirty = True
        mock_confirm_discard_changes.return_value = True
        window_csv_mapping.handle_cancel_click()
        mock_set_mapping_values.assert_called_once()
        window_csv_mapping.mapping.load.assert_called_once()
        mock_destroy.assert_called_once()

    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "confirm_discard_changes")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_cancel_click_dirty_dont_discard_changes(
        self,
        mock_destroy,
        mock_confirm_discard_changes,
        mock_set_mapping_values,
        window_csv_mapping,
    ):
        window_csv_mapping.mapping = MagicMock()
        window_csv_mapping.mapping.is_dirty = True
        mock_confirm_discard_changes.return_value = False
        window_csv_mapping.handle_cancel_click()
        mock_set_mapping_values.assert_called_once()
        window_csv_mapping.mapping.load.assert_not_called()
        mock_destroy.assert_not_called()

    @patch.object(WindowCSVMapping, "set_mapping_values")
    @patch.object(WindowCSVMapping, "confirm_discard_changes")
    @patch.object(WindowCSVMapping, "destroy")
    def test_handle_cancel_click_not_dirty(
        self,
        mock_destroy,
        mock_confirm_discard_changes,
        mock_set_mapping_values,
        window_csv_mapping,
    ):
        window_csv_mapping.mapping = MagicMock()
        window_csv_mapping.mapping.is_dirty = False
        window_csv_mapping.handle_cancel_click()
        mock_confirm_discard_changes.assert_not_called()
        mock_set_mapping_values.assert_called_once()
        window_csv_mapping.mapping.load.assert_called_once()
        mock_destroy.assert_called_once()

    @patch("app.windows.messagebox")
    def test_confirm_discard_changes(self, mock_messagebox, window_csv_mapping):
        window_csv_mapping.confirm_discard_changes()
        mock_messagebox.askyesno.assert_called_once_with("Unsaved Changes", "Discard unsaved changes?")

    @patch("app.windows.askopenfilename")
    def test_browse_file_csv(self, mock_askopenfilename, window_csv_mapping):
        window_csv_mapping.var_csv_mapping_import_file_path = MagicMock()
        test_filename = "test_filename.csv"
        mock_askopenfilename.return_value = test_filename
        window_csv_mapping.browse_file_csv()
        mock_askopenfilename.assert_called_once_with(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        window_csv_mapping.var_csv_mapping_import_file_path.set.assert_called_once_with(test_filename)

    @patch.object(WindowCSVMapping, "add_mapping_field_set")
    def test_initialize_mapping_field_sets(self, mock_add_mapping_field_set, window_csv_mapping):
        window_csv_mapping.mapping.get_parsed_config.return_value = [
            {"test": "test_data_1"},
            {"test": "test_data_2"},
            {"test": "test_data_3"},
        ]

        window_csv_mapping.initialize_mapping_field_sets(starting_row=1)
        mock_add_mapping_field_set.assert_has_calls(
            [call(row=1, test="test_data_1"), call(row=2, test="test_data_2"), call(row=3, test="test_data_3")]
        )

    @patch.object(WindowCSVMapping, "add_mapping_field_set")
    @patch.object(WindowCSVMapping, "resize")
    def test_handle_button_add_mapping_field_set(self, mock_resize, mock_add_mapping_field_set, window_csv_mapping):
        window_csv_mapping.mapping_fields = [1, 2, 3]
        window_csv_mapping.handle_button_add_mapping_field_set()
        mock_add_mapping_field_set.assert_called_once_with(row=4)
        mock_resize.assert_called_once()

    @patch("app.windows.ttk")
    @patch("app.windows.Checkbox")
    @patch("app.windows.ExtensionMappingFieldSet")
    def test_add_mapping_field_set(
        self, mock_extension_mapping_field_set_class, mock_checkbox_class, mock_ttk_class, window_csv_mapping
    ):
        mock_extension_mapping_field_set = MagicMock()
        mock_extension_mapping_field_set_class.return_value = mock_extension_mapping_field_set
        mock_lblfrm = MagicMock()
        window_csv_mapping.widgets.lblfrm_csv_mapping_fields = mock_lblfrm
        mock_entry = MagicMock()
        mock_button = MagicMock()
        mock_checkbox = MagicMock()
        mock_ttk_class.Entry.return_value = mock_entry
        mock_ttk_class.Button.return_value = mock_button
        mock_checkbox_class.return_value = mock_checkbox

        window_csv_mapping.add_mapping_field_set(
            row=2, header="Header1", field="Field1", static=True, update=False, key=True
        )

        # Check if widgets were created and grid called with correct row/column
        assert len(window_csv_mapping.mapping_fields) == 1

        mock_ttk_class.Entry.assert_any_call(mock_lblfrm)
        mock_entry.grid.assert_any_call(row=2, column=0, sticky="ew")
        mock_entry.grid.assert_any_call(row=2, column=1, sticky="ew")
        mock_entry.insert.assert_any_call(0, "Header1")
        mock_entry.insert.assert_any_call(0, "Field1")

        mock_checkbox_class.assert_any_call(mock_lblfrm, value=True)
        mock_checkbox_class.assert_any_call(mock_lblfrm, value=False)

        mock_checkbox.grid.assert_any_call(row=2, column=2, sticky="w")
        mock_checkbox.grid.assert_any_call(row=2, column=3, sticky="w")
        mock_checkbox.grid.assert_any_call(row=2, column=4, sticky="w")
        mock_checkbox.invoke.assert_called_once_with()

        mock_ttk_class.Button.assert_called_once_with(mock_lblfrm, width=2, text="−")
        mock_button.grid.assert_any_call(row=2, column=5, padx=2, pady=2)

        mock_extension_mapping_field_set_class.assert_called_once()
        assert window_csv_mapping.mapping_fields == [mock_extension_mapping_field_set]

    @patch.object(WindowCSVMapping, "delete_mapping_field_set_by_row_index")
    @patch.object(WindowCSVMapping, "resize")
    def test_handle_button_delete_mapping_field_set(
        self, mock_resize, mock_delete_mapping_field_set_by_row_index, window_csv_mapping
    ):
        window_csv_mapping.mapping_fields = [1, 2, 3]
        window_csv_mapping.handle_button_delete_mapping_field_set()
        mock_delete_mapping_field_set_by_row_index.assert_called_once_with(2)
        mock_resize.assert_called_once()

    @patch.object(WindowCSVMapping, "delete_mapping_field_set_by_row_index")
    def test_handle_button_delete_specific_mapping_field_set(
        self, mock_delete_mapping_field_set_by_row_index, window_csv_mapping
    ):
        mock_delete_button = MagicMock(spec=Button)
        mock_delete_button1 = MagicMock(spec=Button)
        mock_delete_button2 = MagicMock(spec=Button)
        field_set = ExtensionMappingFieldSet(
            None,
            None,
            None,
            None,
            None,
            delete=mock_delete_button,
        )
        field_set1 = ExtensionMappingFieldSet(
            None,
            None,
            None,
            None,
            None,
            delete=mock_delete_button1,
        )
        field_set2 = ExtensionMappingFieldSet(
            None,
            None,
            None,
            None,
            None,
            delete=mock_delete_button2,
        )
        window_csv_mapping.mapping_fields = [field_set, field_set1, field_set2]
        window_csv_mapping.handle_button_delete_specific_mapping_field_set(mock_delete_button2)
        mock_delete_mapping_field_set_by_row_index.assert_called_once_with(2)

    @patch.object(WindowCSVMapping, "enable_key_checkboxes")
    @patch.object(WindowCSVMapping, "shift_rows_up")
    def test_delete_mapping_field_set_by_row_index(
        self, mock_shift_rows_up, mock_enable_key_checkboxes, window_csv_mapping
    ):
        mock_row = MagicMock()
        mock_row.key = MagicMock(checked=True)

        window_csv_mapping.mapping_fields = MagicMock()
        window_csv_mapping.mapping_fields.pop.return_value = mock_row

        window_csv_mapping.delete_mapping_field_set_by_row_index(5)

        window_csv_mapping.mapping_fields.pop.assert_called_once_with(5)
        mock_row.destroy.assert_called_once()
        mock_shift_rows_up.assert_called_once_with(starting_row=5)
        mock_enable_key_checkboxes.assert_called_once()

    def test_reindex_mapping_field_rows(self, window_csv_mapping):
        ...
        mock_field_1 = MagicMock()
        mock_field_2 = MagicMock()
        mock_field_3 = MagicMock()
        window_csv_mapping.mapping_fields = [mock_field_1, mock_field_2, mock_field_3]
        window_csv_mapping.shift_rows_up(1)

        mock_field_1.change_row.assert_not_called()
        mock_field_2.change_row.assert_called_once_with(row=2)
        mock_field_3.change_row.assert_called_once_with(row=3)

    @patch.object(WindowCSVMapping, "geometry")
    @patch.object(WindowCSVMapping, "winfo_width")
    def test_resize(self, mock_winfo_width, mock_gemoetry, window_csv_mapping):
        window_csv_mapping.widgets = MagicMock()
        mock_winfo_width.return_value = 100
        window_csv_mapping.widgets.frm_window.winfo_reqheight.return_value = 2000
        window_csv_mapping.resize()
        window_csv_mapping.widgets.frm_window.update_idletasks.assert_called_once()
        mock_winfo_width.assert_called_once()
        mock_gemoetry.assert_called_once_with("100x2020")

    @patch.object(WindowCSVMapping, "disable_key_checkboxes")
    @patch.object(WindowCSVMapping, "enable_key_checkboxes")
    def test_handle_checkbox_key_change_normal(
        self, mock_enable_key_checkboxes, mock_disable_key_checkboxes, window_csv_mapping
    ):
        window_csv_mapping.checkbox_key_state = MagicMock()
        window_csv_mapping.checkbox_key_state.get.return_value = "normal"

        window_csv_mapping.handle_checkbox_key_change()

        mock_disable_key_checkboxes.assert_called_once()
        mock_enable_key_checkboxes.assert_not_called()

    @patch.object(WindowCSVMapping, "disable_key_checkboxes")
    @patch.object(WindowCSVMapping, "enable_key_checkboxes")
    def test_handle_checkbox_key_change_disable(
        self, mock_enable_key_checkboxes, mock_disable_key_checkboxes, window_csv_mapping
    ):
        window_csv_mapping.checkbox_key_state = MagicMock()
        window_csv_mapping.checkbox_key_state.get.return_value = "disable"

        window_csv_mapping.handle_checkbox_key_change()

        mock_disable_key_checkboxes.assert_not_called()
        mock_enable_key_checkboxes.assert_called_once()

    def test_disable_key_checkboxes(self, window_csv_mapping):
        window_csv_mapping.checkbox_key_state = MagicMock()
        checked_key = MagicMock(checked=False)
        unchecked_key = MagicMock(checked=True)
        row_1 = MagicMock(key=checked_key)
        row_2 = MagicMock(key=unchecked_key)
        window_csv_mapping.mapping_fields = [row_1, row_2]

        window_csv_mapping.disable_key_checkboxes()

        window_csv_mapping.checkbox_key_state.set.assert_called_once_with("disable")
        checked_key.configure.assert_called_once_with(state="disable")
        unchecked_key.configure.assert_not_called()

    def test_enable_key_checkboxes(self, window_csv_mapping):
        window_csv_mapping.checkbox_key_state = MagicMock()
        checked_key = MagicMock(checked=False)
        unchecked_key = MagicMock(checked=True)
        row_1 = MagicMock(key=checked_key)
        row_2 = MagicMock(key=unchecked_key)
        window_csv_mapping.mapping_fields = [row_1, row_2]

        window_csv_mapping.enable_key_checkboxes()

        window_csv_mapping.checkbox_key_state.set.assert_called_once_with("normal")
        checked_key.configure.assert_called_once_with(state="normal")
        unchecked_key.configure.assert_called_once_with(state="normal")


class TestWindowSync:
    @patch("app.windows.WidgetList")
    @patch.object(WindowSync, "build_gui")
    def test_init(self, mock_build_gui, mock_widget_list_class, app):
        mock_widget_list_class.return_value.txt_output = MagicMock(spec=ScrolledText)
        window = WindowSync(master=app)

        assert window.widgets == mock_widget_list_class.return_value
        mock_build_gui.assert_called_once()
        app.logger.add_text_window_handler.assert_called_once_with(mock_widget_list_class.return_value.txt_output)

    def test_handle_pause_resume(self, window_sync):
        # Mock the sync object
        window_sync.update_btn_pause_resume_text = MagicMock()
        window_sync.master.sync = MagicMock()
        mock_master_toggle_sync_state = MagicMock()
        window_sync.master.toggle_sync_state = mock_master_toggle_sync_state

        # Simulate if already paused
        type(window_sync.master.sync).is_paused = PropertyMock(return_value=True)
        window_sync.handle_pause_resume()  # Sync Resumed
        window_sync.update_btn_pause_resume_text.assert_called_once()

    def test_update_btn_pause_resume_text(self, window_sync):
        # Mock the sync object
        window_sync.master.sync = MagicMock()

        # Simulate if resumed and we update the button text
        type(window_sync.master.sync).is_paused = PropertyMock(return_value=False)
        window_sync.update_btn_pause_resume_text()
        assert window_sync.widgets.btn_pause_resume.cget("text") == "Pause"

        # Simulate if paused and we update the button text
        type(window_sync.master.sync).is_paused = PropertyMock(return_value=True)
        window_sync.update_btn_pause_resume_text()  # Sync Resumed
        assert window_sync.widgets.btn_pause_resume.cget("text") == "Resume"

    def test_handle_pause_resume_sync_is_none(self, window_sync):
        # Set so that sync is running and not paused
        window_sync.update_btn_pause_resume_text = MagicMock()
        window_sync.master = MagicMock()
        window_sync.master.sync = None

        window_sync.handle_pause_resume()
        window_sync.master.toggle_sync_state.assert_not_called()
        window_sync.update_btn_pause_resume_text.assert_not_called()

    @patch.object(WindowSync, "update")
    @patch.object(WindowSync, "after")
    def test_periodic_update(self, mock_after, mock_update, window_sync):
        window_sync.master.sync = MagicMock()
        type(window_sync.master.sync).is_terminated = PropertyMock(return_value=False)
        window_sync.periodic_update()
        mock_update.assert_called_once()
        mock_after.assert_called_once_with(100, window_sync.periodic_update)

    @patch.object(WindowSync, "update")
    @patch.object(WindowSync, "after")
    def test_periodic_update_master_sync_is_none(self, mock_after, mock_update, window_sync):
        window_sync.master.sync = None
        window_sync.periodic_update()
        mock_update.assert_not_called()
        mock_after.assert_not_called()

    @patch.object(WindowSync, "update")
    @patch.object(WindowSync, "after")
    def test_periodic_update_master_sync_is_terminated(self, mock_after, mock_update, window_sync):
        window_sync.master.sync = MagicMock()
        type(window_sync.master.sync).is_terminated = PropertyMock(return_value=True)
        window_sync.periodic_update()
        mock_update.assert_not_called()
        mock_after.assert_not_called()

    def test_on_destroy_is_registered(self, window_sync):
        assert window_sync.protocol("WM_DELETE_WINDOW").endswith("on_destroy")

    def test_wait_for_sync_thread_is_alive(self, window_sync):
        window_sync.master.sync_thread = MagicMock()
        window_sync.master.sync_thread.is_alive = MagicMock(return_value=True)
        window_sync.wait_for_sync_thread()
        window_sync.master.sync_thread.join.assert_called_once()

    def test_wait_for_sync_thread_is_not_alive(self, window_sync):
        window_sync.master.sync_thread = MagicMock()
        window_sync.master.sync_thread.is_alive = MagicMock(return_value=False)
        window_sync.wait_for_sync_thread()
        window_sync.master.sync_thread.join.assert_not_called()

    def test_on_destroy(self, window_sync):
        window_sync.master.terminate_sync = MagicMock()
        window_sync.destroy = MagicMock()
        window_sync.wait_for_sync_thread = MagicMock()
        window_sync.on_destroy()

        window_sync.master.logger.remove_text_window_handler.assert_called_once_with(window_sync.widgets.txt_output)
        window_sync.destroy.assert_called_once()
        window_sync.master.terminate_sync.assert_called_once()
        window_sync.wait_for_sync_thread.assert_called_once()
