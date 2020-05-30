import asyncio
import requests

from pyrogram import Filters, Message
from nana import Command, app

__MODULE__ = "Nekobin"
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste using replied to message.

"""

@app.on_message(Filters.user("self") & Filters.command(["neko"], Command))
async def paste(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `neko (text) or neko (reply to a text)`")
        return
    await message.edit_text("`Pasting...`")
    if message.reply_to_message.message_id:
        splitter = message.text.split(None, 1)
        if len(splitter) == 1:
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            text = splitter[1]
    else:
        splitter = message.text.split(None, 1)
        if len(splitter) == 1:
            return
        else:
            text = splitter[1]
    try:
        key = requests.post('https://nekobin.com/api/documents', json={"content": text}).json().get('result').get('key')
    except requests.exceptions.RequestException as e:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
    else:
        reply_text = f'`Successfully pasted on` [Nekobin](https://nekobin.com/{key})'
        await message.edit_text(
            reply_text,
            disable_web_page_preview=True,
        )