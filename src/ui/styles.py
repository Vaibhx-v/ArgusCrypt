import customtkinter as ctk

from ui.theme import *


def transparent_frame(master, **kwargs):
    return ctk.CTkFrame(master, fg_color="transparent", **kwargs)


def card(master, **kwargs):
    options = {
        "fg_color": CARD_BG,
        "corner_radius": CARD_RADIUS,
        "border_width": 1,
        "border_color": BORDER,
    }
    options.update(kwargs)
    return ctk.CTkFrame(master, **options)


def card_header(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=HEADING_FONT,
        text_color=TEXT,
    )


def title(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=HEADING_FONT,
        text_color=TEXT,
    )


def subtitle(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=LABEL_FONT,
        text_color=SECONDARY_TEXT,
    )


def body_text(master, text, color=SECONDARY_TEXT):
    return ctk.CTkLabel(
        master,
        text=text,
        font=LABEL_FONT,
        text_color=color,
    )


def info_row(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=LABEL_FONT,
        text_color=TEXT,
        anchor="w",
        justify="left",
        wraplength=520,
    )


def mono_row(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=MONO_FONT,
        text_color=SECONDARY_TEXT,
        anchor="w",
        justify="left",
        wraplength=520,
    )


def section_label(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=("Segoe UI", 16, "bold"),
        text_color=TEXT,
        anchor="w",
    )


def status_badge(master, text, color=SUCCESS):
    return ctk.CTkLabel(
        master,
        text=text,
        font=STATUS_FONT,
        text_color=color,
    )


def action_button(master, text, command, width=ACTION_BUTTON_WIDTH):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        height=BUTTON_HEIGHT,
        corner_radius=BUTTON_RADIUS,
        font=BUTTON_FONT,
        fg_color=PRIMARY,
        hover_color=PRIMARY_HOVER,
        text_color=TEXT,
    )


def primary_button(master, text, command, width=None):
    button_width = width if width is not None else ACTION_BUTTON_WIDTH
    return action_button(master, text, command, width=button_width)


def secondary_button(master, text, command, width=ACTION_BUTTON_WIDTH):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=width,
        height=BUTTON_HEIGHT,
        corner_radius=BUTTON_RADIUS,
        font=BUTTON_FONT,
        fg_color=WINDOW_BG,
        hover_color=CARD_HOVER,
        border_width=1,
        border_color=BORDER,
        text_color=TEXT,
    )


def icon_button(master, text, command):
    return ctk.CTkButton(
        master,
        text=text,
        command=command,
        width=TOGGLE_BUTTON_WIDTH,
        height=ENTRY_HEIGHT,
        corner_radius=12,
        font=("Segoe UI", 16),
        fg_color=WINDOW_BG,
        hover_color=CARD_HOVER,
        border_width=1,
        border_color=BORDER,
        text_color=SECONDARY_TEXT,
    )


def entry(master, placeholder="", show=None):
    return ctk.CTkEntry(
        master,
        placeholder_text=placeholder,
        show=show,
        height=ENTRY_HEIGHT,
        corner_radius=12,
        border_color=BORDER,
        fg_color=WINDOW_BG,
        font=LABEL_FONT,
        text_color=TEXT,
    )


def password_field(master, placeholder, toggle_command):
    row = transparent_frame(master)
    row.grid_columnconfigure(0, weight=1)

    field = entry(row, placeholder=placeholder, show="*")
    field.grid(row=0, column=0, sticky="ew", padx=(0, SMALL_PADDING))

    toggle = icon_button(row, "👁", toggle_command)
    toggle.grid(row=0, column=1)

    return row, field, toggle


def progress_bar(master):
    bar = ctk.CTkProgressBar(
        master,
        height=PROGRESS_HEIGHT,
        corner_radius=8,
        fg_color=PROGRESS_BG,
        progress_color=PROGRESS_COLOR,
    )
    bar.set(0)
    return bar


def build_info_card(parent, heading, rows, mono_keys=None):
    mono_keys = mono_keys or set()
    frame = card(parent)
    card_header(frame, heading).pack(
        anchor="w",
        padx=LARGE_PADDING,
        pady=(LARGE_PADDING, SMALL_PADDING),
    )

    content = transparent_frame(frame)
    content.pack(fill="both", expand=True, padx=LARGE_PADDING, pady=(0, LARGE_PADDING))

    labels = {}
    for key, default_text in rows:
        factory = mono_row if key in mono_keys else info_row
        label = factory(content, default_text)
        label.pack(fill="x", pady=3)
        labels[key] = label

    return frame, labels


def panel_card(master, **kwargs):
    options = {
        "fg_color": CARD_BG,
        "corner_radius": CARD_RADIUS,
        "border_width": 1,
        "border_color": BORDER,
    }
    options.update(kwargs)
    return ctk.CTkFrame(master, **options)


class PanelCard(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        options = {
            "fg_color": CARD_BG,
            "corner_radius": CARD_RADIUS,
            "border_width": 1,
            "border_color": BORDER,
        }
        options.update(kwargs)
        super().__init__(master, **options)


def panel_title(master, text):
    return ctk.CTkLabel(
        master,
        text=text,
        font=("Segoe UI", 18, "bold"),
        text_color=TEXT,
    )
