import asyncio
import os
from asyncio import sleep
from glob import iglob
from random import randint

import aiofiles
import aiohttp
from pyrogram import filters
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

from nana import app, Command, AdminSettings, edrep
from nana.helpers.PyroHelpers import ReplyCheck
from nana.helpers.aiohttp_helper import AioHttp

__MODULE__ = "Github"
__HELP__ = """
This module can help you find information about a github user!

──「 **Github User Info** 」──
-> `git (username)`
Finding information about a github user.

"""

@app.on_message(filters.user(AdminSettings) & filters.command("git", Command))
async def github(client, message):
    if len(message.text.split()) == 1:
            await edrep(message, text="Usage: `git (username)`")
            return
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await edrep(message, text="`" + username + " not found`")

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"**GitHub Info for {name}**"
                f"\n**Username:** `{username}`\n**Bio:** `{bio}`\n**Profile Link:** [Link]({url})"
                f"\n**Company:** `{company}`\n**Created at:** `{created_at}`"
                f"\n**Repository:** [Link](https://github.com/{username}?tab=repositories)"
            )
        url = f"https://ghchart.rshah.org/{username}"
        file_name = f"{randint(1, 999)}{username}"
        resp = await AioHttp.get_raw(url)
        f = await aiofiles.open(f"{file_name}.svg", mode='wb')
        await f.write(resp)
        await f.close()

        try:
            drawing = svg2rlg(f"{file_name}.svg")
            renderPM.drawToFile(drawing, f"{file_name}.png")
        except UnboundLocalError:
            await edrep(message, text="Username does not exist!")
            await sleep(2)
            await message.delete()
            return
        await asyncio.gather(
            client.send_photo(
            chat_id=message.chat.id,
            photo=f"{file_name}.png",
            caption=REPLY,
            reply_to_message_id=ReplyCheck(message)
            )
    )
    for file in iglob(f"{file_name}.*"):
        os.remove(file)