from pyrogram import filters
from pyrogram.types import CallbackQuery
from bot.config import config
from bot.utils.keyboards import get_admin_keyboard
from bot.database import add_filtered_word, remove_filtered_word, get_all_filtered_words

# Define conversation states
WAITING_FOR_WORD_TO_ADD = {}
WAITING_FOR_WORD_TO_REMOVE = {}

def register_admin_handlers(app):
    @app.on_message(filters.private & filters.text & (filters.command("start") | filters.regex("^hi$")))
    async def handle_start(client, message):
        user_id = message.from_user.id
        
        if user_id in config.ADMIN_IDS:
            await message.reply_text(
                "Hi, welcome to bot",
                reply_markup=get_admin_keyboard()
            )
        else:
            await message.reply_text("You're not authorized to use this bot.")

    @app.on_callback_query()
    async def handle_callback(client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        
        if user_id not in config.ADMIN_IDS:
            await callback_query.answer("You're not authorized to use this function.", show_alert=True)
            return
        
        if callback_query.data == "add_words":
            WAITING_FOR_WORD_TO_ADD[user_id] = True
            await callback_query.message.reply_text("Please send the word you want to add:")
            await callback_query.answer()
            
        elif callback_query.data == "remove_words":
            words = get_all_filtered_words()
            if not words:
                await callback_query.message.reply_text("The word list is empty.")
                await callback_query.answer()
                return
                
            WAITING_FOR_WORD_TO_REMOVE[user_id] = True
            await callback_query.message.reply_text("Please send the word you want to remove:")
            await callback_query.answer()
            
        elif callback_query.data == "show_words":
            words = get_all_filtered_words()
            if words:
                word_list = "\n".join([f"• {word}" for word in words])
                await callback_query.message.reply_text(f"List of filtered words:\n{word_list}")
            else:
                await callback_query.message.reply_text("The word list is empty.")
            await callback_query.answer()
        
        else:
            await callback_query.answer("Unknown option")

    @app.on_message(filters.private & filters.text)
    async def handle_messages(client, message):
        user_id = message.from_user.id
        
        if user_id not in config.ADMIN_IDS:
            return
        
        if user_id in WAITING_FOR_WORD_TO_ADD:
            del WAITING_FOR_WORD_TO_ADD[user_id]
            word = message.text.strip().lower()
            success, msg = add_filtered_word(word)
            
            await message.reply_text(
                f"{msg}",
                reply_markup=get_admin_keyboard()
            )
        
        elif user_id in WAITING_FOR_WORD_TO_REMOVE:
            del WAITING_FOR_WORD_TO_REMOVE[user_id]
            word = message.text.strip().lower()
            success, msg = remove_filtered_word(word)
            
            await message.reply_text(
                f"{msg}",
                reply_markup=get_admin_keyboard()
            )
