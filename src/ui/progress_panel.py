import customtkinter as ctk


class ProgressPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="#111827",
            corner_radius=15
        )

        title = ctk.CTkLabel(
            self,
            text="Encryption Progress",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 8))

        self.progress = ctk.CTkProgressBar(
            self,
            height=18
        )
        self.progress.pack(fill="x", padx=20)

        self.progress.set(0)

        self.percent = ctk.CTkLabel(
            self,
            text="0%",
            font=("Segoe UI", 14)
        )
        self.percent.pack(anchor="e", padx=20, pady=(5, 10))

        self.status = ctk.CTkLabel(
            self,
            text="Waiting...",
            font=("Segoe UI", 14),
            text_color="#94A3B8"
        )
        self.status.pack(anchor="w", padx=20, pady=(0, 15))

    def update_progress(self, value, message):

        value = max(0, min(100, value))

        self.progress.set(value / 100)

        self.percent.configure(
            text=f"{value}%"
        )

        self.status.configure(
            text=message
        )

        self.update_idletasks()

    def reset(self):

        self.update_progress(
            0,
            "Waiting..."
        )