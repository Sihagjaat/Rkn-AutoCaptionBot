# AutoCaptionBot by RknDeveloper
# Copyright (c) 2024 RknDeveloper
# Licensed under the MIT License
# https://github.com/RknDeveloper/Rkn-AutoCaptionBot/blob/main/LICENSE
# Please retain this credit when using or forking this code.

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# ⚠️ Please do not remove this credit!


from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import UserNotParticipant
from config import Rkn_Botz
from .database import rkn_botz


# ✅ Force Subscribe Filter
def ForceSubCheck(channel):
    channel = channel.lstrip("@")

    async def func(flt, client: Client, message: Message) -> bool:
        user_id = message.from_user.id

        # Register user in DB
        await rkn_botz.register_user(user_id)

        # If no force sub channel set
        if not channel:
            return False

        try:
            member = await client.get_chat_member(channel, user_id)

            # If user joined, allow bot
            if member.status in [
                enums.ChatMemberStatus.MEMBER,
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.OWNER
            ]:
                return False

            # If user left/banned, block bot
            return True

        except UserNotParticipant:
            return True
        except Exception:
            return True

    return filters.create(func, "ForceSubCheck")


# 📩 Handler for blocked users / unsubscribed
@Client.on_message(filters.private & ForceSubCheck(Rkn_Botz.FORCE_SUB))
async def handle_force_sub(client: Client, message: Message):
    user_id = message.from_user.id
    channel_username = Rkn_Botz.FORCE_SUB.lstrip("@")
    chat_link = f"https://t.me/{channel_username}"

    # 📢 Button UI
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔔 Join Update Channel", url=chat_link)]]
    )

    try:
        member = await client.get_chat_member(channel_username, user_id)

        if member.status == enums.ChatMemberStatus.BANNED:
            return await message.reply_text(
                "**🚫 You are banned from using this bot.**\nContact admin if this is a mistake."
            )

        # If user joined, don't show force sub message
        if member.status in [
            enums.ChatMemberStatus.MEMBER,
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ]:
            return

    except UserNotParticipant:
        pass
    except Exception as e:
        return await message.reply_text(f"⚠️ Unexpected error: `{e}`")

    # Default reply if not joined
    return await message.reply_text(
        "**Hey buddy! 🔐 You need to join our updates channel before using me.**",
        reply_markup=button
    )


# ————
# End of file
# Original author: @RknDeveloperr
# GitHub: https://github.com/RknDeveloper

# Developer Contacts:
# Telegram: @RknDeveloperr
# Updates Channel: @Rkn_Bots_Updates & @Rkn_Botz
# Special Thanks To: @ReshamOwner
# Update Channels: @Digital_Botz & @DigitalBotz_Support

# ⚠️ Please do not remove this credit!
