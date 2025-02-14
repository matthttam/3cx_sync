from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
import sv_ttk
from threecxapi.connection import ThreeCXApiConnection
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from app.widgets import Checkbox, ExtensionMappingFieldSet, WidgetList
from app.config import AppConfig
from sync.strategy.csv.mapping import CSVMapping
from tkinter.scrolledtext import ScrolledText


# Pack Defaults
@dataclass(frozen=True)
class PackButtonDefaults:
    padx: int = 5
    pady: int = 5


@dataclass(frozen=True)
class PackFrameDefaults:
    padx: int = 5
    pady: int = 5
    side: str = tk.LEFT
    fill: str = tk.BOTH


@dataclass(frozen=True)
class PackLabelDefaults:
    padx: tuple = (0, 10)
    fill: str = tk.X


@dataclass(frozen=True)
class PackEntryDefaults:
    pady: int = 5
    fill: str = tk.X


@dataclass(frozen=True)
class LabelFormDefaults:
    padx: int = 20
    pady: int = 10
    fill: str = tk.BOTH
    expand: bool = True


@dataclass(frozen=True)
class PackDefaults:
    btn: PackButtonDefaults = PackButtonDefaults()
    frm: PackFrameDefaults = PackFrameDefaults()
    lbl: PackLabelDefaults = PackLabelDefaults()
    ent: PackEntryDefaults = PackEntryDefaults()
    lblfrm: LabelFormDefaults = LabelFormDefaults()


# Grid Defaults
@dataclass(frozen=True)
class GridButtonDefaults:
    padx: int = 5
    pady: int = 5
    sticky: str = tk.EW


@dataclass(frozen=True)
class GridFrameDefaults:
    padx: int = 5
    pady: int = 5
    side: str = tk.LEFT


@dataclass(frozen=True)
class GridLabelDefaults:
    padx: tuple = (5, 10)
    sticky: str = tk.E


@dataclass(frozen=True)
class GridEntryDefaults:
    padx: tuple = (0, 5)
    pady: int = 5
    sticky: str = tk.EW


@dataclass(frozen=True)
class GridLabelFormDefaults:
    padx: int = 20
    pady: int = 10
    expand: bool = True


@dataclass(frozen=True)
class GridCheckboxDefaults:
    padx: int = 5
    pady: int = 5


@dataclass(frozen=True)
class GridDefaults:
    btn: GridButtonDefaults = GridButtonDefaults()
    frm: GridFrameDefaults = GridFrameDefaults()
    lbl: GridLabelDefaults = GridLabelDefaults()
    ent: GridEntryDefaults = GridEntryDefaults()
    lblfrm: GridLabelFormDefaults = GridLabelFormDefaults()
    chk: GridCheckboxDefaults = GridCheckboxDefaults()


@dataclass(frozen=True)
class Defaults:
    pack: PackDefaults = PackDefaults()
    grid: GridDefaults = GridDefaults()


class Window:
    defaults: Defaults = Defaults()
    _current_row = 0
    _current_column = 0

    def reset_row_and_column(self) -> None:
        self.reset_row()
        self.reset_column()

    def increment_row(self, reset_column=True) -> None:
        self._current_row = self._current_row + 1
        if reset_column:
            self.reset_column()

    def reset_row(self) -> None:
        self._current_row = 0

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

    def get_current_column(self) -> int:
        return self._current_column

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
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)
        self.resizable(height=False, width=False)
        self.widgets = WidgetList()
        self.app_config = app_config
        self.initialize_variables()
        self.build_gui()

    def initialize_variables(self) -> None:
        self.vars = {"3cx": {}, "app": {}}

        # Helper to add trace to the tk variables
        def trace_tk_variables(tk_var: tk.Variable, section, var):
            tk_var.trace_add(
                "write",
                lambda *args: self.app_config.set_value(section, var, str(tk_var.get())),
            )

        # Create StringVars for '3cx' section
        section = "3cx"
        for var in ["scheme", "domain", "port", "username", "password"]:
            self.vars[section][var] = tk.StringVar(self, self.app_config.get(section, var))
            trace_tk_variables(self.vars[section][var], section, var)

        # Create BooleanVars for '3cx' section
        for var in ["store_credential_securely"]:
            self.vars[section][var] = tk.BooleanVar(self, self.app_config.getboolean(section, var))
            trace_tk_variables(self.vars[section][var], section, var)

        # Create BooleanVars for 'app' section
        section = "app"
        for var in ["logout_hotdesk_on_disable"]:
            self.vars[section][var] = tk.BooleanVar(self, self.app_config.getboolean(section, var))
            trace_tk_variables(self.vars[section][var], section, var)

    def build_gui(self) -> None:
        # Create a window frame
        self.widgets.frm_window = ttk.Frame(self)
        self.widgets.frm_window.pack(fill="both", expand=True)

        self.widgets.frm_3cx_options = ttk.LabelFrame(self.widgets.frm_window, text="3CX Settings")
        # self.widgets.frm_3cx_options.grid_columnconfigure(1, weight=1)
        # self.widgets.frm_3cx_options.grid_columnconfigure(2, weight=1)
        self.widgets.frm_3cx_options.grid_columnconfigure(1, weight=0)  # Scheme dropdown fixed width
        self.widgets.frm_3cx_options.grid_columnconfigure(2, weight=0)  # '://' label fixed
        self.widgets.frm_3cx_options.grid_columnconfigure(3, weight=1)  # Expandable domain entry
        self.widgets.frm_3cx_options.grid_columnconfigure(4, weight=0)  # ':' label fixed
        self.widgets.frm_3cx_options.grid_columnconfigure(5, weight=0)  # Port entry fixed

        self.widgets.frm_3cx_options.pack(
            padx=self.defaults.pack.lblfrm.padx,
            pady=self.defaults.pack.lblfrm.pady,
            fill=self.defaults.pack.lblfrm.fill,
            expand=self.defaults.pack.lblfrm.expand,
            side=tk.TOP,
        )

        # Create the 3cx URL
        self.widgets.lbl_3cx_url = ttk.Label(self.widgets.frm_3cx_options, text="3CX URL:")
        self.widgets.lbl_3cx_url.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.lbl.padx,
            sticky=self.defaults.grid.lbl.sticky,
        )

        # Create the 3CX URL widgets
        self.widgets.opt_3cx_scheme = ttk.OptionMenu(
            self.widgets.frm_3cx_options,
            self.vars["3cx"]["scheme"],
            self.vars["3cx"]["scheme"].get(),
            *["https", "http"],
        )
        self.widgets.opt_3cx_scheme.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            pady=self.defaults.grid.ent.pady,
            sticky=self.defaults.grid.ent.sticky,
        )

        self.widgets.lbl_3cx_scheme_ending = ttk.Label(self.widgets.frm_3cx_options, text="://")
        self.widgets.lbl_3cx_scheme_ending.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=2,
        )

        self.widgets.ent_3cx_domain = ttk.Entry(
            self.widgets.frm_3cx_options,
            textvariable=self.vars["3cx"]["domain"],
        )
        self.widgets.ent_3cx_domain.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            pady=self.defaults.grid.ent.pady,
            sticky=self.defaults.grid.ent.sticky,
        )

        self.widgets.lbl_3cx_server_ending = ttk.Label(self.widgets.frm_3cx_options, text=":")
        self.widgets.lbl_3cx_server_ending.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=2,
        )

        self.widgets.ent_3cx_port = ttk.Entry(
            self.widgets.frm_3cx_options,
            textvariable=self.vars["3cx"]["port"],
            width=5,
        )
        self.widgets.ent_3cx_port.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.ent.padx,
            pady=self.defaults.grid.ent.pady,
            sticky=self.defaults.grid.ent.sticky,
        )

        # Create the 3CX username widgets
        self.widgets.lbl_3cx_username = ttk.Label(
            self.widgets.frm_3cx_options,
            text="Username:",
        )
        self.increment_row()
        self.widgets.lbl_3cx_username.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.lbl.padx,
            sticky=self.defaults.grid.lbl.sticky,
        )
        self.widgets.ent_3cx_username = ttk.Entry(
            self.widgets.frm_3cx_options,
            textvariable=self.vars["3cx"]["username"],
        )
        self.widgets.ent_3cx_username.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            pady=self.defaults.grid.ent.pady,
            padx=self.defaults.grid.ent.padx,
            sticky=self.defaults.grid.ent.sticky,
            columnspan=5,
        )

        # Create the 3CX password widgets
        self.increment_row()
        self.widgets.lbl_3cx_password = ttk.Label(self.widgets.frm_3cx_options, text="Password:")
        self.widgets.lbl_3cx_password.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.lbl.padx,
            sticky=self.defaults.grid.lbl.sticky,
        )

        self.widgets.ent_3cx_password = ttk.Entry(
            self.widgets.frm_3cx_options,
            textvariable=self.vars["3cx"]["password"],
            show="*",
        )
        self.widgets.ent_3cx_password.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            pady=self.defaults.grid.ent.pady,
            padx=self.defaults.grid.ent.padx,
            sticky=self.defaults.grid.ent.sticky,
            columnspan=5,
        )

        # Create the Store credential securely widgets
        self.widgets.lbl_store_credential_securely = ttk.Label(
            self.widgets.frm_3cx_options,
            text="Store Credential Securely:",
        )
        self.increment_row()
        self.widgets.lbl_store_credential_securely.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.lbl.padx,
            sticky=self.defaults.grid.lbl.sticky,
        )

        self.widgets.chk_store_credential_securely = ttk.Checkbutton(
            self.widgets.frm_3cx_options,
            variable=self.vars["3cx"]["store_credential_securely"],
        )
        self.widgets.chk_store_credential_securely.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            sticky=tk.W,
            padx=self.defaults.grid.chk.padx,
            pady=self.defaults.grid.chk.pady,
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
            padx=5,
            pady=5,
            sticky=tk.EW,
            columnspan=5,
        )

        # Create the App Settings header
        self.widgets.lblfrm_app_settings = ttk.LabelFrame(self.widgets.frm_window, text="App Settings")
        self.widgets.lblfrm_app_settings.pack(
            padx=self.defaults.pack.lblfrm.padx,
            pady=self.defaults.pack.lblfrm.pady,
            fill=self.defaults.pack.lblfrm.fill,
            expand=self.defaults.pack.lblfrm.expand,
        )

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
            padx=self.defaults.grid.lbl.padx,
            sticky=self.defaults.grid.lbl.sticky,
        )
        self.widgets.chk_app_logout_hotdesk_on_disable.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            sticky="w",
            padx=self.defaults.grid.chk.padx,
            pady=self.defaults.grid.chk.pady,
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
            padx=self.defaults.grid.btn.padx,
            pady=self.defaults.grid.btn.pady,
            sticky=self.defaults.grid.btn.sticky,
        )
        self.widgets.btn_save.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.btn.padx,
            pady=self.defaults.grid.btn.pady,
            sticky=tk.SE,
        )
        self.widgets.btn_cancel.grid(
            row=self.get_current_row(),
            column=self.get_next_column(),
            padx=self.defaults.grid.btn.padx,
            pady=self.defaults.grid.btn.pady,
            sticky=tk.SE,
        )

    def handle_test_connection(self):
        api = ThreeCXApiConnection(server_url=self.app_config.server_url)

        try:
            api.authenticate(
                username=self.app_config["3cx"]["username"],
                password=self.app_config["3cx"]["password"],
            )
            messagebox.showinfo(title="Success", message="Test Successful", parent=self)
        except Exception as e:
            messagebox.showinfo(title="Failure", message=f"Test Failed. {e}", parent=self)

    def handle_apply_click(self):
        self.save_config()

    def handle_save_click(self):
        self.save_config()
        self.destroy()

    def handle_cancel_click(self):
        self.on_destroy()

    def on_destroy(self):
        if self.app_config.is_dirty:
            if not self.confirm_discard_changes():
                return
        self.app_config.load()
        self.destroy()

    def confirm_discard_changes(self) -> bool:
        return messagebox.askyesno(
            "Unsaved Changes",
            "Discard unsaved changes?",
            parent=self
        )

    def save_config(self):
        try:
            self.app_config.save()
            messagebox.showinfo(title="Saved!", message="Config saved!", parent=self)
        except Exception as e:
            messagebox.showerror(title="Error!", message=f"{e}", parent=self)


class WindowCSVMapping(PopupWindow):

    def __init__(self, master, *args, csv_mapping: CSVMapping, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)
        self.geometry("600x920")
        self.widgets = WidgetList()
        self.mapping = csv_mapping
        self.title("CSV Mapping Settings")
        self.initialize_variables()
        self.build_gui()

    def initialize_variables(self) -> None:
        self.mapping_fields = []
        self.checkbox_key_state = tk.StringVar(self, "normal")
        extension = self.mapping.get("Extension", {})
        self.var_csv_mapping_import_file_path = tk.StringVar(self, value=extension.get("Path", ""))
        self.key_checked = False

    def build_gui(self) -> None:
        # Frame: window
        self.widgets.frm_window = ttk.Frame(self, name="csv_mapping")
        self.widgets.frm_window.grid_rowconfigure(0, weight=1)
        self.widgets.frm_window.grid_columnconfigure(0, weight=1)
        self.widgets.frm_window.pack(
            padx=self.defaults.pack.frm.padx,
            pady=self.defaults.pack.frm.pady,
            side=self.defaults.pack.frm.side,
            fill=self.defaults.pack.frm.fill,
            expand=True,
        )

        # Field: Extension Path
        self.widgets.lblfrm_import_file_path = ttk.LabelFrame(self.widgets.frm_window, text="Extension CSV File Path")
        self.widgets.lblfrm_import_file_path.pack(
            padx=self.defaults.pack.lblfrm.padx,
            pady=self.defaults.pack.lblfrm.pady,
            fill=self.defaults.pack.lblfrm.fill,
            expand=False,
        )

        self.widgets.ent_import_file_path = ttk.Entry(
            self.widgets.lblfrm_import_file_path,
            textvariable=self.var_csv_mapping_import_file_path,
        )
        self.widgets.ent_import_file_path.pack(
            pady=self.defaults.pack.ent.pady, fill=self.defaults.pack.ent.fill, padx=(25, 1), side=tk.LEFT, expand=True
        )

        self.widgets.btn_import_file_path_browse = ttk.Button(
            self.widgets.lblfrm_import_file_path, text=">", command=self.browse_file_csv, width=2
        )
        self.widgets.btn_import_file_path_browse.pack(padx=(1, 25), pady=5, side=tk.LEFT)

        # Frame: CSV Mapping Fields
        self.widgets.lblfrm_csv_mapping_fields = ttk.LabelFrame(
            self.widgets.frm_window,
            text="Extension CSV Mapping",
            relief="sunken",
            borderwidth=2,
        )

        self.widgets.lblfrm_csv_mapping_fields.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Adding scrollbar to CSV Mapping Fields
        self.widgets.canvas_csv_mapping_fields_scroll_bar = tk.Canvas(self.widgets.lblfrm_csv_mapping_fields)
        self.widgets.scrollbar_csv_mapping_fields = ttk.Scrollbar(
            self.widgets.lblfrm_csv_mapping_fields,
            orient="vertical",
            command=self.widgets.canvas_csv_mapping_fields_scroll_bar.yview,
        )
        self.widgets.scrollbar_csv_mapping_fields.pack(side="right", fill="y")
        self.widgets.frm_csv_mapping_fields_scrollable = ttk.Frame(self.widgets.canvas_csv_mapping_fields_scroll_bar)
        self.widgets.frm_csv_mapping_fields_scrollable.bind("<Configure>", lambda e: self.update_scrollbar())
        self.widgets.frm_csv_mapping_fields_scrollable.grid_columnconfigure(0, weight=1)
        self.widgets.frm_csv_mapping_fields_scrollable.grid_columnconfigure(1, weight=1)

        self.widgets.canvas_csv_mapping_fields_scroll_bar.bind(
            "<Configure>",
            lambda e: (
                self.widgets.canvas_csv_mapping_fields_scroll_bar.itemconfig(
                    self.widgets.canvas_csv_mapping_fields_scroll_bar.find_withtag("inner_frame"), width=e.width
                ),
            ),
        )

        self.widgets.canvas_csv_mapping_fields_scroll_bar.create_window(
            (0, 0), window=self.widgets.frm_csv_mapping_fields_scrollable, anchor="nw", tags="inner_frame"
        )
        self.widgets.canvas_csv_mapping_fields_scroll_bar.configure(
            yscrollcommand=self.widgets.scrollbar_csv_mapping_fields.set
        )

        self.widgets.canvas_csv_mapping_fields_scroll_bar.pack(side="left", fill="both", expand=True)

        # CSV Mapping Headers
        self.widgets.lbl_csv_mapping_3cx_field = ttk.Label(
            self.widgets.frm_csv_mapping_fields_scrollable, text="3cx Field"
        )
        self.widgets.lbl_csv_mapping_3cx_field.grid(row=0, column=0, sticky="s")

        self.widgets.lbl_csv_mapping_header = ttk.Label(
            self.widgets.frm_csv_mapping_fields_scrollable, text="CSV Header"
        )
        self.widgets.lbl_csv_mapping_header.grid(row=0, column=1, sticky="s")

        self.widgets.lbl_csv_mapping_static = tk.Canvas(
            self.widgets.frm_csv_mapping_fields_scrollable, width=20, height=50
        )

        text_color = "Black"
        if sv_ttk.get_theme() == "dark":
            text_color = "White"
        self.widgets.lbl_csv_mapping_static.create_text(10, 33, text="Static", angle=90, fill=text_color)
        self.widgets.lbl_csv_mapping_static.grid(row=0, column=2, sticky="s")

        self.widgets.lbl_csv_mapping_update = tk.Canvas(
            self.widgets.frm_csv_mapping_fields_scrollable, width=20, height=50
        )
        self.widgets.lbl_csv_mapping_update.create_text(10, 29, text="Update", angle=90, fill=text_color)
        self.widgets.lbl_csv_mapping_update.grid(row=0, column=3, sticky="s")

        self.widgets.lbl_csv_mapping_key = tk.Canvas(
            self.widgets.frm_csv_mapping_fields_scrollable, width=20, height=50
        )
        self.widgets.lbl_csv_mapping_key.create_text(10, 40, text="Key", angle=90, fill=text_color)
        self.widgets.lbl_csv_mapping_key.grid(row=0, column=4, sticky="s")

        self.initialize_mapping_field_sets(starting_row=1)

        # Frame: Add Remove Fields
        self.widgets.frm_add_delete_fields = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_add_delete_fields.pack(side="top", anchor="n", fill="x", padx=25, pady=5)

        self.widgets.btn_add_field = ttk.Button(
            self.widgets.frm_add_delete_fields,
            text="+",
            width=2,
            command=self.handle_button_add_mapping_field_set,
        )
        self.widgets.btn_add_field.grid(row=0, column=0, padx=2, pady=2, sticky="se")

        self.widgets.btn_delete_field = ttk.Button(
            self.widgets.frm_add_delete_fields,
            text="−",
            width=2,
            command=self.handle_button_delete_mapping_field_set,
        )
        self.widgets.btn_delete_field.grid(row=0, column=1, padx=2, pady=2, sticky="se")

        # Frame: Navigation
        self.widgets.frm_navigation = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_navigation.pack(side="bottom", anchor="e", pady=10)

        self.widgets.btn_save = ttk.Button(
            self.widgets.frm_navigation,
            text="Save",
            command=self.handle_save_click,
        )
        self.widgets.btn_save.grid(row=0, column=0, padx=5)

        self.widgets.btn_cancel = ttk.Button(
            self.widgets.frm_navigation,
            text="Cancel",
            command=self.handle_cancel_click,
        )
        self.widgets.btn_cancel.grid(row=0, column=1, padx=5)

    def handle_save_click(self):
        self.set_mapping_values()
        self.mapping.save()
        messagebox.showinfo(title="Saved!", message="Config saved!", parent=self)
        self.destroy()

    def set_mapping_values(self):
        # This needs to be replaced with the trace method like in the app config.
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
        self.on_destroy()

    def on_destroy(self):
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
            parent=self
        )

    def browse_file_csv(self):
        filename = askopenfilename(filetypes=(("CSV", "*.csv"), ("All files", "*.*")))
        self.var_csv_mapping_import_file_path.set(filename)

    def initialize_mapping_field_sets(self, starting_row: int):
        parsed_config = self.mapping.get_parsed_config()
        row = starting_row
        for field_info in parsed_config:
            self.add_mapping_field_set(row=row, **field_info)
            row += 1

    def handle_button_add_mapping_field_set(self):
        self.add_mapping_field_set(row=len(self.mapping_fields) + 1)
        self.update_scrollbar()

    def update_scrollbar(self):
        canvas = self.widgets.canvas_csv_mapping_fields_scroll_bar
        canvas.configure(scrollregion=canvas.bbox("all"))

    def add_mapping_field_set(self, row: int, header="", field="", static=False, update=False, key=False, **kwargs):
        parent = self.widgets.frm_csv_mapping_fields_scrollable
        # 3cx Field
        ent_csv_mapping_3cx_field = ttk.Entry(parent)
        ent_csv_mapping_3cx_field.insert(0, field)
        ent_csv_mapping_3cx_field.grid(row=row, column=0, sticky=tk.NSEW)

        # CSV Header Field
        ent_csv_mapping_header = ttk.Entry(parent)
        ent_csv_mapping_header.insert(0, header)
        ent_csv_mapping_header.grid(row=row, column=1, sticky=tk.NSEW)

        # Static Value Checkbox
        chk_csv_mapping_static_value = Checkbox(parent, value=static)
        chk_csv_mapping_static_value.grid(row=row, column=2)

        # Update Checkbox
        chk_csv_mapping_update = Checkbox(parent, value=update)
        chk_csv_mapping_update.grid(row=row, column=3)

        # Key Checkbox
        chk_csv_mapping_key = Checkbox(
            parent,
            state=self.checkbox_key_state.get(),
            command=self.handle_checkbox_key_change,
        )
        chk_csv_mapping_key.grid(row=row, column=4)

        # Remove Button
        btn_csv_mapping_remove = ttk.Button(parent, text="−", width=1)
        btn_csv_mapping_remove.config(
            command=lambda btn=btn_csv_mapping_remove: self.handle_button_delete_specific_mapping_field_set(btn)
        )
        btn_csv_mapping_remove.grid(row=row, column=5, padx=2, pady=2)

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

    def handle_button_delete_mapping_field_set(self):
        # Delete the last mapping field set
        self.delete_mapping_field_set_by_row_index(len(self.mapping_fields) - 1)
        self.update_scrollbar()

    def handle_button_delete_specific_mapping_field_set(self, button):
        for index, mapping_field in enumerate(self.mapping_fields):
            if mapping_field.delete is button:
                self.delete_mapping_field_set_by_row_index(index)
                break

    def delete_mapping_field_set_by_row_index(self, row_index: int):
        row = self.mapping_fields.pop(row_index)
        # If this row has key checked, enable keys
        if row.key.checked:
            self.enable_key_checkboxes()
        # for widget in row:
        row.destroy()
        # Reindex the rows
        self.shift_rows_up(starting_row=row_index)

    def shift_rows_up(self, starting_row):
        partial_mapping_fields = self.mapping_fields[starting_row : len(self.mapping_fields)]
        for idx, x in enumerate(partial_mapping_fields, start=starting_row):
            x.change_row(row=idx + 1)

    def handle_checkbox_key_change(self):
        if self.checkbox_key_state.get() == "normal":
            self.disable_key_checkboxes()
        else:
            self.enable_key_checkboxes()

    def disable_key_checkboxes(self):
        """Disable any key checkboxes that are not checked"""
        self.checkbox_key_state.set("disable")
        for row in self.mapping_fields:
            if not row.key.checked:
                row.key.configure(state="disable")

    def enable_key_checkboxes(self):
        """Enable all key checkboxes"""
        self.checkbox_key_state.set("normal")
        for row in self.mapping_fields:
            row.key.configure(state="normal")


class WindowSync(PopupWindow):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Set up a protocol to handle the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_destroy)
        self.geometry("1000x800")
        self.resizable(height=False, width=False)
        self.widgets = WidgetList()
        self.build_gui()

        self.master.logger.add_text_window_handler(self.widgets.txt_output)

    def build_gui(self):
        # Frame: Window
        self.widgets.frm_window = ttk.Frame(self)
        self.widgets.frm_window.pack(fill="both", anchor="nw", expand=True)

        # Text:  Output
        self.widgets.txt_output = ScrolledText(self.widgets.frm_window, relief="sunken", name="output")
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
        if not self.master.sync:
            return
        self.master.toggle_sync_state()
        self.update_btn_pause_resume_text()

    def update_btn_pause_resume_text(self):
        self.widgets.btn_pause_resume.configure(text="Pause" if not self.master.sync.is_paused else "Resume")

    def periodic_update(self) -> None:
        if not self.master.sync or self.master.sync.is_terminated:
            return
        self.update()
        self.after(100, self.periodic_update)

    def wait_for_sync_thread(self) -> None:
        # This will block the main thread until the sync thread is finished
        if self.master.sync_thread.is_alive():
            self.master.sync_thread.join()

    def on_destroy(self):
        self.master.terminate_sync()
        self.master.logger.remove_text_window_handler(self.widgets.txt_output)
        self.wait_for_sync_thread()
        self.destroy()
