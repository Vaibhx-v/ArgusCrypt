import customtkinter as ctk


class ActivityPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="#111827",
            corner_radius=15
        )

        title = ctk.CTkLabel(
            self,
            text="Activity",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 10))

        self.textbox = ctk.CTkTextbox(
            self,
            height=250,
            font=("Consolas", 13),
            wrap="word"
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.textbox.insert(
            "end",
            "ArgusCrypt Ready...\n"
        )

        self.textbox.configure(
            state="disabled"
        )

    def log(self, message):

        self.textbox.configure(
            state="normal"
        )

        self.textbox.insert(
            "end",
            f"✔ {message}\n"
        )

        self.textbox.see("end")

        self.textbox.configure(
            state="disabled"
        )

    def error(self, message):

        self.textbox.configure(
            state="normal"
        )

        self.textbox.insert(
            "end",
            f"❌ {message}\n"
        )

        self.textbox.see("end")

        self.textbox.configure(
            state="disabled"
        )

    def clear(self):

        self.textbox.configure(
            state="normal"
        )

        self.textbox.delete(
            "1.0",
            "end"
        )

        self.textbox.insert(
            "end",
            "ArgusCrypt Ready...\n"
        )

        self.textbox.configure(
            state="disabled"
        )