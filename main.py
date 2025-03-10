from bot import create_bot

if __name__ == "__main__":
    app = create_bot()
    print("Bot is starting...")
    app.run()