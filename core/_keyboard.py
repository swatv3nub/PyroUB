#Hamker Baba

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core._functions import get_urls_from_text


def btn(text, data, type=None):
    type = "url" if get_urls_from_text(data) else "callback_data"
    return InlineKeyboardButton(text, **{type: data})


def ikb(keyboard: list):
    lines = []
    for row in keyboard:
        line = []
        for button in row:
            button = btn(*button)  # InlineKeyboardButton
            line.append(button)
        lines.append(line)
    return InlineKeyboardMarkup(inline_keyboard=lines)
