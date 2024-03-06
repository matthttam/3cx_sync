import os
import tkinter as tk
from tkinter import messagebox
from configparser import ConfigParser
from app.Api import Api


class App(tk.Tk):

    @property
    def is_dirty(self):
        pass

    @property
    def defaults_config_file_path(self):
        return os.path.join(os.getcwd(), "conf", "defaults.ini")

    @property
    def config_file_path(self):
        return os.path.join(os.getcwd(), "conf", "conf.ini")

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Paths for config files
        self.config_file = self.get_config_file()

        # Initialize Variables
        self.var_3cx_scheme = tk.StringVar(self)
        self.var_3cx_domain = tk.StringVar(self)
        self.var_3cx_port = tk.StringVar(self)
        self.var_3cx_username = tk.StringVar(self)
        self.var_3cx_password = tk.StringVar(self)

        # Set variable values
        self.set_vars_from_config()

        # Window Options
        self.wm_title("3cx Sync Config")
        self.config(height=500, width=500)

        # Create a window frame
        frm_window = tk.Frame(master=self)
        frm_window.pack()

        # Left Frame
        frm_left_column = tk.Frame(master=frm_window)
        frm_left_column.pack(side="left")
        btn_show_window_3cx_config2 = tk.Button(
            master=frm_left_column,
            text="Configure 3cx",
            command=self.show_Window3cxConfig,
        )
        btn_show_window_3cx_config2.pack(anchor="e")

        # Right Frame
        frm_right_column = tk.Frame(master=frm_window)
        frm_right_column.pack(side="left")

        btn_show_window_3cx_config = tk.Button(
            master=frm_right_column,
            text="Configure 3cx",
            command=self.show_Window3cxConfig,
        )
        btn_show_window_3cx_config.pack()

        # Save and Exit Buttons
        frm_save_and_exit = tk.Frame(master=self)
        frm_save_and_exit.pack(side="bottom", anchor="e", pady=5)

        btn_save = tk.Button(
            master=frm_save_and_exit, text="Save", command=self.handle_save_click
        )
        btn_exit = tk.Button(
            master=frm_save_and_exit, text="Exit", command=self.handle_exit_click
        )
        btn_save.grid(row=0, column=0, padx=5)
        btn_exit.grid(row=0, column=1, padx=5)

    def show_Window3cxConfig(self):
        Window3cxConfig(master=self)

    def handle_save_click(self):
        self.write_config_file()
        messagebox.showinfo(title="Saved!", message="Config saved!")

    def handle_exit_click(self):
        self.destroy()

    def get_config_file(self):
        config_file = ConfigParser()
        config_file.read([self.defaults_config_file_path, self.config_file_path])
        return config_file

    def set_vars_from_config(self):
        if not self.config_file:
            return
        self.var_3cx_scheme.set(self.config_file["3cx"]["scheme"])
        self.var_3cx_domain.set(self.config_file["3cx"]["domain"])
        self.var_3cx_port.set(self.config_file["3cx"]["port"])
        self.var_3cx_username.set(self.config_file["3cx"]["username"])
        self.var_3cx_password.set(self.config_file["3cx"]["password"])

    def write_config_file(self):
        self.config_file["3cx"]["scheme"] = self.var_3cx_scheme.get()
        self.config_file["3cx"]["domain"] = self.var_3cx_domain.get()
        self.config_file["3cx"]["port"] = self.var_3cx_port.get()
        self.config_file["3cx"]["username"] = self.var_3cx_username.get()
        self.config_file["3cx"]["password"] = self.var_3cx_password.get()
        with open(self.config_file_path, "w") as config_file:
            self.config_file.write(config_file)
        config_file.close()


class Window3cxConfig(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        tk.Toplevel.__init__(self, master, *args, **kwargs)
        self.grab_set()
        self.focus_force()

        # Create a window frame
        frm_window = tk.Frame(master=self)
        frm_window.pack()

        # Create 3cx options frame
        frm_3cx_options = tk.Frame(master=frm_window)
        frm_3cx_options.config(width=300, height=200, relief="ridge", borderwidth=2)
        frm_3cx_options.pack()

        # 3cx URL
        lbl_3cx_url = tk.Label(master=frm_3cx_options, text="3CX URL:")
        lbl_3cx_url.grid(row=0, column=0, padx=(5, 0), sticky="w")

        # Create a 3cx URL frame in that window
        frm_3cx_url = tk.Frame(master=frm_3cx_options)
        frm_3cx_url.grid_columnconfigure(2, weight=1)
        frm_3cx_url.grid(row=0, column=1)
        # frm_3cx_url.pack(anchor="w")

        opt_3cx_scheme = tk.OptionMenu(
            frm_3cx_url, self.master.var_3cx_scheme, *["https", "http"]
        )
        lbl_3cx_scheme_ending = tk.Label(master=frm_3cx_url, text="://")
        ent_3cx_domain = tk.Entry(
            master=frm_3cx_url, textvariable=self.master.var_3cx_domain
        )
        lbl_3cx_server_ending = tk.Label(master=frm_3cx_url, text=":")
        ent_3cx_port = tk.Entry(
            master=frm_3cx_url, textvariable=self.master.var_3cx_port, width=5
        )

        elements = [
            opt_3cx_scheme,
            lbl_3cx_scheme_ending,
            ent_3cx_domain,
            lbl_3cx_server_ending,
            ent_3cx_port,
        ]

        for y, element in enumerate(elements):
            element.grid(row=1, column=y, sticky="we")

        lbl_3cx_username = tk.Label(master=frm_3cx_options, text="Username:")
        ent_3cx_username = tk.Entry(
            master=frm_3cx_options, textvariable=self.master.var_3cx_username
        )

        lbl_3cx_password = tk.Label(master=frm_3cx_options, text="Password:")
        ent_3cx_password = tk.Entry(
            master=frm_3cx_options, textvariable=self.master.var_3cx_password, show="*"
        )
        lbl_3cx_username.grid(row=2, column=0, padx=(5, 0))
        ent_3cx_username.grid(row=2, column=1, sticky="we")
        lbl_3cx_password.grid(row=3, column=0, padx=(5, 0))
        ent_3cx_password.grid(row=3, column=1, sticky="we")

        # Test and OK Buttons
        frm_navigation = tk.Frame(master=frm_window)
        frm_navigation.pack(side="bottom", anchor="e")

        btn_test = tk.Button(
            master=frm_navigation, text="Test", command=self.test_connection
        )
        btn_ok = tk.Button(
            master=frm_navigation, text="OK", command=lambda *args: self.destroy()
        )

        btn_test.grid(row=0, column=0, padx=5)
        btn_ok.grid(row=0, column=1, padx=5)

    @property
    def server_url(self):
        return (
            self.master.var_3cx_scheme.get()
            + "://"
            + self.master.var_3cx_domain.get()
            + ":"
            + self.master.var_3cx_port.get()
        )

    def test_connection(self):
        api = Api(server_url=self.server_url)
        api.authenticate(
            username=self.master.var_3cx_username.get(),
            password=self.master.var_3cx_password.get(),
        )
