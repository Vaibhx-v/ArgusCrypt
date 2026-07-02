import customtkinter as ctk
from ui.theme import *


def primary_button(master, text, command):

    return ctk.CTkButton(

        master,

        text=text,

        command=command,

        fg_color=PRIMARY,

        hover_color=PRIMARY_HOVER,

        text_color=TEXT,

        font=BUTTON_FONT,

        corner_radius=BUTTON_RADIUS,

        height=BUTTON_HEIGHT
    )


def card(master):

    return ctk.CTkFrame(

        master,

        fg_color=CARD_BG,

        corner_radius=CARD_RADIUS,

        border_width=1,

        border_color=BORDER
    )


def title(master, text):

    return ctk.CTkLabel(

        master,

        text=text,

        font=HEADING_FONT,

        text_color=TEXT
    )


def subtitle(master, text):

    return ctk.CTkLabel(

        master,

        text=text,

        font=LABEL_FONT,

        text_color=SECONDARY_TEXT
    )


def entry(master, placeholder="", show=None):

    return ctk.CTkEntry(

        master,

        placeholder_text=placeholder,

        show=show,

        height=ENTRY_HEIGHT,

        corner_radius=12,

        border_color=BORDER,

        fg_color=WINDOW_BG
    )