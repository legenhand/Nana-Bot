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
    if message.reply_to_message:
        await message.edit_text("`Pasting...`")
        text = message.reply_to_message.text
        try:
            key = requests.post('https://nekobin.com/api/documents', json={"content": text}).json().get('result').get('key')
        except requests.exceptions.RequestException:
            await message.edit_text("`Pasting failed`")
            await asyncio.sleep(2)
            await message.delete()
        else:
            reply_text = f'`Successfully pasted on` [Nekobin](https://nekobin.com/{key})'
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )
    else:
        await message.edit_text("Usage: `neko (reply to a text)`")