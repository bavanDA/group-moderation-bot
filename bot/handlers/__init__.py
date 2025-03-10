from bot.handlers.admin_handlers import register_admin_handlers
from bot.handlers.group_handlers import register_group_handlers
from bot.handlers.user_handlers import register_user_handlers

def register_handlers(app):
    register_admin_handlers(app)
    register_group_handlers(app)
    register_user_handlers(app)
