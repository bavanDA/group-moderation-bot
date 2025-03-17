from pyrogram import filters
from pyrogram.types import CallbackQuery
from bot.config import config
from bot.utils.keyboards import get_admin_keyboard
from bot.database import add_filtered_word, remove_filtered_word, get_all_filtered_words
from bot.utils.locale_manager import LocaleKeys
from bot.database import remove_user_warning
from pyrogram.types import ChatPermissions

WAITING_FOR_WORD_TO_ADD = {}
WAITING_FOR_WORD_TO_REMOVE = {}


def register_admin_handlers(app, locale):

    @app.on_message(filters.command("lang"))
    async def change_language(client, message):
        user_id = message.from_user.id

        if user_id not in config.ADMIN_IDS:
            await message.reply_text(locale.get(LocaleKeys.unauthorized))
            return

        # Toggle between English and Farsi
        lang = "en" if locale.lang == "fa" else "fa"
        locale.set_language(lang)
        await message.reply_text(locale.get(LocaleKeys.lang_changed))

    @app.on_message(filters.private & filters.text & (filters.command("start") | filters.command("settings")))
    async def handle_start(client, message):
        user_id = message.from_user.id

        if user_id in config.ADMIN_IDS:
            await message.reply_text(
                locale.get(LocaleKeys.welcome),
                reply_markup=get_admin_keyboard(locale)
            )
        else:
            await message.reply_text(locale.get(LocaleKeys.unauthorized))

    @app.on_callback_query(filters.regex(r"^remove_warn_(\d+)_-(\d+)"))
    async def handle_remove_warning(client, callback_query):
        user_id = int(callback_query.matches[0].group(1))
        chat_id = -1*int(callback_query.matches[0].group(2))

        try:
            remove_user_warning(user_id, chat_id=chat_id)

            permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            await client.restrict_chat_member(chat_id, user_id, permissions)

            await callback_query.message.delete()

            await callback_query.answer("Warning removed and user unmuted successfully")
        except Exception as e:
            await callback_query.answer(f"Error: {str(e)}", show_alert=True)

    @app.on_callback_query()
    async def handle_callback(client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id

        if user_id not in config.ADMIN_IDS:
            await callback_query.answer(locale.get(LocaleKeys.unauthorized), show_alert=True)
            return

        if callback_query.data == "add_words":
            WAITING_FOR_WORD_TO_ADD[user_id] = True
            await callback_query.message.reply_text(locale.get(LocaleKeys.prompt_add_word))
            await callback_query.answer()

        elif callback_query.data == "remove_words":
            words = get_all_filtered_words()
            if not words:
                await callback_query.message.reply_text(locale.get(LocaleKeys.empty_word_list))
                await callback_query.answer()
                return

            WAITING_FOR_WORD_TO_REMOVE[user_id] = True
            await callback_query.message.reply_text(locale.get(LocaleKeys.prompt_remove_word))
            await callback_query.answer()

        elif callback_query.data == "show_words":
            words = get_all_filtered_words()
            if words:
                word_list = "\n".join([f"• {word}" for word in words])
                await callback_query.message.reply_text(f"{locale.get(LocaleKeys.filtered_words_list)}\n{word_list}")
            else:
                await callback_query.message.reply_text(locale.get(LocaleKeys.empty_word_list))
            await callback_query.answer()

        else:
            await callback_query.answer(locale.get(LocaleKeys.unknown_option))

    @app.on_message(filters.private & filters.text)
    async def handle_messages(client, message):
        user_id = message.from_user.id

        if user_id not in config.ADMIN_IDS:
            return

        if user_id in WAITING_FOR_WORD_TO_ADD:
            del WAITING_FOR_WORD_TO_ADD[user_id]
            words = message.text
            result = add_filtered_word(locale, words)

            await message.reply_text(
                result,
                reply_markup=get_admin_keyboard(locale)
            )

        elif user_id in WAITING_FOR_WORD_TO_REMOVE:
            del WAITING_FOR_WORD_TO_REMOVE[user_id]
            words = message.text
            result = remove_filtered_word(locale, words)

            await message.reply_text(
                result,
                reply_markup=get_admin_keyboard(locale)
            )
