import asyncio
import aiohttp

from pyrogram import Filters
from nana import Command, app

__MODULE__ = "Nekobin"
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste using replied to message.

"""

@app.on_message(Filters.me & Filters.command(["neko"], Command))
async def paste(client, message):
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
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    'https://nekobin.com/api/documents',
                    json={"content": text},
                    timeout=3
            ) as response:
                key = (await response.json())["result"]["key"]
    except Exception:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f'https://nekobin.com/{key}'
        reply_text = f'Nekofied to [Nekobin]({url})'
        delete = True if len(message.command) > 1 and \
                         message.command[1] in ['d', 'del'] and \
                         message.reply_to_message.from_user.is_self else False
        if delete:
            await asyncio.gather(
                client.send_message(message.chat.id, reply_text, disable_web_page_preview=True),
                message.reply_to_message.delete(),
                message.delete()
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )