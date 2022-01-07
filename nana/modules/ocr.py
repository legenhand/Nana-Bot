import os

import requests
from pyrogram import filters

from nana import app, Command, AdminSettings, edrep

__MODULE__ = "OCR"
__HELP__ = """
Read Texts from photos and Stickers

──「 **OCR** 」──
-> `ocr (lang)`
Read texts from an image or photo.

"""


OCR_SPACE_API_KEY = '30dd97e2b588957'
async def ocr_space_file(filename,overlay=False,api_key=OCR_SPACE_API_KEY,language='eng'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
    }
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.json()


@app.on_message(filters.user(AdminSettings) & filters.command("ocr", Command))
async def ocr(client, message):
    cmd = message.command
    lang_code = ''
    if len(cmd) > 1:
        lang_code = " ".join(cmd[1:])
    elif len(cmd) == 1:
        lang_code = 'eng'
    replied = message.reply_to_message
    if not replied:
        await message.delete()
        return
    if replied.video:
        await message.delete()
        return
    if replied.document:
        await message.delete()
        return
    if replied.voice:
        await message.delete()
        return
    if replied.audio:
        await message.delete()
        return
    if replied.photo:
        reply_p = replied.photo
    elif replied.sticker:
        reply_p = replied.sticker
    downloaded_file_name = await client.download_media(reply_p, 'nana/cache/file.png')
    test_file = await ocr_space_file(filename=downloaded_file_name,language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException as e:
        await edrep(message, text=e)
    else:
        if ParsedText == 'ParsedResults':
            await message.delete()
            return
        else:
            await edrep(message, text=f"`{ParsedText}`")
    os.remove(downloaded_file_name)