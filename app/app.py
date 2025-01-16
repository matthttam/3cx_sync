import os
import sys
import tkinter as tk
from tkinter import ttk
from app.windows import WindowCSVMapping, WindowAppConfig, Window, WindowSync
from app.config import AppConfig
from app.widgets import WidgetList
from sync.sync_strategy import SyncCSV
from sync.sync import run_sync

from sync.logging import SyncLogger

# from app.themes.Forest-ttk-theme-1.0.example import scale


class App(tk.Tk, Window):

    def __init__(self, *args, logger: SyncLogger, app_config: AppConfig, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("3cx Sync")
        self.resizable(height=True, width=True)

        self.widgets = WidgetList()
        self.is_paused = False
        self.sync_running = False
        self.app_config = app_config
        self.logger = logger

        # Load the theme and apply styles
        self.load_theme()
        self.build_gui()

    def load_theme(self):
        """Load and apply the custom theme."""
        self.option_add("*tearOff", False)
        self.style = ttk.Style(self)

        self.tk.call("source", self.get_theme_path())
        self.style.theme_use("forest-light")
        self.style.configure(".", font=("Helvetica", 15))
        self.geometry("600x400")

    def get_theme_path(self):
        # Detect if running from EXE or source
        default_theme_path = ("themes", "Forest-ttk-theme-1.0", "forest-light.tcl")
        if getattr(sys, "_MEIPASS", False):
            # Running in a PyInstaller bundle
            theme_path = os.path.join(sys._MEIPASS, *default_theme_path)
        else:
            # Running as a script
            theme_path = os.path.join(os.path.dirname(__file__), *default_theme_path)
        return theme_path

    def build_gui(self):
        # Frame: Window
        self.widgets.frm_window = ttk.Frame(self, width=500, height=1000)
        self.widgets.frm_window.pack(fill="both", anchor="nw", expand=True)

        # Frame: Left Column
        self.widgets.frm_left_column = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_left_column.pack(**self.pack_defaults["frm"], fill=tk.Y)

        # Button: Configure App
        self.widgets.btn_show_window_app_config = ttk.Button(
            self.widgets.frm_left_column,
            text="Configure App",
            command=self.show_WindowAppConfig,
        )

        self.widgets.btn_show_window_app_config.pack(**self.pack_defaults["btn"])

        # Button: Export Config
        self.widgets.btn_export_configs = ttk.Button(
            self.widgets.frm_left_column,
            text="Export Configs",
            command=self.show_WindowAppConfig,
        )
        self.widgets.btn_export_configs.pack(**self.pack_defaults["btn"])

        # Button: Exit
        self.widgets.btn_exit = ttk.Button(
            self.widgets.frm_left_column,
            text="Exit",
            command=self.handle_exit_click,
        )
        self.widgets.btn_exit.pack(**self.pack_defaults["btn"], side=tk.BOTTOM)

        # Frame: Right Frame
        self.widgets.frm_right_column = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_right_column.pack(
            fill="both", expand=True, **self.pack_defaults["frm"]
        )

        # Notebook: Sync Options
        self.widgets.notebook_sync_options = ttk.Notebook(self.widgets.frm_right_column)
        self.widgets.tab_sync_csv = ttk.Frame(self.widgets.notebook_sync_options)
        self.widgets.notebook_sync_options.add(self.widgets.tab_sync_csv, text="CSV")
        self.widgets.notebook_sync_options.pack(fill="both", expand=True)

        # Button: Configure CSV
        self.widgets.btn_show_window_csv_config = ttk.Button(
            self.widgets.tab_sync_csv,
            text="Configure CSV",
            command=self.show_WindowCSVMapping,
        )

        self.widgets.btn_show_window_csv_config.pack(**self.pack_defaults["btn"])

        # Button: Sync CSV
        self.widgets.btn_sync_csv = ttk.Button(
            self.widgets.tab_sync_csv,
            text="Sync CSV",
            command=self.handle_csv_sync_click,
        )
        self.widgets.btn_sync_csv.pack(**self.pack_defaults["btn"])

    def show_WindowAppConfig(self):
        WindowAppConfig(self, self.app_config)

    def show_WindowCSVMapping(self):
        WindowCSVMapping(self)

    def handle_exit_click(self) -> None:
        self.destroy()

    def handle_csv_sync_click(self) -> None:
        window_sync = WindowSync(self, self.logger)
        window_sync.start_sync()

    def run_sync_in_thread(self) -> None:
        try:
            run_sync(sync_source=SyncCSV, logger=self.logger)
        finally:
            self.sync_running = False
