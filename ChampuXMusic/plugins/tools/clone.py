import logging
import os

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    AccessTokenExpired,
    AccessTokenInvalid,
)

from config import API_HASH, API_ID, LOGGER_ID
from ChampuXMusic import app
from ChampuXMusic.misc import SUDOERS
from ChampuXMusic.utils.database import clonebotdb, get_assistant

CLONES = set()


@app.on_message(filters.command(["clone", "host", "deploy"]) & SUDOERS)
async def clone_txt(client, message):
    userbot = await get_assistant(LOGGER_ID)
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴡʜɪʟᴇ ɪ ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ.")
        try:
            ai = Client(
                bot_token,
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="ChampuXMusic.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            bot_users = await ai.get_users(bot.username)
            bot_id = bot_users.id

        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text(
                "**ʏᴏᴜ ʜᴀᴠᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴀɴ ɪɴᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ.**"
            )
            return

        except Exception as e:
            cloned_bot = await clonebotdb.find_one({"token": bot_token})
            if cloned_bot:
                await mi.edit_text("**🤖 ʏᴏᴜʀ ʙᴏᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴄʟᴏɴᴇᴅ ✅**")
                return

        # Proceed with the cloning process
        await mi.edit_text(
            "**ᴄʟᴏɴɪɴɢ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ. ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ʙᴇ sᴛᴀʀᴛ.**"
        )
        try:

            await app.send_message(
                LOGGER_ID, f"**#New_Clones**\n\n**ʙᴏᴛ:- @{bot.username}**"
            )
            await userbot.send_message(bot.username, f"/start")

            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": message.from_user.id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
            }
            clonebotdb.insert_one(details)
            CLONES.add(bot.id)
            await mi.edit_text(
                f"**ʙᴏᴛ @{bot.username} hᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴄʟᴏɴᴇᴅ ᴀɴᴅ sᴛᴀʀᴛᴇᴅ ✅.**\n**ʀᴇᴍᴏᴠᴇ ᴄʟᴏɴᴇᴅ ʙʏ :- /delclone**"
            )
        except BaseException as e:
            logging.exception("**ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴄʟᴏɴɪɴɢ ʙᴏᴛ.**")
            await mi.edit_text(
                f"⚠️ <b>ᴇʀʀᴏʀ:</b>\n\n<code>{e}</code>\n\n**ᴋɪɴᴅʟʏ ғᴏᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ @vk_zone ᴛᴏ ɢᴇᴛ ᴀssɪsᴛᴀɴᴄᴇ**"
            )
    else:
        await message.reply_text(
            "**ɢɪᴠᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀғᴛᴇʀ /clone ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ @Botfather.**"
        )


@app.on_message(
    filters.command(
        [
            "deletecloned",
            "delcloned",
            "delclone",
            "deleteclone",
            "removeclone",
            "cancelclone",
        ]
    )
)
async def delete_cloned_bot(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "**⚠️ ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.**"
            )
            return

        bot_token = " ".join(message.command[1:])
        ok = await message.reply_text("**ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴛᴏᴋᴇɴ...**")

        cloned_bot = await clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await ok.edit_text(
                "**🤖 ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴅɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ ᴍʏ sᴇʀᴠᴇʀ ☠️**\n**ᴄʟᴏɴᴇ ʙʏ :- /clone**"
            )
            os.system(f"pkill -9 python3 && bash start")

        else:
            await message.reply_text(
                "**⚠️ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʟɪsᴛ.**"
            )
    except Exception as e:
        await message.reply_text(
            f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴇ ᴄʟᴏɴᴇᴅ ʙᴏᴛ:** {e}"
        )
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots........")
        bots = clonebotdb.find()
        async for bot in bots:
            bot_token = bot["token"]
            ai = Client(
                f"{bot_token}",
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="ChampuXMusic.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            if bot.id not in CLONES:
                try:
                    CLONES.add(bot.id)
                except Exception:
                    pass
    except Exception as e:
        logging.exception("Error while restarting bots.")


@app.on_message(filters.command("cloned") & SUDOERS)
async def list_cloned_bots(client, message):
    try:
        cloned_bots = clonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)

        if not cloned_bots_list:
            await message.reply_text("ɴᴏ ʙᴏᴛs ʜᴀᴠᴇ ʙᴇᴇɴ ᴄʟᴏɴᴇᴅ ʏᴇᴛ.")
            return

        total_clones = len(cloned_bots_list)
        text = f"**ᴛᴏᴛᴀʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs:** {total_clones}\n\n"

        for bot in cloned_bots_list:
            text += f"**ʙᴏᴛ ɪᴅ:** `{bot['bot_id']}`\n"
            text += f"**ʙᴏᴛ ɴᴀᴍᴇ:** {bot['name']}\n"
            text += f"**ʙᴏᴛ ᴜsᴇʀɴᴀᴍᴇ:** @{bot['username']}\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʟɪsᴛɪɴɢ ᴄʟᴏɴᴇᴅ ʙᴏᴛs.**")


@app.on_message(filters.command("delallclone") & SUDOERS)
async def delete_all_cloned_bots(client, message):
    try:
        a = await message.reply_text("**ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs...**")
        await clonebotdb.delete_many({})
        CLONES.clear()

        await a.edit_text("**ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**")
    except Exception as e:
        await a.edit_text(f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴅᴇʟᴇᴛɪɴɢ ᴀʟʟ ᴄʟᴏɴᴇᴅ ʙᴏᴛs.** {e}")
        logging.exception(e)
