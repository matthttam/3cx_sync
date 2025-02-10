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

    def check(self) -> None:
        self.variable.set(True)

    def uncheck(self) -> None:
        self.variable.set(False)


class ExtensionMappingFieldSet(NamedTuple):
    header: tk.Entry
    field: tk.Entry
    static: Checkbox
    update: Checkbox
    key: Checkbox
    delete: tk.Button

    def destroy(self) -> None:
        """Destroy all widgets in the field set."""
        for widget in self._widgets():
            widget.destroy()

    def change_row(self, **kwargs) -> None:
        """Adjust all widges of a set to a new row."""
        for idx, widget in enumerate(self._widgets()):
            row = kwargs.get("row", 0)
            widget.grid(row=row, column=idx)

    def _widgets(self) -> list:
        """Return a list of all widgets for easy iteration."""
        return [getattr(self, field) for field in self._fields]


@dataclass
class WidgetList:
    pass
