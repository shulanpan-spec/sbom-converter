#!/usr/bin/env python3
"""
Desktop Clock App - Work Week Display
Prominently shows the current work week number.
"""

import tkinter as tk
from datetime import datetime


class DesktopClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Work Week Clock")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.always_on_top = tk.BooleanVar(value=False)

        self._build_ui()
        self._update()

    def _build_ui(self):
        # Work week label (primary focus)
        tk.Label(
            self.root,
            text="WORK WEEK",
            font=("Courier New", 14),
            fg="#7070a0",
            bg="#1a1a2e",
        ).pack(pady=(30, 0))

        self.week_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 90, "bold"),
            fg="#f0c040",
            bg="#1a1a2e",
        )
        self.week_label.pack(padx=50, pady=(0, 5))

        # Date and time (secondary)
        self.date_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 16),
            fg="#a0a0c0",
            bg="#1a1a2e",
        )
        self.date_label.pack(pady=(0, 4))

        self.time_label = tk.Label(
            self.root,
            text="",
            font=("Courier New", 28),
            fg="#e0e0e0",
            bg="#1a1a2e",
        )
        self.time_label.pack(pady=(0, 20))

        # Always on top checkbox
        tk.Checkbutton(
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
        ).pack(pady=(0, 15))

    def _toggle_on_top(self):
        self.root.attributes("-topmost", self.always_on_top.get())

    def _update(self):
        now = datetime.now()
        # ISO week number (Mon=start of week)
        week_num = now.isocalendar()[1]
        self.week_label.config(text=f"W{week_num:02d}")
        self.date_label.config(text=now.strftime("%Y-%m-%d  %A"))
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.root.after(1000, self._update)


def main():
    root = tk.Tk()
    DesktopClock(root)
    root.mainloop()


if __name__ == "__main__":
    main()
