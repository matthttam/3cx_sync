from dataclasses import dataclass
import tkinter as tk
from typing import NamedTuple


class Checkbox(tk.Checkbutton):

    def __init__(self, *args, value=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = tk.BooleanVar(self, value)
        self.config(variable=self.variable)

    @property
    def checked(self):
        return self.variable.get()

    def check(self):
        self.variable.set(True)

    def uncheck(self):
        self.variable.set(False)


class ExtensionMappingFieldSet(NamedTuple):
    header: tk.Entry
    field: tk.Entry
    static: Checkbox
    update: Checkbox
    key: Checkbox
    delete: tk.Button


@dataclass
class WidgetList:
    pass


def select_all(event):
    widget = event.widget
    widget.select_range(0, tk.END)
    widget.icursor(tk.END)  # Move cursor to the end


def bind_shortcuts(widget):
    # Bind CTRL+A for select all
    widget.bind_all("<Control-a>", select_all)
