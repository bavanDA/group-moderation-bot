import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot_database.db")

    ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")
    ADMIN_IDS = [int(admin_id.strip())
                 for admin_id in ADMIN_IDS if admin_id.strip()]

    BOT_MSG_TTL = int(os.getenv("BOT_MSG_TTL", 60))

    # Penalty settings
    PENALTIES = {
        1: "warning",
        2: "warning",
        3: "mute_1h",
        4: "mute_3h",
        5: "mute_6h",
        6: "mute_12h",
        7: "mute_1d",
        8: "mute_3d",
        9: "mute_1w",
        10: "mute_permanent"
    }

    # Mute durations in seconds
    MUTE_DURATIONS = {
        "mute_1h": 1 * 60 * 60,
        "mute_3h": 3 * 60 * 60,
        "mute_6h": 6 * 60 * 60,
        "mute_12h": 12 * 60 * 60,
        "mute_1d": 24 * 60 * 60,
        "mute_3d": 3 * 24 * 60 * 60,
        "mute_1w": 7 * 24 * 60 * 60,
        "mute_permanent": 0  
    }


config = Config()
