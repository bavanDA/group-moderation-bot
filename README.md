# Telegram Content Moderation Bot

A Telegram bot that monitors messages in groups for inappropriate content, issues warnings, and applies mute penalties based on a configurable word list. Admins can manage the word list through a private interface.

## Features

- Monitors group messages for inappropriate words
- Progressive penalty system:
  - First offense: Warning
  - Second offense: Warning
  - Third offense: 3-hour mute
  - Fourth offense: Permanent mute
- Admin panel in private chat with buttons for:
  - Adding words to the blacklist
  - Removing words from the blacklist
  - Viewing the current blacklist
- Environment-based configuration
- User violation tracking in database

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

## Usage

### Admin Commands

When an admin sends msg to the bot in a private chat, they'll receive an admin panel with three options:

1. **Add words** - Add new words to the blacklist
2. **Remove words** - Remove words from the blacklist
3. **Show list of words** - View all currently blacklisted words

### Group Moderation

Once added to a group, the bot will:
1. Monitor all messages for blacklisted words
2. Track violations by users
3. Apply progressive penalties:
   - First and second violations: Warning message
   - Third violation: 3-hour mute
   - Fourth violation: Permanent mute

## License

MIT