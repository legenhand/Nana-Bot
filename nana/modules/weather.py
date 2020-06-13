from html import escape

import requests
from pyrogram import Filters

from nana import app, Command, lang_code

__MODULE__ = "Weather"
__HELP__ = """
Get current weather in your location

──「 **Weather** 」──
-> `weather (location)`
Get current weather in your location.
Powered by `wttr.in`
"""


# TODO: Add more custom args?

@app.on_message(Filters.me & Filters.command(["weather"], Command))
async def weather(_client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `weather Maldives`")
        return
    location = message.text.split(None, 1)[1]
    h = {'user-agent': 'httpie'}
    a = requests.get(f"https://wttr.in/{location}?mnTC0&lang={lang_code}", headers=h)
    if "Sorry, we processed more than 1M requests today and we ran out of our datasource capacity." in a.text:
        await message.edit("Sorry, location not found!")
        return
    weather = f"<code>{escape(a.text)}</code>"
    await message.edit(weather, parse_mode='html')
