import asyncio
import requests

from pyrogram import Filters
from nana import Command, app

__MODULE__ = "Nekobin"
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste using replied to message.

"""

@app.on_message(Filters.me & Filters.command(["neko"], Command))
async def paste(_client, message):
    cmd = message.command

    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Usage: `neko (reply to a text)`")
        await asyncio.sleep(2)
        await message.delete()
        return
    # await message.edit_text("`Pasting...`")
    try:
        key = requests.post('https://nekobin.com/api/documents', json={"content": text}).json().get('result').get('key')
    except requests.exceptions.RequestException:
        await asyncio.sleep(2)
        await message.delete()
    else:
        reply_text = f'`Successfully pasted on` [Nekobin](https://nekobin.com/{key})'
        await message.edit_text(
            reply_text,
            disable_web_page_preview=True,
        )