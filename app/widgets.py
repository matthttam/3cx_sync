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
