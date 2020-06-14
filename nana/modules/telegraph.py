import os
from telegraph import upload_file

from pyrogram import Filters
from nana import Command, app

__MODULE__ = "Telegra.ph"
__HELP__ = """
Paste Media Documents on Telegra.ph

──「 **Telegra.ph** 」──
-> `telegraph (reply to a media)`
Reply to Media as args to upload it to telegraph.
- Supported Media Types (.jpg, .jpeg, .png, .gif, .mp4)

"""


@app.on_message(Filters.me & Filters.command(["telegraph"], Command))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.edit("reply to a supported media file")
        return
    if not ((replied.photo and replied.photo.file_size <= 5242880)
            or (replied.animation and replied.animation.file_size <= 5242880)
            or (replied.video and replied.video.file_name.endswith('.mp4')
                and replied.video.file_size <= 5242880)
            or (replied.document
                and replied.document.file_name.endswith(
                    ('.jpg', '.jpeg', '.png', '.gif', '.mp4'))
                and replied.document.file_size <= 5242880)):
        await message.edit("not supported!")
        return
    download_location = await client.download_media(message=message.reply_to_message,file_name='root/nana/')
    await message.edit("`passing to telegraph...`")
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.edit(document)
    else:
        await message.edit(f"**Document passed to: [Telegra.ph](https://telegra.ph{response[0]})**")
    finally:
        os.remove(download_location)