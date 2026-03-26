"""
Windows Desktop Calendar Widget
显示日期、工作周、工作天、小时、分钟
"""

import tkinter as tk
from tkinter import font as tkfont
import datetime
import sys


def get_work_info(now: datetime.datetime) -> dict:
    """计算工作周、工作天等信息"""
    # ISO 工作周编号
    iso = now.isocalendar()
    work_week = iso[1]

    # 本年已过的工作天（周一~周五）
    year_start = datetime.date(now.year, 1, 1)
    today = now.date()
    work_days_ytd = 0
    d = year_start
    while d <= today:
        if d.weekday() < 5:  # 0=周一 … 4=周五
            work_days_ytd += 1
        d += datetime.timedelta(days=1)

    # 本周已过工作天（含今天，若今天是工作日）
    week_day = now.weekday()  # 0=周一
    if week_day < 5:
        work_days_this_week = week_day + 1
    else:
        work_days_this_week = 5  # 周末按5算

    # 今天是否工作日
    is_workday = now.weekday() < 5

    return {
        "work_week": work_week,
        "work_days_ytd": work_days_ytd,
        "work_days_this_week": work_days_this_week,
        "is_workday": is_workday,
        "weekday_cn": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
    }


class CalendarWidget:
    # ── 配色方案 ──────────────────────────────────────────
    BG           = "#1a1a2e"   # 深蓝黑背景
    CARD_BG      = "#16213e"   # 卡片背景
    ACCENT       = "#0f3460"   # 强调色
    HIGHLIGHT    = "#e94560"   # 红色高亮
    TEXT_PRIMARY = "#eaeaea"   # 主文字
    TEXT_DIM     = "#8892a4"   # 次要文字
    BORDER       = "#0f3460"   # 边框

    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()
        self._build_ui()
        self._offset_x = 0
        self._offset_y = 0
        self._tick()

    # ── 窗口配置 ─────────────────────────────────────────
    def _setup_window(self):
        root = self.root
        root.title("桌面时钟")
        root.overrideredirect(True)          # 无边框
        root.attributes("-topmost", True)    # 始终置顶
        root.attributes("-alpha", 0.93)      # 略透明
        root.configure(bg=self.BG)
        root.resizable(False, False)

        # 初始位置：屏幕右下角
        w, h = 300, 380
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = sw - w - 20
        y = sh - h - 60
        root.geometry(f"{w}x{h}+{x}+{y}")

        # 拖拽绑定
        root.bind("<ButtonPress-1>",   self._drag_start)
        root.bind("<B1-Motion>",       self._drag_move)
        root.bind("<ButtonPress-3>",   self._show_menu)   # 右键菜单

    # ── UI 构建 ───────────────────────────────────────────
    def _build_ui(self):
        root = self.root
        pad = dict(padx=14, pady=6)

        # ── 顶部标题栏 ──
        title_bar = tk.Frame(root, bg=self.ACCENT, height=28)
        title_bar.pack(fill="x")
        title_bar.bind("<ButtonPress-1>", self._drag_start)
        title_bar.bind("<B1-Motion>",     self._drag_move)

        tk.Label(title_bar, text="  ◆ 桌面日历", bg=self.ACCENT,
                 fg=self.TEXT_PRIMARY, font=("微软雅黑", 9, "bold"),
                 anchor="w").pack(side="left", fill="x", expand=True)

        close_btn = tk.Label(title_bar, text="✕ ", bg=self.ACCENT,
                             fg=self.TEXT_DIM, font=("Segoe UI", 10),
                             cursor="hand2")
        close_btn.pack(side="right")
        close_btn.bind("<Button-1>", lambda e: root.destroy())

        # ── 日期大字 ──
        date_frame = tk.Frame(root, bg=self.BG)
        date_frame.pack(fill="x", padx=14, pady=(14, 4))

        self.lbl_month = tk.Label(date_frame, text="", bg=self.BG,
                                  fg=self.TEXT_DIM, font=("微软雅黑", 11))
        self.lbl_month.pack(anchor="w")

        self.lbl_day = tk.Label(date_frame, text="", bg=self.BG,
                                fg=self.TEXT_PRIMARY,
                                font=("Segoe UI", 62, "bold"))
        self.lbl_day.pack(anchor="w")

        self.lbl_weekday = tk.Label(date_frame, text="", bg=self.BG,
                                    fg=self.HIGHLIGHT, font=("微软雅黑", 13, "bold"))
        self.lbl_weekday.pack(anchor="w")

        # 分隔线
        tk.Frame(root, bg=self.BORDER, height=1).pack(fill="x", padx=14, pady=6)

        # ── 时间大字 ──
        time_frame = tk.Frame(root, bg=self.BG)
        time_frame.pack(fill="x", padx=14, pady=(0, 4))

        self.lbl_time = tk.Label(time_frame, text="", bg=self.BG,
                                 fg=self.TEXT_PRIMARY,
                                 font=("Segoe UI", 42, "bold"))
        self.lbl_time.pack(side="left", anchor="w")

        self.lbl_second = tk.Label(time_frame, text="", bg=self.BG,
                                   fg=self.TEXT_DIM,
                                   font=("Segoe UI", 20))
        self.lbl_second.pack(side="left", anchor="s", pady=(0, 6))

        # 分隔线
        tk.Frame(root, bg=self.BORDER, height=1).pack(fill="x", padx=14, pady=6)

        # ── 工作信息卡片 ──
        card = tk.Frame(root, bg=self.CARD_BG, bd=0)
        card.pack(fill="x", padx=14, pady=(0, 14))

        def info_row(parent, label_text, var_attr, row):
            tk.Label(parent, text=label_text, bg=self.CARD_BG,
                     fg=self.TEXT_DIM, font=("微软雅黑", 9),
                     width=10, anchor="w").grid(row=row, column=0,
                                                padx=(12, 4), pady=5, sticky="w")
            lbl = tk.Label(parent, text="", bg=self.CARD_BG,
                           fg=self.TEXT_PRIMARY, font=("Segoe UI", 14, "bold"),
                           anchor="e")
            lbl.grid(row=row, column=1, padx=(4, 12), pady=5, sticky="e")
            setattr(self, var_attr, lbl)
            # 装饰条
            tk.Frame(parent, bg=self.HIGHLIGHT, width=3).grid(
                row=row, column=2, padx=(0, 8), pady=5, sticky="ns")

        card.columnconfigure(1, weight=1)
        info_row(card, "工作周",  "lbl_wweek",  0)
        info_row(card, "周内工作天", "lbl_wday_week", 1)
        info_row(card, "年内工作天", "lbl_wday_ytd", 2)

    # ── 更新数据 ─────────────────────────────────────────
    def _tick(self):
        now = datetime.datetime.now()
        info = get_work_info(now)

        # 日期
        self.lbl_month.config(
            text=f"{now.year} 年  {now.month:02d} 月")
        self.lbl_day.config(text=f"{now.day:02d}")
        self.lbl_weekday.config(
            text=info["weekday_cn"] + ("  ✦ 工作日" if info["is_workday"] else "  ✧ 休息日"))

        # 时间
        self.lbl_time.config(
            text=f"{now.hour:02d}:{now.minute:02d}")
        self.lbl_second.config(text=f":{now.second:02d}")

        # 工作信息
        self.lbl_wweek.config(
            text=f"第 {info['work_week']} 周")
        self.lbl_wday_week.config(
            text=f"{info['work_days_this_week']} / 5 天")
        self.lbl_wday_ytd.config(
            text=f"{info['work_days_ytd']} 天")

        # 每秒刷新
        self.root.after(1000, self._tick)

    # ── 拖拽 ─────────────────────────────────────────────
    def _drag_start(self, event):
        self._offset_x = event.x_root - self.root.winfo_x()
        self._offset_y = event.y_root - self.root.winfo_y()

    def _drag_move(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        self.root.geometry(f"+{x}+{y}")

    # ── 右键菜单 ─────────────────────────────────────────
    def _show_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg=self.ACCENT,
                       fg=self.TEXT_PRIMARY, activebackground=self.HIGHLIGHT)
        menu.add_command(label="始终置顶 ✔" if self.root.attributes("-topmost")
                         else "始终置顶", command=self._toggle_topmost)
        menu.add_separator()
        menu.add_command(label="退出", command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    def _toggle_topmost(self):
        current = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current)


def main():
    root = tk.Tk()
    app = CalendarWidget(root)
    root.mainloop()


if __name__ == "__main__":
    main()
