import tcx_api
import tkinter as tk
from tcx_api.tcx_api_connection import TCX_API_Connection
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from app.widgets import Checkbox, ExtensionMappingFieldSet
from app.config import TCXConfig
from app.mapping import CSVMapping
from app.exceptions import ConfigSaveError


class Window3cxConfig(tk.Toplevel):

    def __init__(self, master, tcx_config: TCXConfig, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.widgets = {}
        self.tcx_config = tcx_config
        self.tcx_config.load()
        self.initialize_variables()
        self.build_gui()

    def initialize_variables(self) -> None:
        # Initialize Variables
        conf = self.tcx_config["3cx"]
        self.vars = {}
        for var in ["scheme", "domain", "port", "username", "password"]:
            self.vars[var] = tk.StringVar(self, conf.get(var, ""))
            # self.vars[var] = tk.StringVar(self, conf[var])
            # self.vars[var].set(conf.get(var, ""))

    def build_gui(self) -> None:
        self.grab_set()
        self.focus_force()

        # Create a window frame
        self.widgets["frm_window"] = tk.Frame(master=self)
        self.widgets["frm_window"].pack()

        # Create 3cx options frame
        self.widgets["frm_3cx_options"] = tk.Frame(
            master=self.widgets["frm_window"])
        self.widgets["frm_3cx_options"].config(width=300, height=200,
                                               relief="ridge", borderwidth=2)
        self.widgets["frm_3cx_options"].pack()

        # 3cx URL
        self.widgets["lbl_3cx_url"] = tk.Label(
            master=self.widgets["frm_3cx_options"], text="3CX URL:")
        self.widgets["lbl_3cx_url"].grid(
            row=0, column=0, padx=(5, 0), sticky="w")

        # Create a 3cx URL frame in that window
        self.widgets["frm_3cx_url"] = tk.Frame(
            master=self.widgets["frm_3cx_options"])
        self.widgets["frm_3cx_url"].grid_columnconfigure(2, weight=1)
        self.widgets["frm_3cx_url"].grid(row=0, column=1)

        self.widgets["opt_3cx_scheme"] = tk.OptionMenu(
            self.widgets["frm_3cx_url"], self.vars["scheme"], *
            ["https", "http"]
        )
        self.widgets["lbl_3cx_scheme_ending"] = tk.Label(
            master=self.widgets["frm_3cx_url"], text="://")
        self.widgets["ent_3cx_domain"] = tk.Entry(
            master=self.widgets["frm_3cx_url"], textvariable=self.vars["domain"])
        self.widgets["lbl_3cx_server_ending"] = tk.Label(
            master=self.widgets["frm_3cx_url"], text=":")
        self.widgets["ent_3cx_port"] = tk.Entry(
            master=self.widgets["frm_3cx_url"], textvariable=self.vars["port"], width=5
        )

        elements = [
            self.widgets["opt_3cx_scheme"],
            self.widgets["lbl_3cx_scheme_ending"],
            self.widgets["ent_3cx_domain"],
            self.widgets["lbl_3cx_server_ending"],
            self.widgets["ent_3cx_port"],
        ]

        for y, element in enumerate(elements):
            element.grid(row=1, column=y, sticky="we")

        self.widgets["lbl_3cx_username"] = tk.Label(
            master=self.widgets["frm_3cx_options"], text="Username:")
        self.widgets["ent_3cx_username"] = tk.Entry(
            master=self.widgets["frm_3cx_options"], textvariable=self.vars["username"]
        )

        self.widgets["lbl_3cx_password"] = tk.Label(
            master=self.widgets["frm_3cx_options"], text="Password:")
        self.widgets["ent_3cx_password"] = tk.Entry(
            master=self.widgets["frm_3cx_options"], textvariable=self.vars["password"], show="*"
        )
        self.widgets["lbl_3cx_username"].grid(row=2, column=0, padx=(5, 0))
        self.widgets["ent_3cx_username"].grid(row=2, column=1, sticky="we")
        self.widgets["lbl_3cx_password"].grid(row=3, column=0, padx=(5, 0))
        self.widgets["ent_3cx_password"].grid(row=3, column=1, sticky="we")

        # Test and OK Buttons
        self.widgets["frm_navigation"] = tk.Frame(
            master=self.widgets["frm_window"])
        self.widgets["frm_navigation"].pack(side="bottom", anchor="e")

        self.widgets["btn_test"] = tk.Button(
            master=self.widgets["frm_navigation"], name="btn_test", text="Test", command=self.handle_test_connection
        )
        self.widgets["btn_save"] = tk.Button(
            master=self.widgets["frm_navigation"], name="btn_save", text="Save", command=self.handle_save_click
        )
        self.widgets["btn_cancel"] = tk.Button(
            master=self.widgets["frm_navigation"], name="btn_cancel", text="Cancel", command=self.handle_cancel_click
        )

        self.widgets["btn_test"].grid(row=0, column=0, padx=5)
        self.widgets["btn_save"].grid(row=0, column=1, padx=5)
        self.widgets["btn_cancel"].grid(row=0, column=2, padx=5)

    def handle_test_connection(self):
        api = TCX_API_Connection(server_url=self.tcx_config.server_url)

        try:
            api.authenticate(
                username=self.vars["username"].get(),
                password=self.vars["password"].get(),
            )
            messagebox.showinfo(title="Success", message="Test Successful")
        except Exception as e:
            messagebox.showinfo(
                title="Failure", message=f"Test Failed. {str(e)}")

    def handle_save_click(self):
        try:
            self.write_config_file()
            messagebox.showinfo(title="Saved!", message="Config saved!")
            self.destroy()
        except ConfigSaveError as e:
            messagebox.showerror(
                title="Error!", message=f"{e}")

    def handle_cancel_click(self):
        self.destroy()

    def write_config_file(self):
        try:
            for var in ["scheme", "domain", "port", "username", "password"]:
                self.tcx_config["3cx"][var] = self.vars[var].get()
            self.tcx_config.save()
        except Exception as e:
            raise ConfigSaveError() from e


class WindowCSVMapping(tk.Toplevel):
    ""

    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.grab_set()
        self.focus_force()

        self.mapping = CSVMapping()
        self.mapping.load_mapping_config()
        self.mapping_fields = []
        self.ceckbox_key_state = tk.StringVar(self, "normal")
        self.var_csv_mapping_extension_path = tk.StringVar(self)
        self.key_checked = False

        extension = self.mapping.get("Extension", {})
        self.var_csv_mapping_extension_path.set(extension.get("Path", ""))

        header_y_padding = (5, 15)
        paragraph_x_padding = (15, 0)
        frame_iy_padding = 5

        # Frame: window
        frm_window = tk.Frame(master=self, name="window")
        frm_window.pack(fill="both", expand=True)

        # Frame: Mapping
        frm_csv_mapping = tk.Frame(master=frm_window)
        frm_csv_mapping.config(relief="ridge", borderwidth=2)
        frm_csv_mapping.pack(side="top", fill="both",
                             ipady=frame_iy_padding, expand=True)

        # Extension Header
        lbl_extension_header = tk.Label(
            master=frm_csv_mapping, text="Extension Mapping", font=("Arial", 15)
        )
        lbl_extension_header.grid(
            row=0, column=1, pady=header_y_padding, sticky="w", columnspan=3
        )

        # Field: Extension Path
        lbl_extension_path = tk.Label(master=frm_csv_mapping, text="Path:")
        lbl_extension_path.grid(
            row=2, column=1, padx=paragraph_x_padding, sticky="w")

        ent_extension_path = tk.Entry(
            master=frm_csv_mapping,
            textvariable=self.var_csv_mapping_extension_path,
        )
        ent_extension_path.grid(row=2, column=2, sticky="w")
        btn_extension_path_browse = tk.Button(
            master=frm_csv_mapping, text=">", font=40, command=self.browse_file_csv
        )
        btn_extension_path_browse.grid(row=2, column=3, sticky="w")

        # Frame: CSV Mapping Fields
        frm_csv_mapping_fields = tk.Frame(
            master=frm_window, name="csv_mapping_fields")
        frm_csv_mapping_fields.config(
            relief="sunken", borderwidth=2
        )
        frm_csv_mapping_fields.pack(
            side="top", fill="both", ipady=frame_iy_padding, expand=True)

        # CSV Mapping Headers
        # Header: 3cx Field
        lbl_csv_mapping_3cx_field = tk.Label(
            master=frm_csv_mapping_fields, text="3cx Field", width=20
        )
        lbl_csv_mapping_3cx_field.grid(row=1, column=1, sticky="w")

        # Header: CSV Header
        lbl_csv_mapping_header = tk.Label(
            master=frm_csv_mapping_fields, text="CSV Header", width=20
        )
        lbl_csv_mapping_header.grid(row=1, column=2, sticky="w")

        # Header: Update
        lbl_csv_mapping_update = tk.Label(
            master=frm_csv_mapping_fields, text="Update", width=5)
        lbl_csv_mapping_update.grid(row=1, column=3, sticky="w")

        # Header: Key
        lbl_csv_mapping_key = tk.Label(
            master=frm_csv_mapping_fields, text="Key", width=5)
        lbl_csv_mapping_key.grid(row=1, column=4, sticky="w")

        # self.add_mapping_field_set()
        self.initialize_mapping_field_sets()

        # Frame: Add Remove Fields
        frm_add_delete_fields = tk.Frame(master=frm_window)
        frm_add_delete_fields.pack(
            side="top", anchor="center", expand=True, fill="both")

        # Button: Add +
        btn_add_field = tk.Button(
            master=frm_add_delete_fields, text="+", command=self.add_mapping_field_set
        )
        btn_add_field.grid(row=1, column=1)

        # Button: Delete -
        btn_delete_field = tk.Button(
            master=frm_add_delete_fields,
            text="-",
            command=self.delete_mapping_field_set,
        )
        btn_delete_field.grid(row=1, column=2)

        # Frame: Navigation
        frm_navigation = tk.Frame(master=frm_window)
        frm_navigation.pack(side="bottom", anchor="e", expand=True)

        btn_save = tk.Button(
            master=frm_navigation, text="Save", command=self.handle_save_click
        )
        btn_cancel = tk.Button(
            master=frm_navigation, text="Cancel", command=self.handle_cancel_click
        )

        btn_save.grid(row=1, column=1, padx=5)
        btn_cancel.grid(row=1, column=2, padx=5)

    def handle_save_click(self):
        self.mapping["Extension"] = {
            "Path": self.var_csv_mapping_extension_path.get(),
        }
        mapping_new = {}
        # mapping_update = {}
        mapping_update = []
        for mapping_row in self.mapping_fields:
            if mapping_row.key.checked:
                key = mapping_row.header.get()
            mapping_new[mapping_row.field.get()] = mapping_row.header.get()
            if mapping_row.update.checked:
                # mapping_update[mapping_row.field.get()] = mapping_row.header.get()
                mapping_update.append(mapping_row.header.get())
        self.mapping["Extension"]["Key"] = key
        self.mapping["Extension"]["New"] = mapping_new
        self.mapping["Extension"]["Update"] = mapping_update
        self.mapping.save_mapping_config()
        messagebox.showinfo(title="Saved!", message="Config saved!")
        self.destroy()

    def handle_cancel_click(self):
        self.destroy()

    def browse_file_csv(self):
        filename = askopenfilename(filetypes=(
            ("CSV", "*.csv"), ("All files", "*.*")))
        self.var_csv_mapping_extension_path.set(filename)

    def initialize_mapping_field_sets(self):
        for field, header in self.mapping.get("Extension", {}).get("New", {}).items():
            key = False
            update = False
            if header == self.mapping.get("Extension", {}).get("Key", None):
                key = True
            if header in self.mapping.get("Extension", {}).get("Update", {}):
                update = True

            self.add_mapping_field_set(
                header=header, field=field, key=key, update=update
            )

    def add_mapping_field_set(self, header="", field="", update=False, key=False):
        frm_csv_mapping_fields = self.nametowidget("window.csv_mapping_fields")

        # CSV Header Field
        ent_csv_mapping_header = tk.Entry(master=frm_csv_mapping_fields)
        ent_csv_mapping_header.insert(0, header)
        ent_csv_mapping_header.grid(
            row=len(self.mapping_fields) + 2, column=1, sticky="w"
        )

        # 3CX Field
        ent_csv_mapping_3cx_field = tk.Entry(master=frm_csv_mapping_fields)
        ent_csv_mapping_3cx_field.insert(0, field)
        ent_csv_mapping_3cx_field.grid(
            row=len(self.mapping_fields) + 2, column=2, sticky="w"
        )

        # Update Checkbox
        chk_csv_mapping_update = Checkbox(
            master=frm_csv_mapping_fields, value=update)
        chk_csv_mapping_update.grid(
            row=len(self.mapping_fields) + 2, column=3, sticky="w"
        )

        # Key Checkbox
        chk_csv_mapping_key = Checkbox(
            master=frm_csv_mapping_fields,
            state=self.ceckbox_key_state.get(),
            command=self.handle_checkbox_key_change,
            # value=key,
        )
        chk_csv_mapping_key.grid(
            row=len(self.mapping_fields) + 2, column=4, sticky="w")

        # Remove Button
        btn_csv_mapping_remove = tk.Button(
            master=frm_csv_mapping_fields, text="-", command=lambda row_index=len(self.mapping_fields): self.delete_mapping_field_set(row_index)
        )
        btn_csv_mapping_remove.grid(
            row=len(self.mapping_fields) + 2, column=5, sticky="w")

        if key:
            chk_csv_mapping_key.invoke()
        self.mapping_fields.append(
            ExtensionMappingFieldSet(
                header=ent_csv_mapping_header,
                field=ent_csv_mapping_3cx_field,
                update=chk_csv_mapping_update,
                key=chk_csv_mapping_key,
                delete=btn_csv_mapping_remove
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

    def handle_key_unchecked(self):
        # self.key_checked = False
        pass
        # Extensions
        # Path
        # Key
        # New Field Mapping
        # Update Field Mapping

        # Group Memberships
        # Path
        # Groups
        # Group
        # Conditions
