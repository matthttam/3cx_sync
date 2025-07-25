import os
import functools
from pathlib import Path

import platformdirs
import tkinter as tk
import sv_ttk
from sync.logging import LogLevel


def initialize_or_get_user_config_path(app_name, app_author, folder_name) -> Path:
    app_data_dir = platformdirs.user_config_dir(app_name, app_author)
    config_file_path = os.path.join(app_data_dir, folder_name)
    os.makedirs(config_file_path, exist_ok=True)
    return Path(config_file_path)


def handle_error(func):
    """Decorator to wrap a method with error handling."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
            self.logger.log(LogLevel.CRITICAL, f"A critical error has occurred and the application must exit. {e}")

    return wrapper

def get_text_color():
    if sv_ttk.get_theme() == "dark": 
        return "White" 
    return "Black" 