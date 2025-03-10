from pyrogram import Client
from bot.config import config
from bot.database import init_db
from bot.handlers import register_handlers

def create_bot():
    # Initialize the database
    init_db()
    
    # Create the bot
    app = Client(
        "admin_bot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN
    )
    
    # Register all handlers
    register_handlers(app)
    
    return app
