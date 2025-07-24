import os
import sys
import platform
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from threading import Thread
import tkinter.font as tkfont
import darkdetect

from sync.strategy.csv.mapping import CSVMapping
from app.windows import WindowCSVMapping, WindowAppConfig, Window, WindowSync
from app.config import AppConfig
from app.widgets import WidgetList
from app.util import handle_error
from sync.strategy.csv.sync_csv import SyncCSV
from sync.sync import run_sync
from sync.logging import SyncLogger

import sv_ttk

# from app.themes.Forest-ttk-theme-1.0.example import scale


class App(tk.Tk, Window):
    def __init__(self, *args, logger: SyncLogger, app_config: AppConfig, **kwargs):
        super().__init__(*args, **kwargs)  # This ensures both tk.Tk and Window are initialized properly

        self.title("3cx Sync")
        self.resizable(height=True, width=True)
        self.geometry("600x400")
        self.style = ttk.Style(self)

        self.widgets = WidgetList()
        self.is_paused = False
        self.app_config = app_config
        self.logger = logger
        self.sync = None
        self.sync_thread = None
        self.load_theme()
        self.set_font()  # Must occur after theme load
        self.build_gui()

    def load_theme(self):
        """Load and apply the custom theme."""

        # If we are on windows, apply the ttk_sv theme. Otherwise use clam.
        if platform.system() == "Windows":
            sv_ttk.set_theme(darkdetect.theme())
        elif "clam" in self.style.theme_names():
            self.style.theme_use("clam")
        elif "default" in self.style.theme_names():
            self.style.theme_use("default")

    def set_font(self, size=15):
        """Return a platform-appropriate font."""
        available_fonts = set(tkfont.families())  # Get all available font families

        # Check availability and assign accordingly
        if platform.system() == "Windows":
            font = "Segoe UI"
        elif platform.system() == "Darwin":  # macOS
            font = "Helvetica"
        elif platform.system() == "Linux":
            font = "Ubuntu"

        # Fallback to Arial if system specific font is not actually available.
        if not font or font not in available_fonts:
            font = "Arial"

        self.style.configure(".", font=(font, size))

    def build_gui(self):
        # Frame: Window
        self.widgets.frm_window = ttk.Frame(self, width=500, height=1000)
        self.widgets.frm_window.pack(fill="both", anchor="nw", expand=True)

        # Frame: Left Column
        self.widgets.frm_left_column = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_left_column.pack(
            padx=self.defaults.pack.frm.padx,
            pady=self.defaults.pack.frm.pady,
            side=self.defaults.pack.frm.side,
            fill=tk.Y,
        )

        # Button: Configure App
        self.widgets.btn_show_window_app_config = ttk.Button(
            self.widgets.frm_left_column,
            text="Configure App",
            command=self.show_WindowAppConfig,
        )

        self.widgets.btn_show_window_app_config.pack(
            padx=self.defaults.pack.btn.padx,
            pady=self.defaults.pack.btn.pady,
        )

        # Button: Exit
        self.widgets.btn_exit = ttk.Button(
            self.widgets.frm_left_column,
            text="Exit",
            command=self.handle_exit_click,
        )
        self.widgets.btn_exit.pack(padx=self.defaults.pack.btn.padx, pady=self.defaults.pack.btn.pady, side=tk.BOTTOM)

        # Frame: Right Frame
        self.widgets.frm_right_column = ttk.Frame(self.widgets.frm_window)
        self.widgets.frm_right_column.pack(
            fill=tk.BOTH,
            expand=True,
            padx=self.defaults.pack.frm.padx,
            pady=self.defaults.pack.frm.pady,
            side=self.defaults.pack.frm.side,
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

        self.widgets.btn_show_window_csv_config.pack(
            padx=self.defaults.pack.btn.padx,
            pady=self.defaults.pack.btn.pady,
        )

        # Button: Sync CSV
        self.widgets.btn_sync_csv = ttk.Button(
            self.widgets.tab_sync_csv,
            text="Sync CSV",
            command=self.handle_csv_sync_click,
        )
        self.widgets.btn_sync_csv.pack(
            padx=self.defaults.pack.btn.padx,
            pady=self.defaults.pack.btn.pady,
        )

        # Button: Export Configs
        self.widgets.btn_export_configs = ttk.Button(
            self.widgets.tab_sync_csv,
            text="Export Configs",
            command=self.handle_csv_export_configs_click,
        )
        self.widgets.btn_export_configs.pack(
            padx=self.defaults.pack.btn.padx,
            pady=self.defaults.pack.btn.pady,
        )

    @handle_error
    def show_WindowAppConfig(self):
        WindowAppConfig(self, self.app_config)

    @handle_error
    def show_WindowCSVMapping(self):
        csv_mapping = CSVMapping(config_path=self.app_config.config_path)
        csv_mapping.initialize()
        WindowCSVMapping(self, csv_mapping=csv_mapping)

    def handle_exit_click(self) -> None:
        self.destroy()

    @handle_error
    def handle_csv_sync_click(self) -> None:
        window_sync = WindowSync(self)
        kwargs = {
            "sync_source_class": SyncCSV,
            "logger": self.logger,
            "on_sync_initialized": self.on_sync_initialized,
            "config_path": self.app_config.config_path,
        }
        self.sync_thread = Thread(target=run_sync, kwargs=kwargs)
        window_sync.periodic_update()
        self.sync_thread.start()

    @handle_error
    def handle_csv_export_configs_click(self) -> None:
        export_directory = askdirectory()
        if not export_directory:
            return
        self._export_app_config(export_directory)
        self._export_csv_mapping(export_directory)

    def _export_app_config(self, export_directory: str) -> None:
        self.app_config.save_to(export_directory)

    def _export_csv_mapping(self, export_directory: str) -> None:
        csv_mapping = CSVMapping(config_path=self.app_config.config_path)
        csv_mapping.load()
        csv_mapping.save_to(export_directory)

    def handle_toggle_theme_click(self):
        sv_ttk.toggle_theme()
        self.set_font(size=30)

    def on_sync_initialized(self, sync):
        self.sync = sync

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
