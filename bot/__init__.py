from pyrogram import Client
from bot.config import config
from bot.database import init_db
from bot.handlers import register_handlers
from bot.utils.locale_manager import LocaleManager


def create_bot():
    init_db()

    app = Client(
        "admin_bot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN
    )

    locale = LocaleManager("fa")

    register_handlers(app, locale)

    return app
