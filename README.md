# 🚀 Group Moderation Bot  

A Telegram bot that moderates group chats by filtering inappropriate words, issuing warnings, and applying progressive penalties. Supports **English & Persian**.  

## ✨ Features  

✅ **Multi-language support** (English & Persian)  
✅ **Monitors group messages for filtered words**  
✅ **Progressive penalty system (flexible & configurable):**  
   - **1st offense** → Warning  
   - **2nd offense** → Warning  
   - **3rd offense** → 1-hour mute  
   - **4th offense** → 3-hour mute  
   - **5th offense** → 6-hour mute  
   - **6th offense** → 12-hour mute  
   - **7th offense** → 1-day mute  
   - **8th offense** → 3-day mute  
   - **9th offense** → 1-week mute  
   - **10th offense** → Permanent mute  

✅ **Admin private reports** (violations are sent to the admin's private chat)  
✅ **Admin panel** in private chat with buttons for:  
   - 🔹 Add words to blacklist  
   - 🔹 Remove words from blacklist  
   - 🔹 View current blacklist  
   - 🔹 View user warnings and remove them
   - 🔹 Reset user warnings  

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
python -m venv env && env\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Docker Setup

You can also run the bot using Docker. Follow these steps:


1. Rename `env.example` to `.env` and update the environment variables as needed

2. Build and run the Docker containers using Docker Compose:
```bash
docker compose up --build -d
```

## License

[MIT License](LICENSE)