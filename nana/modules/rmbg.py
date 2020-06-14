# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.
# Ported to Nana by @pokurt

import os

from removebg import RemoveBg
from pyrogram import Filters
from nana import app, Command, remove_bg_api
from nana.helpers.PyroHelpers import ReplyCheck

DOWN_PATH = '/root/nana/'

REMOVE_BG_API_KEY = remove_bg_api

IMG_PATH = DOWN_PATH + "image.jpg"


@app.on_message(Filters.me & Filters.command(["rmbg"], Command))
async def lastfm(client, message):
    if not REMOVE_BG_API_KEY:
        await message.edit("Get the API from [Remove.bg](https://www.remove.bg/b/background-removal-api)", disable_web_page_preview=True, parse_mode="html")
    await message.edit("Analysing...")
    replied = message.reply_to_message
    if (replied and replied.media
            and (replied.photo
                or (replied.document and "image" in replied.document.mime_type))):
        if os.path.exists(IMG_PATH):
            os.remove(IMG_PATH)
        await client.download_media(message=replied, file_name=IMG_PATH)
        await message.edit("Removing Background...")
        try:
            rmbg = RemoveBg(REMOVE_BG_API_KEY, "removebg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            RBG_IMG_PATH = IMG_PATH + "_no_bg.png"
            await client.send_document(
                chat_id=message.chat.id,
                document=RBG_IMG_PATH,
                reply_to_message_id=ReplyCheck(message),
                disable_notification=True)
            await message.delete()
        except Exception:
            await message.edit("Something went wrong!\nCheck your usage.")
    else:
        await message.edit("Usage: reply to a photo to remove background!")