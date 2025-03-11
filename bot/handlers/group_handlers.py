from pyrogram import filters
from pyrogram.types import ChatPermissions
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid
from bot.config import config
from bot.database import get_all_filtered_words, add_warning, get_user_warning_count
from datetime import datetime, timedelta
import re
from bot.utils.locale_manager import LocaleKeys
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def register_group_handlers(app, locale):

    async def report_admins(client, user):
        warning_msg = f"Warning Report:\nUser: {user['name']}\nWarning Count: {user['warning_count']}\nFiltered Word: {user['filtered_word']}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "Remove Warning",
                callback_data=f"remove_warn_{user['id']}_{user['chat_id']}"
            )]
        ])

        for admin_id in config.ADMIN_IDS:
            await client.send_message(
                admin_id,
                warning_msg,
                reply_markup=keyboard
            )

    @app.on_message(filters.group & filters.text)
    async def monitor_group_messages(client, message):
        filtered_words = get_all_filtered_words()
        if not filtered_words:
            return

        message_text = message.text.lower()

        words_in_message = re.findall(r'\b\w+\b', message_text)

        found_word = None

        for word in filtered_words:
            word_lower = word.lower()
            if word_lower in words_in_message:
                found_word = word
                break

        if found_word:
            try:
                chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
                if chat_member.status in ["creator", "administrator"]:
                    return
            except Exception as e:
                print(f"Error checking admin status: {e}")

            user = {}
            user_id = message.from_user.id
            chat_id = message.chat.id
            username = message.from_user.username
            first_name = message.from_user.first_name

            display_name = username if username else first_name
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
                try:
                    await message.delete()
                except Exception as e:
                    print(f"Could not delete message: {e}")

                # Handle the appropriate action based on warning count
                if action == "warning":
                    await message.reply_text(
                        f"⚠️ {locale.get(LocaleKeys.warning)} #{warning_count}: {display_name} {locale.get(LocaleKeys.warning_msg)} "
                    )
                    await report_admins(client, user)

                elif action.startswith("mute"):

                    # Get mute duration
                    duration = 3 * 60 * 60
                    duration_text = locale.get(LocaleKeys.h3_mute) if duration > 0 else locale.get(
                        LocaleKeys.permanent_mute)

                    # Restrict user with proper permissions
                    try:
                        # Define restricted permissions (no permissions)
                        mute_permissions = ChatPermissions(
                            can_send_messages=False,
                            can_send_media_messages=False,
                            can_send_other_messages=False,
                            can_add_web_page_previews=False
                        )

                        if (action == "mute_3h"):
                            # Restrict user
                            await client.restrict_chat_member(
                                chat_id=chat_id,
                                user_id=user_id,
                                permissions=mute_permissions,
                                until_date=datetime.now() + timedelta(hours=3)
                            )

                        else:
                            await client.restrict_chat_member(
                                chat_id=chat_id,
                                user_id=user_id,
                                permissions=mute_permissions
                            )

                        # Send notification
                        await client.send_message(
                            chat_id,
                            f"🚫 {display_name} {duration_text} {locale.get(LocaleKeys.mute_msg)} "
                            f"for using filtered words {warning_count} times."
                        )

                    except ChatAdminRequired:
                        await client.send_message(
                            chat_id,
                            "⚠️ I don't have permission to restrict users. Please make me an admin with appropriate rights."
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
