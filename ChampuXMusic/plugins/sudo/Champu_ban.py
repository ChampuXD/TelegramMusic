import random

from pyrogram import *
from pyrogram.types import *

from ChampuXMusic import app
from ChampuXMusic.misc import SUDOERS
from ChampuXMusic.utils.Champu_ban import admin_filter

Champu_text = [
    "ʜᴇʏ ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ᴅɪsᴛᴜʀʙ ᴍᴇ.",
    "ᴡʜᴏ ᴀʀᴇ ʏᴏᴜ",
    "ᴀᴀᴘ ᴋᴏɴ ʜᴏ",
    "ᴀᴀᴘ ᴍᴇʀᴇ ᴏᴡɴᴇʀ ᴛᴏ ɴʜɪ ʟɢᴛᴇ ",
    "ʜᴇʏ ᴛᴜᴍ ᴍᴇʀᴀ ɴᴀᴍᴇ ᴋʏᴜ ʟᴇ ʀʜᴇ ʜᴏ ᴍᴇᴋᴏ sᴏɴᴇ ᴅᴏ",
    "ʜᴀ ʙᴏʟᴏ ᴋʏᴀ ᴋᴀᴀᴍ ʜᴀɪ ",
    "ᴅᴇᴋʜᴏ ᴀʙʜɪ ᴍᴀɪ ʙᴜsʏ ʜᴜ ",
    "ʜᴇʏ ɪ ᴀᴍ ʙᴜsʏ",
    "ᴀᴀᴘᴋᴏ sᴍᴊ ɴʜɪ ᴀᴀᴛᴀ ᴋʏᴀ ",
    "ʟᴇᴀᴠᴇ ᴍᴇ ᴀʟᴏɴᴇ",
    "ᴅᴜᴅᴇ ᴡʜᴀᴛ ʜᴀᴘᴘᴇɴᴅ",
]

strict_txt = [
    "ɪ ᴄᴀɴ'ᴛ ʀᴇsᴛʀɪᴄᴛ ᴀɢᴀɪɴsᴛ ᴍʏ ʙᴇsᴛɪᴇs",
    "ᴀʀᴇ ʏᴏᴜ sᴇʀɪᴏᴜs ɪ ᴀᴍ ɴᴏᴛ ʀᴇsᴛʀɪᴄᴛ ᴛᴏ ᴍʏ ғʀɪᴇɴᴅs",
    "ғᴜᴄᴋ ʏᴏᴜ ʙsᴅᴋ ᴋ ᴍᴀɪ ᴀᴘɴᴇ ᴅᴏsᴛᴏ ᴋᴏ ᴋʏᴜ ᴋʀᴜ",
    "ʜᴇʏ sᴛᴜᴘɪᴅ ᴀᴅᴍɪɴ ",
    "ʜᴀ ʏᴇ ᴘʜᴇʟᴇ ᴋʀʟᴏ ᴍᴀᴀʀ ʟᴏ ᴇᴋ ᴅᴜsʀᴇ ᴋɪ ɢᴡᴀᴀɴᴅ",
    "ɪ ᴄᴀɴ'ᴛ ʜɪ ɪs ᴍʏ ᴄʟᴏsᴇsᴛ ғʀɪᴇɴᴅ",
    "ɪ ʟᴏᴠᴇ ʜɪᴍ ᴘʟᴇᴀsᴇ ᴅᴏɴ'ᴛ ʀᴇsᴛɪᴄᴛ ᴛʜɪs ᴜsᴇʀ ᴛʀʏ ᴛᴏ ᴜsᴇʀᴛᴀɴᴅ ",
]


ban = ["ban", "boom"]
unban = [
    "unban",
]
mute = ["mute", "silent", "shut"]
unmute = ["unmute", "speak", "free"]
kick = ["kick", "out", "nikaal", "nikal"]
promote = ["promote", "adminship"]
demote = ["demote", "lelo"]
group = ["group"]
channel = ["channel"]


# ========================================= #


@app.on_message(filters.command(["hampu"], prefixes=["C", "c"]) & admin_filter)
async def restriction_app(app: app, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 2:
        return await message.reply(random.choice(Champu_text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await message.reply(
                        "OK, Ban kar diya!"
                    )

        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await app.unban_chat_member(chat_id, user_id)
                await message.reply(f"Ok, aap bolte hai to unban kar diya")

        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await app.unban_chat_member(chat_id, user_id)
                    await message.reply("get lost!")

        for muted in data:
            print(f"present {muted}")
            if muted in mute:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply(f"muted successfully!")

        for unmuted in data:
            print(f"present {unmuted}")
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await message.chat.restrict_member(user_id, permissions)
                await message.reply(f"Huh, OK, sir!")

        for promoted in data:
            print(f"present {promoted}")
            if promoted in promote:
                await app.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=True,
                        can_delete_messages=True,
                        can_restrict_members=False,
                        can_pin_messages=True,
                        can_promote_members=False,
                        can_manage_chat=True,
                        can_manage_video_chats=True,
                    ),
                )
                await message.reply("promoted !")

        for demoted in data:
            print(f"present {demoted}")
            if demoted in demote:
                await app.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                        can_manage_chat=False,
                        can_manage_video_chats=False,
                    ),
                )
                await message.reply("demoted !")
