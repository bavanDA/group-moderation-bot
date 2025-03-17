import asyncio
from pyrogram import Client

task_list = {}


async def delete_message_task(app: Client, chat_id: int, message_id: int):
    await asyncio.sleep(60)

    try:
        await app.delete_messages(chat_id, message_id)
        print(f"Deleted message {message_id} from chat {chat_id}")
    except Exception as e:
        print(f"Failed to delete message {message_id}: {e}")

    task_list.pop(message_id, None)


def schedule_message_deletion(app: Client, chat_id: int, message_id: int):
    task = asyncio.create_task(delete_message_task(app, chat_id, message_id))
    task_list[message_id] = task


def cancel_scheduled_deletion(message_id: int):
    task = task_list.pop(message_id, None)
    if task:
        task.cancel()
        print(f"Cancelled deletion for message {message_id}")
