import tkinter as tk
from datetime import datetime


class Sync:
    user_data = list()

    def __init__(self, text: tk.Text = None) -> None:
        self.text = text
        self.newline = ""  # Set to "\n" on first output

    def output(self, value) -> None:
        text_output = self.newline + self.get_timestamp() + value
        if self.text:
            self.text.insert(tk.END, text_output)
            self.newline = "\n"
            # self.text.master.update()
            self.text.winfo_toplevel().update()
        else:
            print(text_output)

    def output_spacer(self) -> None:
        self.output("--------------------")

    def get_timestamp(self) -> str:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return f"[{dt}]"
