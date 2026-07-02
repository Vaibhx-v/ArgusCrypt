import customtkinter as ctk


class StatusPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="#111827",
            corner_radius=15
        )

        title = ctk.CTkLabel(
            self,
            text="System Status",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 15))

        self.state = ctk.CTkLabel(
            self,
            text="🟢 Ready",
            font=("Segoe UI", 16, "bold"),
            text_color="#22C55E"
        )
        self.state.pack(anchor="w", padx=20)

        self.file = ctk.CTkLabel(
            self,
            text="Current File : None",
            font=("Segoe UI", 14)
        )
        self.file.pack(anchor="w", padx=20, pady=5)

        self.operation = ctk.CTkLabel(
            self,
            text="Operation : Waiting",
            font=("Segoe UI", 14)
        )
        self.operation.pack(anchor="w", padx=20, pady=5)

        self.algorithm = ctk.CTkLabel(
            self,
            text="Algorithm : AES-256-GCM",
            font=("Segoe UI", 14)
        )
        self.algorithm.pack(anchor="w", padx=20, pady=5)

        self.version = ctk.CTkLabel(
            self,
            text="Version : ArgusCrypt v1.1",
            font=("Segoe UI", 14)
        )
        self.version.pack(anchor="w", padx=20, pady=(5,20))

    def ready(self):
        self.state.configure(
            text="🟢 Ready",
            text_color="#22C55E"
        )
        self.operation.configure(
            text="Operation : Waiting"
        )

    def encrypting(self):
        self.state.configure(
            text="🟡 Encrypting...",
            text_color="#FACC15"
        )
        self.operation.configure(
            text="Operation : Encryption"
        )

    def decrypting(self):
        self.state.configure(
            text="🟡 Decrypting...",
            text_color="#FACC15"
        )
        self.operation.configure(
            text="Operation : Decryption"
        )

    def success(self):
        self.state.configure(
            text="🟢 Completed",
            text_color="#22C55E"
        )

    def failed(self):
        self.state.configure(
            text="🔴 Failed",
            text_color="#EF4444"
        )

    def update_file(self, filename):
        self.file.configure(
            text=f"Current File : {filename}"
        )