from datetime import datetime

import customtkinter as ctk

from ui.constant import ACTIVITY_MAX_ENTRIES
from ui.styles import PanelCard, panel_title
from ui.theme import *


class ActivityPanel(PanelCard):

    def __init__(self, master):
        super().__init__(master)

        panel_title(self, "Activity Log").pack(
            anchor="w",
            padx=LARGE_PADDING,
            pady=(LARGE_PADDING, SMALL_PADDING),
        )

        self.textbox = ctk.CTkTextbox(
            self,
            height=ACTIVITY_TEXT_HEIGHT,
            font=MONO_FONT,
            fg_color=WINDOW_BG,
            border_color=BORDER,
            border_width=1,
            corner_radius=12,
            wrap="word",
            text_color=TEXT,
        )
        self.textbox.pack(
            fill="both",
            expand=True,
            padx=LARGE_PADDING,
            pady=(0, LARGE_PADDING),
        )

        self._entry_count = 0
        self._append_line("ArgusCrypt Ready...")

    def _append_line(self, line):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{line}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def _trim_history(self):
        while self._entry_count > ACTIVITY_MAX_ENTRIES:
            self.textbox.configure(state="normal")
            content = self.textbox.get("1.0", "end")
            lines = content.splitlines()

            if len(lines) <= 2:
                break

            trimmed = "\n".join(lines[2:])
            if trimmed:
                trimmed += "\n"

            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", trimmed)
            self.textbox.configure(state="disabled")
            self._entry_count -= 1

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._append_line(timestamp)
        self._append_line(f"✔ {message}")
        self._entry_count += 1
        self._trim_history()

    def error(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self._append_line(timestamp)
        self._append_line(f"❌ {message}")
        self._entry_count += 1
        self._trim_history()

    def clear(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
        self._entry_count = 0
        self._append_line("ArgusCrypt Ready...")
