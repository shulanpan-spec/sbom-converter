#!/usr/bin/env python3
"""
Desktop Clock App
A simple desktop clock with date and time display.
"""

import tkinter as tk
from datetime import datetime


class DesktopClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Clock")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        # Keep window on top toggle
        self.always_on_top = tk.BooleanVar(value=False)

        self._build_ui()
        self._update()

    def _build_ui(self):
        # Time label
        self.time_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 60, "bold"),
            fg="#e0e0e0",
            bg="#1a1a2e",
        )
        self.time_label.pack(padx=40, pady=(30, 5))

        # Date label
        self.date_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 18),
            fg="#a0a0c0",
            bg="#1a1a2e",
        )
        self.date_label.pack(pady=(0, 10))

        # Weekday label
        self.weekday_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 14),
            fg="#7070a0",
            bg="#1a1a2e",
        )
        self.weekday_label.pack(pady=(0, 20))

        # Always on top checkbox
        cb = tk.Checkbutton(
            self.root,
            text="Always on top",
            variable=self.always_on_top,
            command=self._toggle_on_top,
            fg="#606080",
            bg="#1a1a2e",
            activebackground="#1a1a2e",
            activeforeground="#a0a0c0",
            selectcolor="#1a1a2e",
            font=("Courier New", 10),
        )
        cb.pack(pady=(0, 15))

    def _toggle_on_top(self):
        self.root.attributes("-topmost", self.always_on_top.get())

    def _update(self):
        now = datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%Y-%m-%d"))
        self.weekday_label.config(text=now.strftime("%A"))
        # Schedule next update in 1 second
        self.root.after(1000, self._update)


def main():
    root = tk.Tk()
    DesktopClock(root)
    root.mainloop()


if __name__ == "__main__":
    main()
