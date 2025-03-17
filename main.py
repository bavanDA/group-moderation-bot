import asyncio
from bot import create_bot


async def main():
    app = create_bot()  
    print("Bot is starting...")
    await app.start()  

    print("Bot is running...")
    try:
        await asyncio.Event().wait()  
    except (KeyboardInterrupt, SystemExit):
        print("Bot is stopping...")
    finally:
        await app.stop()  
    

if __name__ == "__main__":
    asyncio.run(main())  
