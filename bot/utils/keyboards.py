from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.locale_manager import LocaleKeys


def get_admin_keyboard(locale):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(locale.get(
                    LocaleKeys.add_words), callback_data="add_words"),
                InlineKeyboardButton(locale.get(
                    LocaleKeys.remove_words), callback_data="remove_words")
            ],
            [
                InlineKeyboardButton(locale.get(
                    LocaleKeys.show_words), callback_data="show_words")
            ]
        ]
    )
