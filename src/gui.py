import hashlib
import os
import secrets
import string
import threading
from datetime import datetime

import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

from crypto_engine import decrypt_file, encrypt_file
from ui.activity_panel import ActivityPanel
from ui.constant import (
    ALGORITHM,
    APP_NAME,
    APP_VERSION,
    AUTHENTICATION,
    KDF_ALGORITHM,
    KEY_SIZE_BITS,
    NONCE_BITS,
    PASSWORD_LENGTH,
    SALT_BITS,
    WINDOW_TITLE,
)
from ui.layout import LAYOUT
from ui.operation_controller import OperationController
from ui.progress_panel import ProgressPanel
from ui.status_panel import StatusPanel
from ui import styles
from ui.theme import *


class ArgusCryptApp:
    PREVIEW_SIZE = (420, 420)
    PREVIEW_PLACEHOLDER = ("Segoe UI Emoji", 96)
    PASSWORD_SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"

    FILE_INFO_ROWS = (
        ("filename", "Filename : -"),
        ("resolution", "Resolution : -"),
        ("image_format", "Image Format : -"),
        ("file_size", "File Size : -"),
        ("absolute_path", "Absolute Path : -"),
        ("last_modified", "Last Modified : -"),
        ("sha256_hash", "SHA-256 Hash : -"),
        ("color_mode", "Image Color Mode : -"),
    )

    SECURITY_INFO_ROWS = (
        ("algorithm_label", f"Algorithm : {ALGORITHM}"),
        ("key_size_label", f"Key Size : {KEY_SIZE_BITS} bits"),
        ("nonce_label", f"Nonce : {NONCE_BITS} bits"),
        ("salt_label", f"Salt : {SALT_BITS} bits"),
        ("auth_label", f"Authentication : {AUTHENTICATION}"),
        ("kdf_label", f"KDF : {KDF_ALGORITHM}"),
        ("version_label", f"Engine Version : {APP_NAME} v{APP_VERSION}"),
    )

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1200, 820)
        self.root.configure(fg_color=WINDOW_BG)

        self.selected_file = None
        self.preview_image = None
        self.current_mode = "encrypt"
        self.last_output_path = None
        self._password_visible = False
        self._confirm_visible = False

        self._build_ui()

    def _build_ui(self):
        self._build_header()
        self._build_main_layout()

    def _build_header(self):
        header = ctk.CTkFrame(
            self.root,
            height=LAYOUT["header"]["height"],
            fg_color=HEADER_BG,
            corner_radius=0,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = styles.transparent_frame(header)
        brand.pack(side="left", padx=LARGE_PADDING, pady=SMALL_PADDING)

        ctk.CTkLabel(
            brand,
            text=f"🔒 {APP_NAME}",
            font=TITLE_FONT,
            text_color=TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="Advanced Image Encryption Suite",
            font=SUBTITLE_FONT,
            text_color=SECONDARY_TEXT,
        ).pack(anchor="w", pady=(2, 0))

        self.header_status = styles.status_badge(
            header,
            text="🟢 System Ready",
            color=SUCCESS,
        )
        self.header_status.pack(side="right", padx=LARGE_PADDING)

    def _build_main_layout(self):
        self.body = ctk.CTkScrollableFrame(
            self.root,
            fg_color=WINDOW_BG,
            scrollbar_button_color=CARD_BG,
            scrollbar_button_hover_color=CARD_HOVER,
        )
        self.body.pack(fill="both", expand=True, padx=PADDING, pady=PADDING)

        self.body.grid_columnconfigure(0, weight=3, uniform="columns")
        self.body.grid_columnconfigure(1, weight=2, uniform="columns")

        left_column = styles.transparent_frame(self.body)
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PADDING))

        right_column = styles.transparent_frame(self.body)
        right_column.grid(row=0, column=1, sticky="nsew", padx=(SMALL_PADDING, 0))

        self._build_preview_section(left_column)
        self._build_information_cards(left_column)
        self._build_password_section(right_column)
        self._build_action_buttons(right_column)
        self._build_dashboard(right_column)

    def _build_preview_section(self, parent):
        preview_card = styles.card(parent)
        preview_card.pack(fill="x", pady=(0, PADDING))

        styles.card_header(preview_card, "Image Preview").pack(
            anchor="w",
            padx=LARGE_PADDING,
            pady=(LARGE_PADDING, SMALL_PADDING),
        )

        self.preview_frame = styles.card(
            preview_card,
            fg_color=WINDOW_BG,
            corner_radius=BUTTON_RADIUS,
        )
        self.preview_frame.pack(
            fill="x",
            padx=LARGE_PADDING,
            pady=(0, SMALL_PADDING),
        )

        preview_height = LAYOUT["preview"]["height"] + 120

        self.preview_container = styles.transparent_frame(self.preview_frame)
        self.preview_container.pack(
            fill="both",
            expand=True,
            padx=PADDING,
            pady=PADDING,
        )

        self.preview = ctk.CTkLabel(
            self.preview_container,
            text="🖼",
            font=self.PREVIEW_PLACEHOLDER,
            text_color=SECONDARY_TEXT,
            height=preview_height,
        )
        self.preview.pack(fill="both", expand=True)

        self.encrypted_placeholder = styles.transparent_frame(self.preview_container)

        ctk.CTkLabel(
            self.encrypted_placeholder,
            text="🔒",
            font=("Segoe UI Emoji", 72),
            text_color=PRIMARY,
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            self.encrypted_placeholder,
            text="Encrypted File",
            font=("Segoe UI", 24, "bold"),
            text_color=TEXT,
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            self.encrypted_placeholder,
            text="Preview not available",
            font=LABEL_FONT,
            text_color=SECONDARY_TEXT,
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            self.encrypted_placeholder,
            text=f"{ALGORITHM} Protected",
            font=("Segoe UI", 14, "bold"),
            text_color=SUCCESS,
        ).pack(pady=(0, 30))

        self.preview_title = ctk.CTkLabel(
            preview_card,
            text="No File Selected",
            font=("Segoe UI", 22, "bold"),
            text_color=TEXT,
        )
        self.preview_title.pack(pady=(SMALL_PADDING, 0))

        button_row = styles.transparent_frame(preview_card)
        button_row.pack(pady=LARGE_PADDING)

        self.image_button = styles.secondary_button(
            button_row,
            text="📁 Browse Image",
            command=self.select_image,
        )
        self.image_button.pack(side="left", padx=SMALL_PADDING)

        self.enc_button = styles.secondary_button(
            button_row,
            text="📂 Browse .enc",
            command=self.select_enc,
        )
        self.enc_button.pack(side="left", padx=SMALL_PADDING)

        self.selected_file_label = styles.body_text(
            preview_card,
            text="Waiting for file...",
        )
        self.selected_file_label.pack(pady=(0, LARGE_PADDING))

    def _build_information_cards(self, parent):
        cards_row = styles.transparent_frame(parent)
        cards_row.pack(fill="x", pady=(0, PADDING))
        cards_row.grid_columnconfigure(0, weight=1)
        cards_row.grid_columnconfigure(1, weight=1)

        file_card, file_labels = styles.build_info_card(
            cards_row,
            "📄 File Information",
            self.FILE_INFO_ROWS,
            mono_keys={"absolute_path", "sha256_hash"},
        )
        file_card.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PADDING))

        security_card, security_labels = styles.build_info_card(
            cards_row,
            "🔐 Security Information",
            self.SECURITY_INFO_ROWS,
        )
        security_card.grid(row=0, column=1, sticky="nsew", padx=(SMALL_PADDING, 0))

        self.filename_label = file_labels["filename"]
        self.resolution_label = file_labels["resolution"]
        self.image_format_label = file_labels["image_format"]
        self.file_size_label = file_labels["file_size"]
        self.absolute_path_label = file_labels["absolute_path"]
        self.last_modified_label = file_labels["last_modified"]
        self.sha256_hash_label = file_labels["sha256_hash"]
        self.color_mode_label = file_labels["color_mode"]

        self.algorithm_label = security_labels["algorithm_label"]
        self.key_size_label = security_labels["key_size_label"]
        self.nonce_label = security_labels["nonce_label"]
        self.salt_label = security_labels["salt_label"]
        self.auth_label = security_labels["auth_label"]
        self.kdf_label = security_labels["kdf_label"]
        self.version_label = security_labels["version_label"]

        self.file_name = self.filename_label
        self.file_size = self.file_size_label
        self.file_resolution = self.resolution_label
        self.file_format = self.image_format_label

    def _build_password_section(self, parent):
        password_card = styles.card(parent)
        password_card.pack(fill="x", pady=(0, PADDING))

        header = styles.transparent_frame(password_card)
        header.pack(fill="x", padx=LARGE_PADDING, pady=(LARGE_PADDING, SMALL_PADDING))

        styles.card_header(header, "🔑 Credential Security").pack(side="left")

        self.generate_password_button = styles.secondary_button(
            header,
            text="⚡ Generate Password",
            command=self.generate_password,
            width=ACTION_BUTTON_WIDTH,
        )
        self.generate_password_button.pack(side="right")

        form = styles.transparent_frame(password_card)
        form.pack(fill="x", padx=LARGE_PADDING, pady=(0, LARGE_PADDING))

        styles.section_label(form, "Password").pack(anchor="w", pady=(0, 6))
        _, self.password_entry, self.password_toggle = styles.password_field(
            form,
            placeholder="Enter Password",
            toggle_command=self.toggle_password_visibility,
        )
        self.password_entry.master.pack(fill="x", pady=(0, PADDING))

        styles.section_label(form, "Confirm Password").pack(anchor="w", pady=(0, 6))
        _, self.confirm_entry, self.confirm_toggle = styles.password_field(
            form,
            placeholder="Confirm Password",
            toggle_command=self.toggle_confirm_visibility,
        )
        self.confirm_entry.master.pack(fill="x", pady=(0, PADDING))

        strength_header = styles.transparent_frame(form)
        strength_header.pack(fill="x", pady=(0, 6))

        styles.section_label(strength_header, "Password Strength").pack(side="left")

        self.password_strength_label = styles.body_text(
            strength_header,
            text="Weak",
            color=ERROR,
        )
        self.password_strength_label.pack(side="right")

        self.password_strength = styles.progress_bar(form)
        self.password_strength.pack(fill="x")

    def _build_action_buttons(self, parent):
        button_row = styles.transparent_frame(parent)
        button_row.pack(fill="x", pady=(0, SMALL_PADDING))
        button_row.grid_columnconfigure(0, weight=1)
        button_row.grid_columnconfigure(1, weight=1)

        self.encrypt_button = styles.action_button(
            button_row,
            text="🔒 Encrypt Image",
            command=self.encrypt_clicked,
        )
        self.encrypt_button.grid(row=0, column=0, sticky="ew", padx=(0, SMALL_PADDING))

        self.decrypt_button = styles.action_button(
            button_row,
            text="🔓 Decrypt File",
            command=self.decrypt_clicked,
        )
        self.decrypt_button.grid(row=0, column=1, sticky="ew", padx=(SMALL_PADDING, 0))

        self.open_folder_button = styles.secondary_button(
            parent,
            text="📂 Open Output Folder",
            command=self.open_output_folder,
            width=ACTION_BUTTON_WIDTH * 2 + SMALL_PADDING,
        )
        self.open_folder_button.pack(pady=(0, PADDING))
        self.open_folder_button.configure(state="disabled")

    def _build_dashboard(self, parent):
        dashboard = styles.transparent_frame(parent)
        dashboard.pack(fill="both", expand=True)
        dashboard.grid_columnconfigure(0, weight=3)
        dashboard.grid_columnconfigure(1, weight=2)

        left_panel = styles.transparent_frame(dashboard)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, SMALL_PADDING))

        right_panel = styles.transparent_frame(dashboard)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(SMALL_PADDING, 0))
        right_panel.configure(width=LAYOUT["dashboard"]["status_width"])

        self.progress_panel = ProgressPanel(left_panel)
        self.progress_panel.pack(fill="x", pady=(0, PADDING))

        self.activity_panel = ActivityPanel(left_panel)
        self.activity_panel.pack(fill="both", expand=True)

        self.status_panel = StatusPanel(right_panel)
        self.status_panel.pack(fill="both", expand=True)

        self.controller = OperationController(
            self.progress_panel,
            self.activity_panel,
            self.status_panel,
        )

    @staticmethod
    def _format_file_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{round(size_bytes / 1024, 2)} KB"
        return f"{round(size_bytes / (1024 * 1024), 2)} MB"

    @staticmethod
    def _compute_sha256(file_path):
        digest = hashlib.sha256()
        with open(file_path, "rb") as handle:
            for chunk in iter(lambda: handle.read(8192), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _set_header_status(self, text, color=SUCCESS):
        self.header_status.configure(text=text, text_color=color)

    def _set_output_folder_enabled(self, output_path):
        self.last_output_path = output_path
        self.open_folder_button.configure(state="normal")

    def show_encrypted_placeholder(self):
        self.preview_image = None
        self.preview.configure(image=None)
        self.preview.pack_forget()
        self.encrypted_placeholder.pack(fill="both", expand=True)

    def _show_image_preview_widget(self):
        self.encrypted_placeholder.pack_forget()
        self.preview.pack(fill="both", expand=True)

    def _reset_preview_to_default(self):
        self.preview_image = None
        self.preview.configure(image=None, text="🖼", font=self.PREVIEW_PLACEHOLDER)
        self._show_image_preview_widget()

    def toggle_password_visibility(self):
        self._password_visible = not self._password_visible
        self.password_entry.configure(show="" if self._password_visible else "*")
        self.password_toggle.configure(
            text="🙈" if self._password_visible else "👁"
        )

    def toggle_confirm_visibility(self):
        self._confirm_visible = not self._confirm_visible
        self.confirm_entry.configure(show="" if self._confirm_visible else "*")
        self.confirm_toggle.configure(
            text="🙈" if self._confirm_visible else "👁"
        )

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + self.PASSWORD_SYMBOLS
        required = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
            secrets.choice(self.PASSWORD_SYMBOLS),
        ]
        remaining = [
            secrets.choice(alphabet)
            for _ in range(PASSWORD_LENGTH - len(required))
        ]
        password_chars = required + remaining
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.confirm_entry.insert(0, password)
        self.update_password_strength()

    def open_output_folder(self):
        if not self.last_output_path:
            return

        folder = os.path.dirname(os.path.abspath(self.last_output_path))
        if not os.path.isdir(folder):
            messagebox.showerror(APP_NAME, "Output folder not found.")
            return

        os.startfile(folder)

    def select_image(self):
        file = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")],
        )
        if not file:
            return

        self.current_mode = "encrypt"
        self.selected_file = file
        self.load_image_preview(file)
        self.load_file_information(file)
        self._set_header_status("🟢 Image Selected")
        self.activity_panel.log("Image Selected")
        self.status_panel.ready()
        self.status_panel.update_file(os.path.basename(file))

    def select_enc(self):
        file = filedialog.askopenfilename(
            title="Select Encrypted File",
            filetypes=[("Encrypted Files", "*.enc")],
        )
        if not file:
            return

        self.current_mode = "decrypt"
        self.selected_file = file

        self.show_encrypted_placeholder()
        self.preview_title.configure(text=os.path.basename(file))
        self.selected_file_label.configure(text=file)
        self.load_encrypted_file_information(file)

        self._set_header_status("🟢 Encrypted File Selected")
        self.activity_panel.log("Encrypted File Selected")
        self.status_panel.ready()
        self.status_panel.update_file(os.path.basename(file))

    def load_image_preview(self, file):
        image = Image.open(file)
        preview = image.copy()
        preview.thumbnail(self.PREVIEW_SIZE)

        self.preview_image = ctk.CTkImage(
            light_image=preview,
            dark_image=preview,
            size=preview.size,
        )

        self._show_image_preview_widget()
        self.preview.configure(image=self.preview_image, text="")
        self.preview_title.configure(text=os.path.basename(file))
        self.selected_file_label.configure(text=file)

    def load_file_information(self, file):
        image = Image.open(file)
        width, height = image.size
        size = os.path.getsize(file)
        extension = os.path.splitext(file)[1].upper().lstrip(".") or "UNKNOWN"
        modified = datetime.fromtimestamp(os.path.getmtime(file)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        file_hash = self._compute_sha256(file)

        self.filename_label.configure(text=f"Filename : {os.path.basename(file)}")
        self.resolution_label.configure(text=f"Resolution : {width} × {height}")
        self.image_format_label.configure(text=f"Image Format : {extension}")
        self.file_size_label.configure(text=f"File Size : {self._format_file_size(size)}")
        self.absolute_path_label.configure(text=f"Absolute Path : {os.path.abspath(file)}")
        self.last_modified_label.configure(text=f"Last Modified : {modified}")
        self.sha256_hash_label.configure(text=f"SHA-256 Hash : {file_hash}")
        self.color_mode_label.configure(text=f"Image Color Mode : {image.mode}")

    def load_encrypted_file_information(self, file):
        size = os.path.getsize(file)
        file_hash = self._compute_sha256(file)

        self.filename_label.configure(text=f"Encrypted File : {os.path.basename(file)}")
        self.resolution_label.configure(text="Unknown Resolution")
        self.image_format_label.configure(text="Image Format : ARGUSCRYPT (.enc)")
        self.file_size_label.configure(text=f"Encrypted Size : {self._format_file_size(size)}")
        self.absolute_path_label.configure(text=f"Absolute Path : {os.path.abspath(file)}")
        self.last_modified_label.configure(
            text=f"Last Modified : {datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.sha256_hash_label.configure(text=f"SHA-256 Hash : {file_hash}")
        self.color_mode_label.configure(text="Image Color Mode : N/A")

    def encrypt_clicked(self):
        if self.selected_file is None:
            messagebox.showerror(APP_NAME, "Please select an image.")
            return

        if self.current_mode != "encrypt":
            messagebox.showerror(APP_NAME, "Please select an image, not an encrypted file.")
            return

        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if password == "":
            messagebox.showerror(APP_NAME, "Password cannot be empty.")
            return

        if password != confirm:
            messagebox.showerror(APP_NAME, "Passwords do not match.")
            return

        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")
        self.open_folder_button.configure(state="disabled")

        threading.Thread(target=self.perform_encryption, daemon=True).start()

    def perform_encryption(self):
        try:
            filename = os.path.basename(self.selected_file)

            self.controller.start_encryption(filename)

            self.root.after(0, lambda: self.controller.validate_password())
            self.root.after(200, lambda: self.controller.generate_salt())
            self.root.after(400, lambda: self.controller.derive_key())
            self.root.after(600, lambda: self.controller.encrypting())

            result = encrypt_file(self.selected_file, self.password_entry.get())

            self.root.after(900, lambda: self.controller.saving())
            self.root.after(1200, lambda: self.controller.success())
            self.root.after(
                0,
                lambda: self._set_output_folder_enabled(result["output_file"]),
            )
            self.root.after(
                1300,
                lambda: messagebox.showinfo(
                    APP_NAME,
                    f"Encryption Successful!\n\nSaved To:\n{result['output_file']}",
                ),
            )

        except Exception as e:
            self.root.after(0, lambda: self.controller.failed(str(e)))
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))

        finally:
            self.root.after(0, lambda: self.encrypt_button.configure(state="normal"))
            self.root.after(0, lambda: self.decrypt_button.configure(state="normal"))

    def decrypt_clicked(self):
        if self.selected_file is None:
            messagebox.showerror(APP_NAME, "Please select an encrypted file.")
            return

        if self.current_mode != "decrypt":
            messagebox.showerror(APP_NAME, "Please select a .enc file.")
            return

        password = self.password_entry.get()
        if password == "":
            messagebox.showerror(APP_NAME, "Password cannot be empty.")
            return

        self.encrypt_button.configure(state="disabled")
        self.decrypt_button.configure(state="disabled")
        self.open_folder_button.configure(state="disabled")

        threading.Thread(target=self.perform_decryption, daemon=True).start()

    def perform_decryption(self):
        try:
            filename = os.path.basename(self.selected_file)

            self.controller.start_decryption(filename)

            self.root.after(0, lambda: self.controller.validate_password())
            self.root.after(250, lambda: self.controller.decrypting())

            result = decrypt_file(self.selected_file, self.password_entry.get())

            if not result.get("success", True):
                raise ValueError(result.get("message", "Decryption failed."))

            self.root.after(900, lambda: self.controller.restoring())
            self.root.after(1200, lambda: self.controller.decryption_success())
            self.root.after(
                0,
                lambda: self._set_output_folder_enabled(result["output_file"]),
            )
            self.root.after(
                1300,
                lambda: messagebox.showinfo(
                    APP_NAME,
                    f"Decryption Successful!\n\nSaved To:\n{result['output_file']}",
                ),
            )

        except Exception as e:
            self.root.after(0, lambda: self.controller.failed(str(e)))
            self.root.after(0, lambda: messagebox.showerror(APP_NAME, str(e)))

        finally:
            self.root.after(0, lambda: self.encrypt_button.configure(state="normal"))
            self.root.after(0, lambda: self.decrypt_button.configure(state="normal"))

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

        self.password_strength.set(score / 100)

        if score < 40:
            self.password_strength_label.configure(text="Weak", text_color=ERROR)
        elif score < 70:
            self.password_strength_label.configure(text="Medium", text_color=WARNING)
        else:
            self.password_strength_label.configure(text="Strong", text_color=SUCCESS)

    def reset_interface(self):
        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")
        self.password_strength.set(0)
        self.password_strength_label.configure(text="Weak", text_color=ERROR)
        self._password_visible = False
        self._confirm_visible = False
        self.password_entry.configure(show="*")
        self.confirm_entry.configure(show="*")
        self.password_toggle.configure(text="👁")
        self.confirm_toggle.configure(text="👁")
        self.last_output_path = None
        self.open_folder_button.configure(state="disabled")
        self._reset_preview_to_default()
        self.preview_title.configure(text="No File Selected")
        self.selected_file_label.configure(text="Waiting for file...")
        self.controller.progress.reset()
        self.controller.activity.clear()
        self.controller.status.ready()

    def bind_events(self):
        self.password_entry.bind("<KeyRelease>", self.update_password_strength)

    def run(self):
        self.bind_events()
        self.root.mainloop()


if __name__ == "__main__":
    app = ArgusCryptApp()
    app.run()
