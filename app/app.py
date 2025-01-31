import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from threading import Thread

from app.mapping import CSVMapping
from app.windows import WindowCSVMapping, WindowAppConfig, Window, WindowSync
from app.config import AppConfig
from app.widgets import WidgetList
from sync.sync_strategy import SyncCSV, SyncSourceStrategy
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
        self.app_config = app_config
        self.logger = logger
        self.sync = None
        self.sync_thread = None

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

        # Button: Exit
        self.widgets.btn_exit = ttk.Button(
            self.widgets.frm_left_column,
            text="Exit",
            command=self.handle_exit_click,
        )
        self.widgets.btn_exit.pack(**self.pack_defaults["btn"], side=tk.BOTTOM)

        # Frame: Right Frame
        self.widgets.frm_right_column = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_right_column.pack(fill="both", expand=True, **self.pack_defaults["frm"])

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

        # Button: Export Configs
        self.widgets.btn_export_configs = ttk.Button(
            self.widgets.tab_sync_csv,
            text="Export Configs",
            command=self.handle_csv_export_configs_click,
        )
        self.widgets.btn_export_configs.pack(**self.pack_defaults["btn"])

    def show_WindowAppConfig(self):
        WindowAppConfig(self, self.app_config)

    def show_WindowCSVMapping(self):
        WindowCSVMapping(self)

    def handle_exit_click(self) -> None:
        self.destroy()

    def handle_csv_sync_click(self) -> None:
        window_sync = WindowSync(self)
        self.sync_thread = Thread(target=run_sync, args=(SyncCSV, self.logger, self.on_sync_initialized))
        window_sync.periodic_update()
        self.sync_thread.start()

    def handle_csv_export_configs_click(self) -> None:
        export_directory = askdirectory()
        if not export_directory:
            return
        self._export_app_config(export_directory)
        self._export_csv_mapping(export_directory)

    def _export_app_config(self, export_directory: str) -> None:
        self.app_config.save_to(export_directory)

    def _export_csv_mapping(self, export_directory: str) -> None:
        csv_mapping = CSVMapping()
        csv_mapping.load()
        csv_mapping.save_to(export_directory)

    def on_sync_initialized(self, sync):
        self.sync = sync

    def resume_sync(self):
        if not self.sync:
            return
        self.sync.resume()

    def pause_sync(self):
        if not self.sync:
            return
        self.sync.pause()

    def toggle_sync_state(self):
        if not self.sync:
            return
        if self.sync.is_paused:
            self.sync.resume()
        else:
            self.sync.pause()

    def terminate_sync(self):
        if not self.sync:
            return
        self.sync.terminate()
        self.sync.running_event.set()
        # if self.sync_thread.is_alive():
        #    self.sync_thread.join()
