import asyncio
import os

import aiohttp
from pyrogram import filters

from nana import Command, app, AdminSettings, edrep
from nana.helpers.aiohttp_helper import AioHttp

__MODULE__ = "Nekobin"
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste using replied to message.

"""


@app.on_message(filters.user(AdminSettings) & filters.command("neko", Command))
async def paste(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    if message.reply_to_message.document and message.reply_to_message.document.file_size < 2 ** 20 * 10:
        var = os.path.splitext(message.reply_to_message.document.file_name)[1]
        print(var)
        path = await message.reply_to_message.download("nana/")
        with open(path, 'r') as doc:
            text = doc.read()
        os.remove(path)
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
        raw_url = f'https://nekobin.com/raw/{key}'
        reply_text = '**Nekofied:**\n'
        reply_text += f' - **Link**: {url}\n'
        reply_text += f' - **Raw**: {raw_url}'
        delete = True if len(message.command) > 1 and \
                         message.command[1] in ['d', 'del'] and \
                         message.reply_to_message.from_user.is_self else False
        if delete:
            await asyncio.gather(
                client.send_message(message.chat.id,
                                    reply_text,
                                    disable_web_page_preview=True
                                    ),
                message.reply_to_message.delete(),
                message.delete()
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )


@app.on_message(filters.user(AdminSettings) & filters.command(["gpaste"], Command))
async def get_paste_(_client, message):
    """fetches the content of a dogbin or nekobin URL."""
    link = message.reply_to_message.text
    if not link:
        await edrep(message, text="input not found!")
        return
    await edrep(message, text="`Getting paste content...`")
    format_view = 'https://del.dog/v/'
    if link.startswith(format_view):
        link = link[len(format_view):]
        raw_link = f'https://del.dog/raw/{link}'
    elif link.startswith("https://del.dog/"):
        link = link[len("https://del.dog/"):]
        raw_link = f'https://del.dog/raw/{link}'
    elif link.startswith("del.dog/"):
        link = link[len("del.dog/"):]
        raw_link = f'https://del.dog/raw/{link}'
    elif link.startswith("https://nekobin.com/"):
        link = link[len("https://nekobin.com/"):]
        raw_link = f'https://nekobin.com/raw/{link}'
    elif link.startswith("nekobin.com/"):
        link = link[len("nekobin.com/"):]
        raw_link = f'https://nekobin.com/raw/{link}'
    else:
        await edrep(message, text="Is that even a paste url?")
        return
    resp = await AioHttp().get_text(raw_link)
    await edrep(message, text=f"**URL content** :\n`{resp}`")