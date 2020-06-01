import os
import time
from datetime import datetime

from removebg import RemoveBg
from pyrogram import Filters
from nana import app, Command, remove_bg_api

DOWN_PATH = '/root/nana/'

REMOVE_BG_API_KEY = remove_bg_api

IMG_PATH = DOWN_PATH + "image.jpg"

@app.on_message(Filters.user("self") & Filters.command(["lastfm"], Command))
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
        await message.edit(f"Removing Background...")
        try:
            rmbg = RemoveBg(REMOVE_BG_API_KEY, "removebg_error.log")
            rmbg.remove_background_from_img_file(IMG_PATH)
            RBG_IMG_PATH = IMG_PATH + "_no_bg.png"
            await client.send_document(
                chat_id=message.chat.id,
                document=RBG_IMG_PATH,
                disable_notification=True)
            await message.delete()
        except Exception:
            await message.edit("Something went wrong!\nCheck your usage.")
    else:
        await message.edit("Usage: reply to a photo to remove background!")