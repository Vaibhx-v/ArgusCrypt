import customtkinter as ctk

from ui.styles import PanelCard, panel_title, progress_bar, transparent_frame
from ui.theme import *


class ProgressPanel(PanelCard):

    def __init__(self, master):
        super().__init__(master)

        self._current_value = 0
        self._target_value = 0
        self._animation_job = None

        header = transparent_frame(self)
        header.pack(fill="x", padx=LARGE_PADDING, pady=(LARGE_PADDING, SMALL_PADDING))

        panel_title(header, "Operation Progress").pack(side="left")

        self.percent = ctk.CTkLabel(
            header,
            text="0%",
            font=("Segoe UI", 16, "bold"),
            text_color=PRIMARY,
        )
        self.percent.pack(side="right")

        self.stage = ctk.CTkLabel(
            self,
            text="Current Stage: Waiting...",
            font=LABEL_FONT,
            text_color=TEXT,
            anchor="w",
        )
        self.stage.pack(fill="x", padx=LARGE_PADDING, pady=(0, SMALL_PADDING))

        self.progress = progress_bar(self)
        self.progress.pack(fill="x", padx=LARGE_PADDING)

        self.status = ctk.CTkLabel(
            self,
            text="Waiting...",
            font=LABEL_FONT,
            text_color=SECONDARY_TEXT,
            anchor="w",
        )
        self.status.pack(fill="x", padx=LARGE_PADDING, pady=(SMALL_PADDING, 4))

        self.estimate = ctk.CTkLabel(
            self,
            text="Estimated completion: Waiting to start",
            font=("Segoe UI", 13),
            text_color=SECONDARY_TEXT,
            anchor="w",
        )
        self.estimate.pack(fill="x", padx=LARGE_PADDING, pady=(0, LARGE_PADDING))

    def _estimate_message(self, value):
        if value <= 0:
            return "Estimated completion: Waiting to start"
        if value >= 100:
            return "Estimated completion: Complete"
        if value < 30:
            return "Estimated completion: ~15 seconds remaining"
        if value < 60:
            return "Estimated completion: ~10 seconds remaining"
        if value < 90:
            return "Estimated completion: ~5 seconds remaining"
        return "Estimated completion: Almost done"

    def _cancel_animation(self):
        if self._animation_job is not None:
            self.after_cancel(self._animation_job)
            self._animation_job = None

    def _animate_step(self):
        if self._current_value >= self._target_value:
            self._animation_job = None
            return

        self._current_value = min(self._current_value + 2, self._target_value)
        self.progress.set(self._current_value / 100)
        self.percent.configure(text=f"{self._current_value}%")
        self._animation_job = self.after(30, self._animate_step)

    def _start_animation(self):
        self._cancel_animation()
        if self._current_value < self._target_value:
            self._animation_job = self.after(30, self._animate_step)

    def update_progress(self, value, message):
        value = max(0, min(100, value))
        self._target_value = value

        if value < self._current_value:
            self._cancel_animation()
            self._current_value = value
            self.progress.set(value / 100)
            self.percent.configure(text=f"{value}%")
        else:
            self._start_animation()

        self.stage.configure(text=f"Current Stage: {message}")
        self.status.configure(text=message)
        self.estimate.configure(text=self._estimate_message(value))
        self.update_idletasks()

    def reset(self):
        self._cancel_animation()
        self._current_value = 0
        self._target_value = 0
        self.progress.set(0)
        self.percent.configure(text="0%")
        self.stage.configure(text="Current Stage: Waiting...")
        self.status.configure(text="Waiting...")
        self.estimate.configure(text="Estimated completion: Waiting to start")
