from bot.handlers.admin_handlers import register_admin_handlers
from bot.handlers.group_handlers import register_group_handlers
from bot.handlers.user_handlers import register_user_handlers

def register_handlers(app,locale):
    register_admin_handlers(app,locale)
    register_group_handlers(app,locale)
    register_user_handlers(app,locale)
