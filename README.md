# 🚀 Group Moderation Bot  

A Telegram bot that moderates group chats by filtering inappropriate words, issuing warnings, and applying progressive penalties. Supports **English & Persian**.  

## ✨ Features  

✅ **Multi-language support** (English & Persian)  
✅ **Monitors group messages for filtered words**  
✅ **Progressive penalty system:**  
   - **1st offense** → Warning  
   - **2nd offense** → Warning  
   - **3rd offense** → 3-hour mute  
   - **4th offense** → Permanent mute  
✅ **Admin private reports** (violations are sent to the admin's private chat)  
✅ **Admin panel** in private chat with buttons for:  
   - 🔹 Add words to blacklist  
   - 🔹 Remove words from blacklist  
   - 🔹 View current blacklist  
   - 🔹 Remove user warnings  
✅ **Environment-based configuration**  
✅ **User violation tracking in database**  


## Installation

1. Clone the repository:
```bash
git clone https://github.com/bavanDA/Telegram-moderator.git
cd telegram-moderation-bot
```
2. Change `.env.example` file to `env`

3. Start the bot:
```bash
python -m venv env
pip install -r requirements.txt
python main.py
```

## Docker Setup

You can also run the bot using Docker. Follow these steps:

1. **Pull the Docker image**:
```bash
docker pull spoiler2400/group-moderation-bot:0.1.0
```

2. **Create a `.env` file** with the following environment variables:
```bash
API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN
ADMIN_IDS=AdminID1,AdminID2
```

3. **Run the Docker container**:
```bash
docker run -d --env-file .env spoiler2400/group-moderation-bot:0.1.0

```

## License

MIT