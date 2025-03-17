import asyncio
from bot import create_bot


async def main():
    app = create_bot()  # Create bot instance
    print("Bot is starting...")
    await app.start()  # Start the bot (async)

    # Keep the bot running and ensure the event loop is alive
    print("Bot is running...")
    try:
        await asyncio.Event().wait()  # Keep the bot running
    except (KeyboardInterrupt, SystemExit):
        print("Bot is stopping...")
    finally:
        await app.stop()  # Properly stop the bot
    

if __name__ == "__main__":
    asyncio.run(main())  # Use asyncio.run to handle the event loop
