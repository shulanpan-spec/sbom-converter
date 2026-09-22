#!/usr/bin/env python3
import tkinter as tk
from datetime import datetime
import ctypes
import sys
import os
import winreg

if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

BG = "#0f0f1a"
ACCENT = "#f0c040"
FG_PRIMARY = "#e8e8f0"
FG_DIM = "#6060a0"
FONT = "Consolas"
APP_NAME = "DesktopClock"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def get_exe_path():
    if getattr(sys, "frozen", False):
        return sys.executable
    return os.path.abspath(__file__)


def is_autostart_enabled():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False


def set_autostart(enable: bool):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0,
                        winreg.KEY_SET_VALUE) as key:
        if enable:
            path = get_exe_path()
            if path.endswith(".py"):
                pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
                value = f'"{pythonw}" "{path}"'
            else:
                value = f'"{path}"'
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, value)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass


class DesktopClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Work Week Clock")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self._drag_x = 0
        self._drag_y = 0

        self._build_ui()
        self._update()
        self._center()

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w = self.winfo_width()
        h = self.winfo_height()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    def _build_ui(self):
        outer = tk.Frame(self, bg=BG, padx=2, pady=2)
        outer.pack(fill="both", expand=True)

        bar = tk.Frame(outer, bg="#1a1a30", height=28)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        title_lbl = tk.Label(bar, text="Work Week Clock", font=(FONT, 10),
                             fg=FG_DIM, bg="#1a1a30", cursor="fleur")
        title_lbl.pack(side="left", padx=10)
        title_lbl.bind("<ButtonPress-1>", self._drag_start)
        title_lbl.bind("<B1-Motion>", self._drag_move)

        tk.Button(bar, text="×", font=(FONT, 12, "bold"),
                  fg=FG_DIM, bg="#1a1a30", bd=0,
                  activebackground="#cc3333", activeforeground="white",
                  cursor="hand2", command=self.destroy).pack(side="right", padx=6)

        pin_btn = tk.Button(bar, text="\U0001f4cc", font=(FONT, 10),
                            fg=ACCENT, bg="#1a1a30", bd=0,
                            activebackground="#1a1a30", cursor="hand2",
                            command=self._toggle_pin)
        pin_btn.pack(side="right")
        self._pin_btn = pin_btn
        self._pinned = True

        self._autostart_var = tk.BooleanVar(value=is_autostart_enabled())
        tk.Checkbutton(
            bar, text="开机启动", font=(FONT, 9),
            variable=self._autostart_var,
            command=self._toggle_autostart,
            fg=FG_DIM, bg="#1a1a30",
            activebackground="#1a1a30", activeforeground=ACCENT,
            selectcolor="#1a1a30",
        ).pack(side="right", padx=(0, 8))

        bar.bind("<ButtonPress-1>", self._drag_start)
        bar.bind("<B1-Motion>", self._drag_move)

        content = tk.Frame(outer, bg=BG, padx=18, pady=12)
        content.pack()

        tk.Label(content, text="WORK WEEK", font=(FONT, 8),
                 fg=FG_DIM, bg=BG).pack()

        self.week_label = tk.Label(content, text="",
                                   font=(FONT, 44, "bold"),
                                   fg=ACCENT, bg=BG)
        self.week_label.pack(pady=(0, 2))

        self.date_label = tk.Label(content, text="",
                                   font=(FONT, 10), fg=FG_PRIMARY, bg=BG)
        self.date_label.pack()

        self.time_label = tk.Label(content, text="",
                                   font=(FONT, 18), fg=FG_PRIMARY, bg=BG)
        self.time_label.pack(pady=(2, 0))

    def _toggle_pin(self):
        self._pinned = not self._pinned
        self.attributes("-topmost", self._pinned)
        self._pin_btn.config(fg=ACCENT if self._pinned else FG_DIM)

    def _toggle_autostart(self):
        set_autostart(self._autostart_var.get())

    def _drag_start(self, event):
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()

    def _drag_move(self, event):
        self.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")

    def _update(self):
        now = datetime.now()
        week = now.isocalendar()[1]
        self.week_label.config(text=f"W{week:02d}")
        self.date_label.config(text=now.strftime("%Y-%m-%d  %A"))
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.after(1000, self._update)


if __name__ == "__main__":
    app = DesktopClock()
    app.mainloop()
