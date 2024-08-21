import requests
import tkinter as tk
from app.windows import WindowCSVMapping, Window3cxConfig
from app.config import AppConfig, TCXConfig
from sync.sync_strategy import SyncCSV
from sync.sync import Sync
from tcx_api.exceptions import APIAuthenticationError
from tkinter.scrolledtext import ScrolledText


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.app_config = AppConfig()
        self.tcx_config = TCXConfig()

        # Window Options
        self.wm_title("3cx Sync")
        self.geometry('1200x800')

        # Create a window frame
        frm_window = tk.Frame(
            master=self, background="pink", width=500, height=1000)
        frm_window.pack(fill="both", anchor="ne", expand=True)

        # Frame: Left Column
        frm_left_column = tk.Frame(master=frm_window)
        frm_left_column.pack(side="left")

        # Button: Configure 3CX
        btn_show_window_3cx_config = tk.Button(
            master=frm_left_column,
            text="Configure 3CX",
            command=self.show_Window3cxConfig,
        )
        btn_show_window_3cx_config.pack(fill="x")

        # Button: Configure CSV
        btn_show_window_3cx_config = tk.Button(
            master=frm_left_column,
            text="Configure CSV",
            command=self.show_WindowCSVMapping,
        )
        btn_show_window_3cx_config.pack(fill="x")

        # Right Frame
        frm_right_column = tk.Frame(master=frm_window, background="blue")
        frm_right_column.pack(side="left", fill="both",
                              expand=True, padx="5", pady="5")

        # Text:  Output
        self.txt_output = ScrolledText(
            master=frm_right_column, relief="sunken", name="output"
        )
        self.txt_output.pack(fill="both", expand=True)
        # self.txt_output.bind("<1>", lambda event: self.txt_output.focus_set())
        # self.txt_output.bind("<Key>", lambda e: "break")

        # Form: Sync
        # frm_sync = tk.Frame(master=frm_right_column, background="green")
        # frm_sync.pack()

        # Button: Sync CSV
        btn_sync_csv = tk.Button(
            master=frm_right_column, text="Sync CSV", command=self.handle_csv_sync_click
        )
        btn_sync_csv.pack(side="bottom", anchor="s")

        # Form: Navigation Buttons
        frm_navigation = tk.Frame(master=self)
        frm_navigation.pack(side="bottom", anchor="e", pady=5)

        btn_exit = tk.Button(
            master=frm_navigation, text="Exit", command=self.handle_exit_click
        )
        btn_exit.grid(row=0, column=1, padx=5)

    def show_Window3cxConfig(self):
        Window3cxConfig(master=self, tcx_config=self.tcx_config)

    def show_WindowCSVMapping(self):
        WindowCSVMapping(master=self)

    def handle_exit_click(self):
        self.destroy()

    def handle_csv_sync_click(self):
        sync = Sync(sync_source=SyncCSV, text=self.txt_output)
        try:
            sync.sync()
        except APIAuthenticationError:
            sync.output("Failed to sync. Unable to authenticate.")
        except Exception as e:
            sync.output(f"Failed to sync. {e}")
