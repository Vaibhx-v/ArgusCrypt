import customtkinter as ctk

from ui.constant import ALGORITHM, APP_NAME, APP_VERSION
from ui.styles import PanelCard, panel_title
from ui.theme import *


class StatusPanel(PanelCard):

    def __init__(self, master):
        super().__init__(master)

        panel_title(self, "System Status").pack(
            anchor="w",
            padx=LARGE_PADDING,
            pady=(LARGE_PADDING, SMALL_PADDING),
        )

        self.state = ctk.CTkLabel(
            self,
            text="🟢 Ready",
            font=("Segoe UI", 16, "bold"),
            text_color=SUCCESS,
        )
        self.state.pack(anchor="w", padx=LARGE_PADDING)

        self.file = ctk.CTkLabel(
            self,
            text="Current File : None",
            font=LABEL_FONT,
            text_color=TEXT,
        )
        self.file.pack(anchor="w", padx=LARGE_PADDING, pady=5)

        self.operation = ctk.CTkLabel(
            self,
            text="Operation : Waiting",
            font=LABEL_FONT,
            text_color=TEXT,
        )
        self.operation.pack(anchor="w", padx=LARGE_PADDING, pady=5)

        self.algorithm = ctk.CTkLabel(
            self,
            text=f"Algorithm : {ALGORITHM}",
            font=LABEL_FONT,
            text_color=TEXT,
        )
        self.algorithm.pack(anchor="w", padx=LARGE_PADDING, pady=5)

        self.version = ctk.CTkLabel(
            self,
            text=f"Version : {APP_NAME} v{APP_VERSION}",
            font=LABEL_FONT,
            text_color=TEXT,
        )
        self.version.pack(anchor="w", padx=LARGE_PADDING, pady=(5, LARGE_PADDING))

    def ready(self):
        self.state.configure(text="🟢 Ready", text_color=SUCCESS)
        self.operation.configure(text="Operation : Waiting")

    def encrypting(self):
        self.state.configure(text="🟡 Encrypting...", text_color=WARNING)
        self.operation.configure(text="Operation : Encryption")

    def decrypting(self):
        self.state.configure(text="🟡 Decrypting...", text_color=WARNING)
        self.operation.configure(text="Operation : Decryption")

    def success(self):
        self.state.configure(text="🟢 Completed", text_color=SUCCESS)

    def failed(self):
        self.state.configure(text="🔴 Failed", text_color=ERROR)

    def update_file(self, filename):
        self.file.configure(text=f"Current File : {filename}")
