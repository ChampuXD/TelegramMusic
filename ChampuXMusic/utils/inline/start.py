from typing import Union

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config


def start_pannel(_, BOT_USERNAME, OWNER: Union[bool, int] = None):
    buttons = [
        [
            InlineKeyboardButton(
                text="✦ᴀᴅᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ◉‿◉",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="☆ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs☆",
                callback_data="settings_back_helper",
            ),
            InlineKeyboardButton(
                text="sᴇᴛᴛɪɴɢs", callback_data="settings_helper"
            ),
        ],
     ]
    return buttons


def private_panel(_, BOT_USERNAME, OWNER: Union[bool, int] = None):
    buttons = [
        [
            InlineKeyboardButton(
                text="✦ᴀᴅᴅ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ◉‿◉",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(
                text="❣ᴄʜᴀᴛ ɢʀᴏᴜᴘ❣🥀", url=config.SUPPORT_GROUP
            ),
            InlineKeyboardButton(
                text="ᴏᴡɴᴇʀ͡° ͜ʖ ͡°", user_id=OWNER
            )
        ],
         [
            InlineKeyboardButton(
                text="☆ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs☆", callback_data="settings_back_helper"
            )
        ],
         [
            InlineKeyboardButton(
                text="ᴄʜᴀɴɴᴇʟ͡° ͜ʖ ͡°💘", url=f"https://t.me/rockhushh"
            ),
            InlineKeyboardButton(

                text="ᴅᴇᴠʟᴏᴘᴇʀ✶❍", url=f"https://t.me/Rockhush_13Ra_kinG"
             ),
          ],
          [
            InlineKeyboardButton(
                text="☆ ᴀʙᴏᴜᴛ ʀᴏᴄᴋʜᴜsʜ ☆", url=f"https://t.me/about_Rockhush"
            ),
          ],
     ]
    return buttons
