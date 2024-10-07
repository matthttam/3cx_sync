import tkinter as tk
import logging
from app.windows import WindowCSVMapping, WindowAppConfig, WindowPreferences
from app.config import AppConfig
from sync.sync_strategy import SyncCSV
from sync.sync import run_sync, Sync
from tcx_api.exceptions import APIAuthenticationError
from tkinter.scrolledtext import ScrolledText
from sync.logging import SyncLogger


class App(tk.Tk):

    def __init__(self, *args, sync_logger: SyncLogger, app_config: AppConfig, **kwargs):
        # app_args = kwargs.pop("app_args")
        # logger = kwargs.pop("logger")
        tk.Tk.__init__(self, *args, **kwargs)

        self.is_paused = False
        self.app_config = app_config  # AppConfig()

        self.build_gui()
        sync_logger.addTextWindowHandler(self.txt_output)
        self.logger = sync_logger.get_logger()

    def build_gui(self):
        # Window Options
        self.wm_title("3cx Sync")
        self.geometry("1200x800")

        # Create a window frame
        self.frm_window = tk.Frame(master=self, width=500, height=1000)
        self.frm_window.pack(fill="both", anchor="ne", expand=True)

        # Frame: Left Column
        self.frm_left_column = tk.Frame(master=self.frm_window)
        self.frm_left_column.pack(side="left", ipadx=5)

        # Button: Configure App
        self.btn_show_window_csv_config = tk.Button(
            master=self.frm_left_column,
            text="Configure App",
            command=self.show_WindowAppConfig,
        )
        self.btn_show_window_csv_config.pack(fill="x")

        # Button: Configure CSV
        self.btn_show_window_csv_config = tk.Button(
            master=self.frm_left_column,
            text="Configure CSV",
            command=self.show_WindowCSVMapping,
        )
        self.btn_show_window_csv_config.pack(fill="x")

        # Frame: Right Frame
        self.frm_right_column = tk.Frame(master=self.frm_window)
        self.frm_right_column.pack(
            side="left", fill="both", expand=True, padx="5", pady="5"
        )

        # Text:  Output
        self.txt_output = ScrolledText(
            master=self.frm_right_column, relief="sunken", name="output"
        )
        self.txt_output.pack(fill="both", expand=True)

        # Form: Sync Buttons
        self.frm_sync_buttons = tk.Frame(
            master=self.frm_right_column, background="green"
        )
        self.frm_sync_buttons.pack(side="bottom")

        # Button: Sync CSV
        self.btn_sync_csv = tk.Button(
            master=self.frm_sync_buttons,
            text="Sync CSV",
            command=self.handle_csv_sync_click,
        )
        self.btn_sync_csv.pack(side="left", anchor="s")
        # Button: Pause/Resume
        self.btn_pause_resume = tk.Button(
            master=self.frm_sync_buttons, text="Pause", command=self.handle_pause_resume
        )
        self.btn_pause_resume.pack(side="left", anchor="s")

        # Form: Navigation Buttons
        self.frm_navigation = tk.Frame(master=self)
        self.frm_navigation.pack(side="bottom", anchor="e", pady=5)

        self.btn_exit = tk.Button(
            master=self.frm_navigation, text="Exit", command=self.handle_exit_click
        )
        self.btn_exit.grid(row=0, column=1, padx=5)

    def show_WindowAppConfig(self):
        WindowAppConfig(master=self, app_config=self.app_config)

    def show_WindowCSVMapping(self):
        WindowCSVMapping(master=self)

    def show_WindowPreferences(self):
        WindowPreferences(master=self)

    def handle_exit_click(self):
        self.destroy()

    def handle_csv_sync_click(self):
        run_sync(logger=self.logger, sync_source=SyncCSV)

    def handle_pause_resume(self):
        self.is_paused = not self.is_paused
        self.btn_pause_resume.configure(text="Resume" if self.is_paused else "Pause")
        if self.is_paused:
            self.pause_app()

    def pause_app(self):
        self.logger.info(f"Paused by user")
        while True:
            self.update()
            self.after(100)
            if not self.is_paused:
                return

    # def output(self, value: str, level="info") -> None:
    #    self.logger.info(value)
    #    self.update()
