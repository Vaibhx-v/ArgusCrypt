import os
import threading

import customtkinter as ctk

from tkinter import filedialog, messagebox

from PIL import Image

from crypto_engine import encrypt_file, decrypt_file

from ui.progress_panel import ProgressPanel
from ui.activity_panel import ActivityPanel
from ui.status_panel import StatusPanel
from ui.operation_controller import OperationController


class ArgusCryptApp:

    def __init__(self):

        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()

        self.root.title("🔒 ArgusCrypt")

        self.root.geometry("1450x920")

        self.root.minsize(1300, 850)

        self.root.configure(
            fg_color="#0B1120"
        )

        self.selected_file = None

        self.preview_image = None

        self.current_mode = "encrypt"

        self.build_ui()

    # ==========================================================
    # BUILD UI
    # ==========================================================

    def build_ui(self):

        self.build_header()

        self.build_main_window()
         
        # ==========================================================
    # HEADER
    # ==========================================================

    def build_header(self):

        header = ctk.CTkFrame(
            self.root,
            height=80,
            fg_color="#111827",
            corner_radius=0
        )

        header.pack(fill="x")

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            padx=25,
            pady=15
        )

        title = ctk.CTkLabel(
            left,
            text="🔒 ArgusCrypt",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            left,
            text="Advanced Image Encryption Suite",
            text_color="#94A3B8",
            font=("Segoe UI", 14)
        )

        subtitle.pack(anchor="w")

        self.header_status = ctk.CTkLabel(
            header,
            text="🟢 System Ready",
            text_color="#22C55E",
            font=("Segoe UI", 15, "bold")
        )

        self.header_status.pack(
            side="right",
            padx=25
        )

    # ==========================================================
    # MAIN WINDOW
    # ==========================================================

    def build_main_window(self):

        self.body = ctk.CTkScrollableFrame(
            self.root,
            fg_color="#0B1120"
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.build_upload_section()

        self.build_information_cards()

        self.build_password_section()

        self.build_dashboard()

    # ==========================================================
    # UPLOAD SECTION
    # ==========================================================

    def build_upload_section(self):

        upload = ctk.CTkFrame(
            self.body,
            fg_color="#111827",
            corner_radius=18
        )

        upload.pack(
            fill="x",
            pady=(0, 20)
        )

        self.preview = ctk.CTkLabel(
            upload,
            text="🖼",
            font=("Segoe UI Emoji", 72)
        )

        self.preview.pack(
            pady=(25, 10)
        )

        self.preview_title = ctk.CTkLabel(
            upload,
            text="No File Selected",
            font=("Segoe UI", 22, "bold")
        )

        self.preview_title.pack()

        button_frame = ctk.CTkFrame(
            upload,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        self.image_button = ctk.CTkButton(
            button_frame,
            text="📁 Browse Image",
            width=180,
            command=self.select_image
        )

        self.image_button.pack(
            side="left",
            padx=10
        )

        self.enc_button = ctk.CTkButton(
            button_frame,
            text="📂 Browse .enc",
            width=180,
            command=self.select_enc
        )

        self.enc_button.pack(
            side="left",
            padx=10
        )

        self.selected_file_label = ctk.CTkLabel(
            upload,
            text="Waiting for file...",
            text_color="#94A3B8"
        )

        self.selected_file_label.pack(
            pady=(0, 20)
        )

         # ==========================================================
    # INFORMATION CARDS
    # ==========================================================

    def build_information_cards(self):

        cards = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        cards.pack(
            fill="x",
            pady=(0,20)
        )

        # --------------------------------------------------
        # File Information Card
        # --------------------------------------------------

        file_card = ctk.CTkFrame(
            cards,
            fg_color="#111827",
            corner_radius=18,
            width=650,
            height=220
        )

        file_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,10)
        )

        ctk.CTkLabel(
            file_card,
            text="📄 File Information",
            font=("Segoe UI",20,"bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15,10)
        )

        self.file_name = ctk.CTkLabel(
            file_card,
            text="Name : -",
            font=("Segoe UI",15)
        )

        self.file_name.pack(anchor="w", padx=25, pady=3)

        self.file_size = ctk.CTkLabel(
            file_card,
            text="Size : -",
            font=("Segoe UI",15)
        )

        self.file_size.pack(anchor="w", padx=25, pady=3)

        self.file_resolution = ctk.CTkLabel(
            file_card,
            text="Resolution : -",
            font=("Segoe UI",15)
        )

        self.file_resolution.pack(anchor="w", padx=25, pady=3)

        self.file_format = ctk.CTkLabel(
            file_card,
            text="Format : -",
            font=("Segoe UI",15)
        )

        self.file_format.pack(anchor="w", padx=25, pady=3)

        # --------------------------------------------------
        # Security Card
        # --------------------------------------------------

        security_card = ctk.CTkFrame(
            cards,
            fg_color="#111827",
            corner_radius=18,
            width=650,
            height=220
        )

        security_card.pack(
            side="left",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            security_card,
            text="🔐 Security Information",
            font=("Segoe UI",20,"bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15,10)
        )

        self.algorithm_label = ctk.CTkLabel(
            security_card,
            text="Algorithm : AES-256-GCM",
            font=("Segoe UI",15)
        )

        self.algorithm_label.pack(anchor="w", padx=25, pady=3)

        self.kdf_label = ctk.CTkLabel(
            security_card,
            text="KDF : PBKDF2-HMAC-SHA256",
            font=("Segoe UI",15)
        )

        self.kdf_label.pack(anchor="w", padx=25, pady=3)

        self.salt_label = ctk.CTkLabel(
            security_card,
            text="Salt : Generated Automatically",
            font=("Segoe UI",15)
        )

        self.salt_label.pack(anchor="w", padx=25, pady=3)

        self.integrity_label = ctk.CTkLabel(
            security_card,
            text="Integrity : AES-GCM Authentication",
            font=("Segoe UI",15)
        )

        self.integrity_label.pack(anchor="w", padx=25, pady=3)

        self.version_label = ctk.CTkLabel(
            security_card,
            text="Engine : ArgusCrypt v1.1",
            font=("Segoe UI",15)
        )

        self.version_label.pack(anchor="w", padx=25, pady=3)

        # ==========================================================
    # PASSWORD SECTION
    # ==========================================================

    def build_password_section(self):

        password_card = ctk.CTkFrame(
            self.body,
            fg_color="#111827",
            corner_radius=18
        )

        password_card.pack(
            fill="x",
            pady=(0,20)
        )

        # ---------------- Password ---------------- #

        ctk.CTkLabel(
            password_card,
            text="Password",
            font=("Segoe UI",18,"bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,5)
        )

        self.password_entry = ctk.CTkEntry(
            password_card,
            height=45,
            show="*",
            placeholder_text="Enter Password"
        )

        self.password_entry.pack(
            fill="x",
            padx=20
        )

        # ---------------- Confirm Password ---------------- #

        ctk.CTkLabel(
            password_card,
            text="Confirm Password",
            font=("Segoe UI",18,"bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,5)
        )

        self.confirm_entry = ctk.CTkEntry(
            password_card,
            height=45,
            show="*",
            placeholder_text="Confirm Password"
        )

        self.confirm_entry.pack(
            fill="x",
            padx=20
        )

        # ---------------- Password Strength ---------------- #

        ctk.CTkLabel(
            password_card,
            text="Password Strength",
            font=("Segoe UI",16)
        ).pack(
            anchor="w",
            padx=20,
            pady=(20,5)
        )

        self.password_strength = ctk.CTkProgressBar(
            password_card,
            height=12
        )

        self.password_strength.pack(
            fill="x",
            padx=20
        )

        self.password_strength.set(0)

        self.password_strength_label = ctk.CTkLabel(
            password_card,
            text="Weak",
            text_color="#EF4444"
        )

        self.password_strength_label.pack(
            anchor="w",
            padx=20,
            pady=(5,20)
        )

        # ---------------- Buttons ---------------- #

        button_frame = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=(0,20)
        )

        self.encrypt_button = ctk.CTkButton(
            button_frame,
            text="🔒 Encrypt Image",
            width=220,
            height=48,
            corner_radius=12,
            command=self.encrypt_clicked
        )

        self.encrypt_button.pack(
            side="left",
            padx=15
        )

        self.decrypt_button = ctk.CTkButton(
            button_frame,
            text="🔓 Decrypt File",
            width=220,
            height=48,
            corner_radius=12,
            command=self.decrypt_clicked
        )

        self.decrypt_button.pack(
            side="left",
            padx=15
        )

        # ==========================================================
    # DASHBOARD
    # ==========================================================

    def build_dashboard(self):

        dashboard = ctk.CTkFrame(
            self.body,
            fg_color="transparent"
        )

        dashboard.pack(
            fill="both",
            expand=True,
            pady=(0,20)
        )

        # Left Column
        left = ctk.CTkFrame(
            dashboard,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,10)
        )

        # Right Column
        right = ctk.CTkFrame(
            dashboard,
            fg_color="transparent",
            width=350
        )

        right.pack(
            side="left",
            fill="y"
        )

        # --------------------------------------------------
        # Progress Panel
        # --------------------------------------------------

        self.progress_panel = ProgressPanel(left)

        self.progress_panel.pack(
            fill="x",
            pady=(0,15)
        )

        # --------------------------------------------------
        # Activity Panel
        # --------------------------------------------------

        self.activity_panel = ActivityPanel(left)

        self.activity_panel.pack(
            fill="both",
            expand=True
        )

        # --------------------------------------------------
        # Status Panel
        # --------------------------------------------------

        self.status_panel = StatusPanel(right)

        self.status_panel.pack(
            fill="both",
            expand=True
        )

        # --------------------------------------------------
        # Controller
        # --------------------------------------------------

        self.controller = OperationController(

            self.progress_panel,

            self.activity_panel,

            self.status_panel

        )

         # ==========================================================
    # IMAGE SELECTION
    # ==========================================================

    def select_image(self):

        file = filedialog.askopenfilename(

            title="Select Image",

            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")
            ]
        )

        if not file:
            return

        self.current_mode = "encrypt"

        self.selected_file = file

        self.load_image_preview(file)

        self.load_file_information(file)

        self.header_status.configure(
            text="🟢 Image Selected",
            text_color="#22C55E"
        )

        self.activity_panel.log("Image Selected")

        self.status_panel.ready()

        self.status_panel.update_file(
            os.path.basename(file)
        )

    # ==========================================================
    # ENCRYPTED FILE SELECTION
    # ==========================================================

    def select_enc(self):

        file = filedialog.askopenfilename(

            title="Select Encrypted File",

            filetypes=[
                ("Encrypted Files", "*.enc")
            ]
        )

        if not file:
            return

        self.current_mode = "decrypt"

        self.selected_file = file

        self.preview.configure(
            image=None,
            text="🔒",
            font=("Segoe UI Emoji",72)
        )

        self.preview_title.configure(
            text=os.path.basename(file)
        )

        self.selected_file_label.configure(
            text=file
        )

        size = os.path.getsize(file)

        self.file_name.configure(
            text=f"Name : {os.path.basename(file)}"
        )

        self.file_size.configure(
            text=f"Size : {round(size/1024,2)} KB"
        )

        self.file_resolution.configure(
            text="Resolution : Encrypted File"
        )

        self.file_format.configure(
            text="Format : ARGUSCRYPT (.enc)"
        )

        self.header_status.configure(
            text="🟢 Encrypted File Selected",
            text_color="#22C55E"
        )

        self.activity_panel.log(
            "Encrypted File Selected"
        )

        self.status_panel.ready()

        self.status_panel.update_file(
            os.path.basename(file)
        )

    # ==========================================================
    # IMAGE PREVIEW
    # ==========================================================

    def load_image_preview(self, file):

        image = Image.open(file)

        preview = image.copy()

        preview.thumbnail((250,250))

        self.preview_image = ctk.CTkImage(

            light_image=preview,

            dark_image=preview,

            size=preview.size

        )

        self.preview.configure(

            image=self.preview_image,

            text=""

        )

        self.preview_title.configure(

            text=os.path.basename(file)

        )

        self.selected_file_label.configure(

            text=file

        )

    # ==========================================================
    # FILE INFORMATION
    # ==========================================================

    def load_file_information(self, file):

        image = Image.open(file)

        width, height = image.size

        size = os.path.getsize(file)

        extension = os.path.splitext(file)[1].upper()

        self.file_name.configure(

            text=f"Name : {os.path.basename(file)}"

        )

        self.file_size.configure(

            text=f"Size : {round(size/1024,2)} KB"

        )

        self.file_resolution.configure(

            text=f"Resolution : {width} × {height}"

        )

        self.file_format.configure(

            text=f"Format : {extension}"

        )

        # ==========================================================
    # ENCRYPT BUTTON
    # ==========================================================

    def encrypt_clicked(self):

        if self.selected_file is None:

            messagebox.showerror(
                "ArgusCrypt",
                "Please select an image."
            )

            return

        if self.current_mode != "encrypt":

            messagebox.showerror(
                "ArgusCrypt",
                "Please select an image, not an encrypted file."
            )

            return

        password = self.password_entry.get()

        confirm = self.confirm_entry.get()

        if password == "":

            messagebox.showerror(
                "ArgusCrypt",
                "Password cannot be empty."
            )

            return

        if password != confirm:

            messagebox.showerror(
                "ArgusCrypt",
                "Passwords do not match."
            )

            return

        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")

        threading.Thread(
            target=self.perform_encryption,
            daemon=True
        ).start()

    # ==========================================================
    # PERFORM ENCRYPTION
    # ==========================================================

    def perform_encryption(self):

        try:

            filename = os.path.basename(self.selected_file)

            self.controller.start_encryption(filename)

            self.root.after(
                0,
                lambda: self.controller.validate_password()
            )

            self.root.after(
                200,
                lambda: self.controller.generate_salt()
            )

            self.root.after(
                400,
                lambda: self.controller.derive_key()
            )

            self.root.after(
                600,
                lambda: self.controller.encrypting()
            )

            result = encrypt_file(

                self.selected_file,

                self.password_entry.get()

            )

            self.root.after(
                900,
                lambda: self.controller.saving()
            )

            self.root.after(
                1200,
                lambda: self.controller.success()
            )

            self.root.after(
                1300,
                lambda: messagebox.showinfo(
                    "ArgusCrypt",
                    f"Encryption Successful!\n\nSaved To:\n{result['output_file']}"
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.controller.failed(str(e))
            )

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "ArgusCrypt",
                    str(e)
                )
            )

        finally:

            self.root.after(
                0,
                lambda: self.encrypt_button.configure(state="normal")
            )

            self.root.after(
                0,
                lambda: self.decrypt_button.configure(state="normal")
            )

    # ==========================================================
    # DECRYPT BUTTON
    # ==========================================================

    def decrypt_clicked(self):

        if self.selected_file is None:

            messagebox.showerror(
                "ArgusCrypt",
                "Please select an encrypted file."
            )

            return

        if self.current_mode != "decrypt":

            messagebox.showerror(
                "ArgusCrypt",
                "Please select a .enc file."
            )

            return

        password = self.password_entry.get()

        if password == "":

            messagebox.showerror(
                "ArgusCrypt",
                "Password cannot be empty."
            )

            return

        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")

        threading.Thread(
            target=self.perform_decryption,
            daemon=True
        ).start()

    # ==========================================================
    # PERFORM DECRYPTION
    # ==========================================================

    def perform_decryption(self):

        try:

            filename = os.path.basename(self.selected_file)

            self.controller.start_decryption(filename)

            self.root.after(
                0,
                lambda: self.controller.validate_password()
            )

            self.root.after(
                250,
                lambda: self.controller.decrypting()
            )

            result = decrypt_file(

                self.selected_file,

                self.password_entry.get()

            )

            self.root.after(
                900,
                lambda: self.controller.restoring()
            )

            self.root.after(
                1200,
                lambda: self.controller.decryption_success()
            )

            self.root.after(
                1300,
                lambda: messagebox.showinfo(
                    "ArgusCrypt",
                    f"Decryption Successful!\n\nSaved To:\n{result['output_file']}"
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.controller.failed(str(e))
            )

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "ArgusCrypt",
                    str(e)
                )
            )

        finally:

            self.root.after(
                0,
                lambda: self.encrypt_button.configure(state="normal")
            )

            self.root.after(
                0,
                lambda: self.decrypt_button.configure(state="normal")
            )                  
            # ==========================================================
    # PASSWORD STRENGTH
    # ==========================================================

    def update_password_strength(self, event=None):

        password = self.password_entry.get()

        score = 0

        if len(password) >= 8:
            score += 25

        if any(c.isupper() for c in password):
            score += 20

        if any(c.islower() for c in password):
            score += 20

        if any(c.isdigit() for c in password):
            score += 20

        if any(not c.isalnum() for c in password):
            score += 15

        value = score / 100

        self.password_strength.set(value)

        if score < 40:

            self.password_strength_label.configure(
                text="Weak",
                text_color="#EF4444"
            )

        elif score < 70:

            self.password_strength_label.configure(
                text="Medium",
                text_color="#F59E0B"
            )

        else:

            self.password_strength_label.configure(
                text="Strong",
                text_color="#22C55E"

            )

    # ==========================================================
    # RESET GUI
    # ==========================================================

    def reset_interface(self):

        self.password_entry.delete(0, "end")

        self.confirm_entry.delete(0, "end")

        self.password_strength.set(0)

        self.password_strength_label.configure(

            text="Weak",

            text_color="#EF4444"

        )

        self.controller.progress.reset()

        self.controller.activity.clear()

        self.controller.status.ready()

    # ==========================================================
    # EVENTS
    # ==========================================================

    def bind_events(self):

        self.password_entry.bind(

            "<KeyRelease>",

            self.update_password_strength

        )

    # ==========================================================
    # RUN
    # ==========================================================

    def run(self):

        self.bind_events()

        self.root.mainloop()


# ==========================================================
# APPLICATION ENTRY
# ==========================================================

if __name__ == "__main__":

    app = ArgusCryptApp()

    app.run()    