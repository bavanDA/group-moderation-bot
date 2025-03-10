from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Add Words", callback_data="add_words"),
                InlineKeyboardButton("Remove Words", callback_data="remove_words")
            ],
            [
                InlineKeyboardButton("Show List of Words", callback_data="show_words")
            ]
        ]
    )