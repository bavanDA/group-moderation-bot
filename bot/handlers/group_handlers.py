from pyrogram import filters
from pyrogram.types import ChatPermissions
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid
from bot.config import config
from bot.database import get_all_filtered_words, add_warning, remove_all_user_warnings, get_user_warnings_count
from datetime import datetime, timedelta
import re
from bot.utils.locale_manager import LocaleKeys
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.job_queue import schedule_message_deletion


def register_group_handlers(app, locale):

    async def report_admins(client, user):
        warning_msg = f'''{locale.get(LocaleKeys.report_start)} \n {locale.get(LocaleKeys.report_warning_msg)} {user['name']}
{locale.get(LocaleKeys.report_user_id)} [{user['id']}](https://t.me/@{user['id']})
{locale.get(LocaleKeys.report_username)} @{user['username']}
{locale.get(LocaleKeys.report_filtered_word)} {user['filtered_word']}
{locale.get(LocaleKeys.report_warning_count)} {user['warning_count']}
{locale.get(LocaleKeys.report_punishment)} {user['action']}'''

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                locale.get(LocaleKeys.remove_warning),
                callback_data=f"remove_warn_{user['id']}_{user['chat_id']}"
            )]
        ])

        for admin_id in config.ADMIN_IDS:
            await client.send_message(
                admin_id,
                warning_msg,
                reply_markup=keyboard
            )

    @app.on_message(filters.command("reset") & filters.group & filters.reply)
    async def reset_user_warnings(client, message):
        chat_id = message.chat.id

        chat_member = await client.get_chat_member(chat_id, message.from_user.id)

        if chat_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return

        replied_user = message.reply_to_message.from_user
        replied_user_member = await client.get_chat_member(chat_id, replied_user.id)

        username = replied_user.username
        first_name = replied_user.first_name
        display_name = "@" + username if username else first_name

        if not replied_user:
            return

        try:
            warning_counts = get_user_warnings_count(
                replied_user.id, chat_id=chat_id)

            remove_all_user_warnings(replied_user.id, chat_id)
            msg = await message.reply_text(f"{locale.get(LocaleKeys.reset_msg_p1)} {display_name} {locale.get(LocaleKeys.reset_msg_p2)}")
            schedule_message_deletion(client, chat_id, msg.id)

            if (warning_counts <= 2 or replied_user_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]):
                return

            permissions = ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
            await client.restrict_chat_member(chat_id, replied_user.id, permissions)

        except Exception as e:
            msg = await message.reply_text(f"Error resetting warnings: {str(e)}")
            schedule_message_deletion(client, chat_id, msg.id)

    @app.on_message(filters.command("info") & filters.group)
    async def get_user_info(client, message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            warnings_count = get_user_warnings_count(user_id, chat_id)
            msg = await message.reply_text(f"{locale.get(LocaleKeys.info_msg_p1)} {warnings_count} {locale.get(LocaleKeys.info_msg_p2)}")
            schedule_message_deletion(client, chat_id, msg.id)

        except Exception as e:
            msg = await message.reply_text(f"⚠️ Error getting warnings: {str(e)}")
            schedule_message_deletion(client, chat_id, msg.id)

    @app.on_message(filters.group & filters.text)
    async def monitor_group_messages(client, message):

        filtered_words = get_all_filtered_words()
        if not filtered_words:
            return

        message_text = message.text.lower()

        found_word = None

        for word in filtered_words:
            word_lower = word.lower()
            if word_lower in message_text:
                idx = message_text.find(word_lower)
                if idx > 0 and message_text[idx-1].isalpha():
                    continue
                idx += len(word_lower)

                if idx < len(message_text) and message_text[idx].isalpha():
                    continue

                found_word = word
                break

        if found_word:

            user = {}
            user_id = message.from_user.id
            chat_id = message.chat.id
            username = message.from_user.username
            first_name = message.from_user.first_name

            chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
            is_admin = chat_member.status in [
                ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]

            display_name = "@" + username if username else first_name
            if not display_name:
                display_name = f"User {user_id}"

            try:
                warning_count, action = add_warning(
                    user_id,
                    found_word,
                    chat_id,
                    username,
                    first_name
                )

                user['id'] = user_id
                user['chat_id'] = chat_id
                user['name'] = first_name
                user['username'] = username
                user['filtered_word'] = found_word
                user['warning_count'] = warning_count
                user['action'] = action

                if (is_admin):
                    user['action'] = "admin"
                try:
                    await message.delete()
                except Exception as e:
                    print(f"Could not delete message: {e}")

                await report_admins(client, user)

                if action == "warning" or is_admin:
                    msg = await message.reply_text(
                        f"⚠️ {locale.get(LocaleKeys.warning)} #{warning_count}: {display_name} {locale.get(LocaleKeys.warning_msg)} "
                    )
                    schedule_message_deletion(client, chat_id, msg.id)

                elif action.startswith("mute_"):

                    duration_text = locale.get(action)
                    mute_seconds = config.MUTE_DURATIONS.get(action, 0)
                    try:
                        mute_permissions = ChatPermissions(
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False
                        )

                        if ("permanent" in action):
                            await client.restrict_chat_member(
                                chat_id=chat_id,
                                user_id=user_id,
                                permissions=mute_permissions
                            )

                        else:
                            await client.restrict_chat_member(
                                chat_id=chat_id,
                                user_id=user_id,
                                permissions=mute_permissions,
                                until_date=datetime.now() + timedelta(seconds=mute_seconds)
                            )

                        msg = await client.send_message(
                            chat_id,
                            f"🚫{locale.get(LocaleKeys.user)} {display_name} {locale.get(LocaleKeys.mute_reason)} {duration_text} {locale.get(LocaleKeys.mute_msg)} \n "
                        )
                        schedule_message_deletion(client, chat_id, msg.id)

                    except ChatAdminRequired:
                        await client.send_message(
                            chat_id,
                            locale.get(LocaleKeys.bot_not_admin)
                        )
                    except UserAdminInvalid:
                        await client.send_message(
                            chat_id,
                            f"⚠️ Cannot restrict user {display_name} as they are an admin."
                        )
                    except Exception as e:
                        print(
                            f"Error muting user: {type(e).__name__}: {str(e)}")
                        await client.send_message(
                            chat_id,
                            f"⚠️ Failed to mute user {display_name}. Error: {type(e).__name__}: {str(e)}"
                        )

            except Exception as e:
                print(
                    f"Error handling filtered word: {type(e).__name__}: {str(e)}")
                try:
                    await client.send_message(
                        chat_id,
                        f"⚠️ An error occurred while processing filtered word: {type(e).__name__}: {str(e)}"
                    )
                except:
                    pass
