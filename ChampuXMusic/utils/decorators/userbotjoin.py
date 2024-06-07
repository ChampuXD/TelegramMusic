import asyncio

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT
from strings import get_string
from ChampuXMusic import app
from ChampuXMusic.misc import SUDOERS
from ChampuXMusic.utils.database import (
    get_assistant,
    get_lang,
    is_active_chat,
    is_maintenance,
)

links = {}


def UserbotWrapper(command):
    async def wrapper(client, message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} is under maintenance, visit [support chat]({SUPPORT_CHAT}) for knowing the reason.",
                    disable_web_page_preview=True,
                    protect_content=True,
                )

        try:
            await message.delete()
        except:
            pass

        chat_id = message.chat.id

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text(
                        "➥ ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ ᴍᴜsᴛ ɢɪᴠᴇ ᴀʟʟ ᴘᴏᴡᴇʀ.",
                        protect_content=True,
                    )
                if (
                    get.status == ChatMemberStatus.BANNED
                    or get.status == ChatMemberStatus.RESTRICTED
                ):
                    return await message.reply_text(
                        _["call_2"].format(
                            app.mention, userbot.id, userbot.name, userbot.username,
                            protect_content=True,
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="๏ ᴜɴʙᴀɴ ᴀssɪsᴛᴀɴᴛ ๏",
                                        callback_data=f"unban_assistant",
                                    )
                                ]
                            ]
                        ),
                    )
            except UserNotParticipant:
                if message.chat.username:
                    invitelink = message.chat.username
                    await userbot.join_chat(invitelink)
                else:
                    if chat_id in links:
                        invitelink = links[chat_id]
                        try:
                            await userbot.resolve_peer(invitelink)
                        except:
                            pass
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.reply_text(
                                "➥ ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ ᴍᴜsᴛ ɢɪᴠᴇ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴘᴏᴡᴇʀ ғᴏʀ ɪɴᴠɪᴛᴇ ᴍʏ ᴀssɪsᴛᴀɴᴛ ɪᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.",
                                protect_content=True,
                            )
                        except Exception as e:
                            return await message.reply_text(
                                f"{app.mention} ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ✅\n\nɪᴅ:- {userbot.mention}..",
                                protect_content=True,
                            )

                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                myu = await message.reply_text("ᴀssɪsᴛᴀɴᴛ ᴊᴏɪɴɪɴɢ...")
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invitelink)
                    await myu.delete()
                    await message.reply_text(
                        f"{app.mention} ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ✅\n\nɪᴅ:- **@{userbot.username}**"
                    )
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_3"].format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.delete()
                    await message.reply_text(
                        f"{app.mention} ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ✅\n\nɪᴅ:- **@{userbot.username}**"
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(
                        f"{app.mention} ᴀssɪsᴛᴀɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴊᴏɪɴᴇᴅ ✅\n\nɪᴅ:- **@{userbot.username}**"
                    )

                links[chat_id] = invitelink

                try:
                    await userbot.resolve_peer(chat_id)
                except:
                    pass

        return await command(client, message, _, chat_id)

    return wrapper
