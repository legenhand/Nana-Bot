import jikanpy
import asyncio

from pyrogram import Filters

from nana.helpers.PyroHelpers import ReplyCheck
from nana import app, Command
from nana.helpers.string import replace_text
from nana.helpers.anime import get_anime_manga, getBannerLink

__MODULE__ = "MyAnimeList"

__HELP__ = """
Get information about anime, manga or characters from [MyAnimeList](https://myanimelist.net).

──「 **Upcoming Anime** 」──
-> `upcoming`
returns a list of new anime in the upcoming seasons.
"""

@app.on_message(Filters.me & Filters.command(["upcoming"], Command))
async def upcoming(_client, message):
    jikan = jikanpy.jikan.Jikan()
    rep = "<b>Upcoming anime</b>\n"
    later = jikan.season_later()
    anime = later.get("anime")
    for new in anime:
        name = new.get("title")
        url = new.get("url")
        rep += f"• <a href='{url}'>{name}</a>\n"
        if len(rep) > 1000:
            break
    await message.edit(rep, parse_mode='html')