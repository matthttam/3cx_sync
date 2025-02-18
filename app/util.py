import os
import functools
from pathlib import Path

import platformdirs
import tkinter as tk

from pydantic import BaseModel

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


def get_variable_for_model_field(master: tk.Tk, mapping: BaseModel, field_key: str) -> tk.Variable:
    field_info = mapping.model_fields[field_key]
    current_value = getattr(mapping, field_key)

    if issubclass(field_info.annotation, str):
        var = tk.StringVar(master, current_value)
    elif issubclass(field_info.annotation, bool):
        var = tk.BooleanVar(master, current_value)
    else:
        raise TypeError("Field type not valid for mapping configuration.")

    # Trace to update the mapping when the variable changes
    def update_model(*_):
        setattr(mapping, field_key, var.get())

    var.trace_add("write", update_model)
    return var
