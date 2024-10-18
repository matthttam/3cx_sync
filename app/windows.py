import tkinter as tk
from tkinter import ttk
from tcx_api.tcx_api_connection import TCX_API_Connection
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from app.widgets import Checkbox, ExtensionMappingFieldSet, WidgetList
from app.config import AppConfig
from app.mapping import CSVMapping
from tkinter.scrolledtext import ScrolledText
import threading
from sync.logging import SyncLogger


def update_nested_dict(d: dict, keys: list, value) -> None:
    """Update a nested dictionary with the given keys and value."""
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


class Window:
    header_y_padding = (5, 15)
    paragraph_x_padding = (15, 0)
    frame_iy_padding = 5
    _current_row = 0
    _current_column = 0

    # Default configurations
    lbl_grid_defaults = {"padx": (0, 10), "sticky": tk.E}
    lbl_pack_defaults = {"padx": (0, 10), "fill": tk.X}
    ent_grid_defaults = {"pady": (5, 5), "sticky": tk.EW}
    ent_pack_defaults = {"pady": (5, 5), "fill": tk.X}
    frm_default = {"padx": 5, "pady": 5, "side": tk.LEFT}
    btn_pack_default = {"padx": 5, "pady": (5, 5), "fill": tk.X}
    lblfrm_defaults = {"padx": 20, "pady": 10, "fill": tk.BOTH, "expand": True}
    chk_defaults = {"padx": 5, "pady": 5}

    def increment_row(self, reset_column=True) -> None:
        self._current_row = self._current_row + 1
        if reset_column:
            self.reset_column()

    def reset_row_and_column(self) -> None:
        self._current_row = 0
        self.reset_column()

    def get_current_row(self) -> int:
        return self._current_row

    def get_next_row(self, increment=True) -> int:
        current_row = self._current_row
        if increment:
            self.increment_row()
        return current_row

    def increment_column(self) -> None:
        self._current_column = self._current_column + 1

    def reset_column(self) -> None:
        self._current_column = 0

    def get_next_column(self, increment=True) -> int:
        current_column = self._current_column
        if increment:
            self.increment_column()
        return current_column


class PopupWindow(tk.Toplevel, Window):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grab_set()
        self.focus_force()


class WindowAppConfig(PopupWindow):

    def __init__(self, master, app_config: AppConfig, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.resizable(height=False, width=False)
        self.widgets = WidgetList()
        self.app_config = app_config
        # self.app_config.load()
        self.initialize_variables()
        self.build_gui()

    def initialize_variables(self) -> None:
        self.vars = {"3cx": {}, "app": {}}

        # Helper to add trace to the tk variables
        def trace_tk_variables(tk_var: tk.Variable, section, var):
            tk_var.trace_add(
                "write",
                lambda *args: self.app_config.set_value(
                    section, var, str(tk_var.get())
                ),
            )

        # Create StringVars for '3cx' section
        section = "3cx"
        for var in ["scheme", "domain", "port", "username", "password"]:
            tk_var = tk.StringVar(self, self.app_config.get(section, var))
            self.vars[section][var] = tk_var
            trace_tk_variables(tk_var, section, var)

        # Create BooleanVars for '3cx' section
        for var in ["store_credential_securely"]:
            tk_var = tk.BooleanVar(self, self.app_config.getboolean(section, var))
            self.vars[section][var] = tk_var
            trace_tk_variables(tk_var, section, var)

        # Create BooleanVars for 'app' section
        section = "app"
        for var in ["logout_hotdesk_on_disable"]:
            tk_var = tk.BooleanVar(self, self.app_config.getboolean(section, var))
            self.vars[section][var] = tk_var
            trace_tk_variables(tk_var, section, var)

    def build_gui(self) -> None:
        # Create a window frame
        self.widgets.frm_window = ttk.Frame(self)
        self.widgets.frm_window.pack(fill="both", expand=True)

        self.widgets.frm_3cx_options = ttk.LabelFrame(
            self.widgets.frm_window, text="3CX Settings", padding=(20, 10)
        )
        self.widgets.frm_3cx_options.pack(**self.lblfrm_defaults)

        # Create the 3cx header
        # self.widgets.lbl_3cx_settings_header = ttk.Label(
        #    self.widgets.frm_window,
        #    text="3CX Settings",
        #    font=("Arial", 15),
        # )
        # self.widgets.lbl_3cx_settings_header.pack()

        # Create the 3cx options frame
        # self.widgets.frm_3cx_options = ttk.Frame(self.widgets.frm_window)
        # self.widgets.frm_3cx_options.config(
        #    width=300, height=200, relief="ridge", borderwidth=2
        # )
        # self.widgets.frm_3cx_options.pack(fill="both", expand=True)
        # self.lbl_defaults = {"padx": (0, 10), "sticky": tk.E}
        # self.frm_field_defaults = {"pady": (5, 5), "sticky": tk.EW}
        # Create the 3cx URL
        self.widgets.lbl_3cx_url = ttk.Label(
            self.widgets.frm_3cx_options, text="3CX URL:"
        )
        self.widgets.lbl_3cx_url.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.lbl_grid_defaults,
        )

        # Create a 3cx URL frame in that window
        self.widgets.frm_3cx_url = ttk.Frame(self.widgets.frm_3cx_options)
        self.widgets.frm_3cx_url.grid_columnconfigure(2, weight=1)
        self.widgets.frm_3cx_url.grid(
            row=self.get_current_row(), column=self.get_next_column(), pady=(0, 5)
        )

        # Create the 3CX URL widgets
        self.widgets.opt_3cx_scheme = ttk.OptionMenu(
            self.widgets.frm_3cx_url, self.vars["3cx"]["scheme"], *["https", "http"]
        )
        self.widgets.lbl_3cx_scheme_ending = ttk.Label(
            self.widgets.frm_3cx_url, text="://"
        )
        self.widgets.ent_3cx_domain = ttk.Entry(
            self.widgets.frm_3cx_url,
            textvariable=self.vars["3cx"]["domain"],
        )
        self.widgets.lbl_3cx_server_ending = ttk.Label(
            self.widgets.frm_3cx_url, text=":"
        )
        self.widgets.ent_3cx_port = ttk.Entry(
            self.widgets.frm_3cx_url,
            textvariable=self.vars["3cx"]["port"],
            width=5,
        )

        self.widgets.opt_3cx_scheme.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )
        self.widgets.lbl_3cx_scheme_ending.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )
        self.widgets.ent_3cx_domain.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )
        self.widgets.lbl_3cx_server_ending.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )
        self.widgets.ent_3cx_port.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )

        # Create the 3CX username widgets
        self.widgets.lbl_3cx_username = ttk.Label(
            self.widgets.frm_3cx_options,
            text="Username:",
        )
        self.widgets.ent_3cx_username = ttk.Entry(
            self.widgets.frm_3cx_options,
            textvariable=self.vars["3cx"]["username"],
        )

        self.increment_row()
        self.widgets.lbl_3cx_username.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.lbl_grid_defaults,
        )
        self.widgets.ent_3cx_username.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )

        # Create the 3CX password widgets
        self.widgets.lbl_3cx_password = ttk.Label(
            self.widgets.frm_3cx_options, text="Password:"
        )
        self.widgets.ent_3cx_password = ttk.Entry(
            self.widgets.frm_3cx_options,
            textvariable=self.vars["3cx"]["password"],
            show="*",
        )

        self.increment_row()
        self.widgets.lbl_3cx_password.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.lbl_grid_defaults,
        )
        self.widgets.ent_3cx_password.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.ent_grid_defaults,
        )

        # Create the Store credential securely widgets
        self.widgets.lbl_store_credential_securely = ttk.Label(
            self.widgets.frm_3cx_options,
            text="Store Credential Securely:",
        )
        self.widgets.chk_store_credential_securely = ttk.Checkbutton(
            self.widgets.frm_3cx_options,
            variable=self.vars["3cx"]["store_credential_securely"],
        )

        self.increment_row()
        self.widgets.lbl_store_credential_securely.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.lbl_grid_defaults,
        )
        self.widgets.chk_store_credential_securely.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            sticky="w",
            **self.chk_defaults,
        )

        # Create the test button widget
        self.widgets.btn_test = ttk.Button(
            self.widgets.frm_3cx_options,
            name="btn_test",
            text="Test",
            command=self.handle_test_connection,
        )

        self.increment_row()
        self.increment_column()
        self.widgets.btn_test.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            columnspan=2,
            padx=5,
            pady=5,
            sticky="we",
        )

        # Create the App Settings header
        self.widgets.lblfrm_app_settings = ttk.LabelFrame(
            self.widgets.frm_window, text="App Settings", padding=(20, 10)
        )
        self.widgets.lblfrm_app_settings.pack(**self.lblfrm_defaults)
        # self.widgets.lbl_app_settings_header = ttk.Label(
        #    self.widgets.frm_window,
        #    text="App Settings",
        #    font=("Arial", 15),
        # )
        # self.widgets.lbl_app_settings_header.pack()

        # Create the form App Options
        # self.widgets.frm_app_options = ttk.Frame(
        #    self.widgets.lbl_app_settings_header,
        #    width=300,
        #    height=200,
        #    relief="ridge",
        #    borderwidth=2,
        # )
        # self.widgets.frm_app_options.pack(fill="both", expand=True)

        # Create the Log out hotdesk on disable widgets
        self.widgets.lbl_app_logout_hotdesk_on_disable = ttk.Label(
            self.widgets.lblfrm_app_settings,
            text="Logout hotdesk on disable:",
        )
        self.widgets.chk_app_logout_hotdesk_on_disable = ttk.Checkbutton(
            self.widgets.lblfrm_app_settings,
            variable=self.vars["app"]["logout_hotdesk_on_disable"],
        )
        self.reset_row_and_column()
        self.widgets.lbl_app_logout_hotdesk_on_disable.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.lbl_grid_defaults,
        )
        self.widgets.chk_app_logout_hotdesk_on_disable.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            sticky="w",
            **self.chk_defaults,
        )

        # Create the Apply, Save, and Cnacel Buttons
        self.widgets.frm_navigation = ttk.Frame(self.widgets.frm_window)
        self.widgets.btn_apply = ttk.Button(
            self.widgets.frm_navigation,
            text="Apply",
            command=self.handle_apply_click,
        )
        self.widgets.btn_save = ttk.Button(
            self.widgets.frm_navigation,
            text="Save",
            command=self.handle_save_click,
        )
        self.widgets.btn_cancel = ttk.Button(
            self.widgets.frm_navigation,
            text="Cancel",
            command=self.handle_cancel_click,
        )

        self.widgets.frm_navigation.pack(side="bottom", anchor="e")
        self.reset_row_and_column()
        self.increment_column()
        self.widgets.btn_apply.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.btn_pack_default,
        )
        self.widgets.btn_save.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.btn_pack_default,
        )
        self.widgets.btn_cancel.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            **self.btn_pack_default,
        )

    def handle_test_connection(self):
        api = TCX_API_Connection(server_url=self.app_config.server_url)

        try:
            api.authenticate(
                username=self.app_config["3cx"]["username"],
                password=self.app_config["3cx"]["password"],
            )
            messagebox.showinfo(title="Success", message="Test Successful")
        except Exception as e:
            messagebox.showinfo(title="Failure", message=f"Test Failed. {str(e)}")

    def handle_apply_click(self):
        self.save_config()

    def handle_save_click(self):
        self.save_config()
        self.destroy()

    def handle_cancel_click(self):
        if self.app_config.is_dirty:
            if not self.confirm_discard_changes():
                return
        self.app_config.load()
        self.destroy()

    def confirm_discard_changes(self) -> bool:
        return messagebox.askyesno(
            "Unsaved Changes",
            "Discard unsaved changes?",
        )

    def save_config(self):
        try:
            self.app_config.save()
            messagebox.showinfo(title="Saved!", message="Config saved!")
        except Exception as e:
            messagebox.showerror(title="Error!", message=f"{e}")


class WindowCSVMapping(PopupWindow):

    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.widgets = WidgetList()
        self.mapping = CSVMapping()
        self.title("CSV Mapping Settings")
        self.initialize_variables()
        self.build_gui()

    def initialize_variables(self) -> None:
        self.mapping_fields = []
        self.ceckbox_key_state = tk.StringVar(self, "normal")
        extension = self.mapping.get("Extension", {})
        self.var_csv_mapping_import_file_path = tk.StringVar(
            self, value=extension.get("Path", "")
        )
        self.key_checked = False

    def build_gui(self) -> None:
        # Frame: window
        self.widgets.frm_window = ttk.Frame(self, name="csv_mapping")
        self.widgets.frm_window.pack(fill="both", expand=True)

        # Field: Extension Path
        self.widgets.lblfrm_import_file_path = ttk.LabelFrame(
            self.widgets.frm_window, text="Import File Path", padding=(20, 10)
        )
        self.widgets.lblfrm_import_file_path.pack(**self.lblfrm_defaults)

        self.widgets.lbl_import_file_path = ttk.Label(
            self.widgets.lblfrm_import_file_path, text="Path:"
        )
        self.widgets.lbl_import_file_path.pack(**self.lbl_pack_defaults)

        self.widgets.ent_import_file_path = ttk.Entry(
            self.widgets.lblfrm_import_file_path,
            textvariable=self.var_csv_mapping_import_file_path,
        )
        self.widgets.ent_import_file_path.pack(**self.ent_pack_defaults)

        self.widgets.btn_import_file_path_browse = ttk.Button(
            self.widgets.lblfrm_import_file_path, text=">", command=self.browse_file_csv
        )
        self.widgets.btn_import_file_path_browse.pack(
            **self.btn_pack_default,
        )

        # Frame: Mapping
        self.widgets.frm_csv_mapping = ttk.Frame(
            self.widgets.frm_window, relief="ridge", borderwidth=2
        )
        self.widgets.frm_csv_mapping.pack(
            side="top", fill="both", ipady=self.frame_iy_padding, expand=True
        )

        # Frame: CSV Mapping Fields
        self.widgets.frm_csv_mapping_fields = ttk.Frame(
            self.widgets.frm_window,
            name="csv_mapping_fields",
            relief="sunken",
            borderwidth=2,
        )
        self.widgets.frm_csv_mapping_fields.pack(
            side="top", fill="both", ipady=self.frame_iy_padding, expand=True
        )

        # CSV Mapping Headers
        self.widgets.lbl_csv_mapping_3cx_field = ttk.Label(
            self.widgets.frm_csv_mapping_fields, text="3cx Field", width=20
        )
        self.widgets.lbl_csv_mapping_header = ttk.Label(
            self.widgets.frm_csv_mapping_fields, text="CSV Header", width=20
        )
        self.widgets.lbl_csv_mapping_update = ttk.Label(
            self.widgets.frm_csv_mapping_fields, text="Static", width=5
        )
        self.widgets.lbl_csv_mapping_update = ttk.Label(
            self.widgets.frm_csv_mapping_fields, text="Update", width=5
        )
        self.widgets.lbl_csv_mapping_key = ttk.Label(
            self.widgets.frm_csv_mapping_fields, text="Key", width=5
        )
        self.widgets.lbl_csv_mapping_3cx_field.grid(row=1, column=1, sticky="w")
        self.widgets.lbl_csv_mapping_header.grid(row=1, column=2, sticky="w")
        self.widgets.lbl_csv_mapping_update.grid(row=1, column=3, sticky="w")
        self.widgets.lbl_csv_mapping_update.grid(row=1, column=4, sticky="w")
        self.widgets.lbl_csv_mapping_key.grid(row=1, column=5, sticky="w")

        # self.add_mapping_field_set()
        self.initialize_mapping_field_sets()

        # Frame: Add Remove Fields
        self.widgets.frm_add_delete_fields = ttk.Frame(self.widgets.frm_window)
        self.widgets.btn_add_field = ttk.Button(
            self.widgets.frm_add_delete_fields,
            text="+",
            command=self.add_mapping_field_set,
        )
        self.widgets.btn_delete_field = ttk.Button(
            self.widgets.frm_add_delete_fields,
            text="-",
            command=self.delete_mapping_field_set,
        )

        self.widgets.frm_add_delete_fields.pack(
            side="top", anchor="center", expand=True, fill="both"
        )
        self.widgets.btn_add_field.grid(row=1, column=1)
        self.widgets.btn_delete_field.grid(row=1, column=2)

        # Frame: Navigation
        self.widgets.frm_navigation = ttk.Frame(self.widgets.frm_window)
        self.widgets.btn_save = ttk.Button(
            self.widgets.frm_navigation,
            text="Save",
            command=self.handle_save_click,
        )
        self.widgets.btn_cancel = ttk.Button(
            self.widgets.frm_navigation,
            text="Cancel",
            command=self.handle_cancel_click,
        )
        self.widgets.frm_navigation.pack(side="bottom", anchor="e", expand=True)
        self.widgets.btn_save.grid(row=1, column=1, padx=5)
        self.widgets.btn_cancel.grid(row=1, column=2, padx=5)

    def handle_save_click(self):
        self.set_mapping_values()
        self.mapping.save()
        messagebox.showinfo(title="Saved!", message="Config saved!")
        self.destroy()

    def set_mapping_values(self):
        """Update the mapping config with values from the form"""
        self.mapping["Extension"] = {
            "Path": self.var_csv_mapping_import_file_path.get(),
        }
        mapping_new = {}
        mapping_update = []
        mapping_static = []
        for mapping_row in self.mapping_fields:
            if mapping_row.key.checked:
                self.mapping["Extension"]["Key"] = mapping_row.header.get()
            mapping_new[mapping_row.field.get()] = mapping_row.header.get()
            if mapping_row.update.checked:
                mapping_update.append(mapping_row.field.get())
            if mapping_row.static.checked:
                mapping_static.append(mapping_row.field.get())
        self.mapping["Extension"]["New"] = mapping_new
        self.mapping["Extension"]["Update"] = mapping_update
        self.mapping["Extension"]["Static"] = mapping_static

    def handle_cancel_click(self):
        self.set_mapping_values()
        if self.mapping.is_dirty:
            if not self.confirm_discard_changes():
                return
        self.mapping.load()
        self.destroy()

    def confirm_discard_changes(self) -> bool:
        return messagebox.askyesno(
            "Unsaved Changes",
            "Discard unsaved changes?",
        )

    def browse_file_csv(self):
        filename = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        self.var_csv_mapping_import_file_path.set(filename)

    def initialize_mapping_field_sets(self):
        extension_mapping = self.mapping.get("Extension", {})
        new_mapping = extension_mapping.get("New", {})
        key_header = extension_mapping.get("Key", None)

        for field, header in new_mapping.items():
            key = header == key_header
            update = field in extension_mapping.get("Update", {})
            static = field in extension_mapping.get("Static", {})
            self.add_mapping_field_set(
                header=header, field=field, static=static, key=key, update=update
            )

    def add_mapping_field_set(
        self, header="", field="", static=False, update=False, key=False
    ):
        frm_csv_mapping_fields = self.nametowidget("csv_mapping.csv_mapping_fields")

        # 3CX Field
        ent_csv_mapping_3cx_field = ttk.Entry(frm_csv_mapping_fields)
        ent_csv_mapping_3cx_field.insert(0, field)
        ent_csv_mapping_3cx_field.grid(
            row=len(self.mapping_fields) + 2, column=1, sticky="w"
        )

        # CSV Header Field
        ent_csv_mapping_header = ttk.Entry(frm_csv_mapping_fields)
        ent_csv_mapping_header.insert(0, header)
        ent_csv_mapping_header.grid(
            row=len(self.mapping_fields) + 2, column=2, sticky="w"
        )

        # Static Value Checkbox
        chk_csv_mapping_static_value = Checkbox(
            self.widgets.frm_csv_mapping_fields, value=static
        )
        chk_csv_mapping_static_value.grid(
            row=len(self.mapping_fields) + 2, column=3, sticky="w"
        )

        # Update Checkbox
        chk_csv_mapping_update = Checkbox(
            self.widgets.frm_csv_mapping_fields, value=update
        )
        chk_csv_mapping_update.grid(
            row=len(self.mapping_fields) + 2, column=4, sticky="w"
        )

        # Key Checkbox
        chk_csv_mapping_key = Checkbox(
            self.widgets.frm_csv_mapping_fields,
            state=self.ceckbox_key_state.get(),
            command=self.handle_checkbox_key_change,
            # value=key,
        )
        chk_csv_mapping_key.grid(row=len(self.mapping_fields) + 2, column=5, sticky="w")

        # Remove Button
        btn_csv_mapping_remove = ttk.Button(
            self.widgets.frm_csv_mapping_fields,
            text="-",
            command=lambda row_index=len(
                self.mapping_fields
            ): self.delete_mapping_field_set(row_index),
        )
        btn_csv_mapping_remove.grid(
            row=len(self.mapping_fields) + 2, column=6, sticky="w"
        )

        if key:
            chk_csv_mapping_key.invoke()
        self.mapping_fields.append(
            ExtensionMappingFieldSet(
                field=ent_csv_mapping_3cx_field,
                header=ent_csv_mapping_header,
                static=chk_csv_mapping_static_value,
                update=chk_csv_mapping_update,
                key=chk_csv_mapping_key,
                delete=btn_csv_mapping_remove,
            )
        )

    def delete_mapping_field_set(self, row_index=None):
        if row_index is None:
            row_index = len(self.mapping_fields)

        row = self.mapping_fields.pop(row_index)
        for widget in row:
            widget.destroy()

    def handle_checkbox_key_change(self):
        if self.ceckbox_key_state.get() == "normal":
            self.disable_key_checkboxes()
        else:
            self.enable_key_checkboxes()

    def disable_key_checkboxes(self):
        self.ceckbox_key_state.set("disable")
        for row in self.mapping_fields:
            if not row.key.checked:
                row.key.configure(state="disable")

    def enable_key_checkboxes(self):
        self.ceckbox_key_state.set("normal")
        for row in self.mapping_fields:
            row.key.configure(state="normal")


class WindowSync(PopupWindow):
    def __init__(self, master, sync_logger: SyncLogger, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.resizable(height=False, width=False)

        self.widgets = WidgetList()
        self.is_paused = False
        self.sync_running = True

        self.build_gui()
        sync_logger.addTextWindowHandler(self.widgets.txt_output)
        self.logger = sync_logger.get_logger()

        self.sync_thread = threading.Thread(target=self.master.run_sync_in_thread)
        self.sync_thread.start()
        self.periodic_update()

    def build_gui(self):
        # Frame: Window
        self.widgets.frm_window = ttk.Frame(self, width=500, height=1000)
        self.widgets.frm_window.pack(fill="both", anchor="nw", expand=True)

        # Text:  Output
        self.widgets.txt_output = ScrolledText(
            self.widgets.frm_window, relief="sunken", name="output"
        )
        self.widgets.txt_output.pack(fill="both", expand=True)

        # Form: Sync Buttons
        self.widgets.frm_sync_buttons = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_sync_buttons.pack(side="bottom")

        # Button: Pause/Resume
        self.widgets.btn_pause_resume = ttk.Button(
            self.widgets.frm_sync_buttons,
            text="Pause",
            command=self.handle_pause_resume,
        )
        self.widgets.btn_pause_resume.pack(side="left", anchor="s")

        # Form: Navigation Buttons
        self.widgets.frm_navigation = ttk.Frame(self)
        self.widgets.frm_navigation.pack(side="bottom", anchor="e", pady=5)

    def handle_pause_resume(self):
        if not self.sync_running:
            return
        self.is_paused = not self.is_paused
        # self.btn_pause_resume.configure(text="Resume" if self.is_paused else "Pause")
        if self.is_paused:
            self.logger.info(f"Paused by user")
            self.master.sync.pause_sync()
            self.widgets.btn_pause_resume.configure(text="Resume")
        else:
            self.logger.info(f"Resumed by user")
            self.master.sync.resume_sync()
            self.widgets.btn_pause_resume.configure(text="Pause")

    def periodic_update(self) -> None:
        if not self.sync_running:
            return
        self.update()
        self.after(100, self.periodic_update)
