from jikanpy import Jikan
from jikanpy.exceptions import APIException
from pyrogram import Filters
import asyncio

from nana.helpers.PyroHelpers import ReplyCheck
from nana import app, Command
from nana.helpers.string import replace_text

__MODULE__ = "MyAnimeList"

__HELP__ = """
Get information about anime, manga or characters from [MyAnimeList](https://myanimelist.net).

──「 **Anime** 」──
-> `anime <anime>`
returns information about the anime.

──「 **Character** 」──
-> `character <character>`
returns information about the character.

──「 **Manga** 」──
-> `manga <manga>`
returns information about the manga.

──「 **Upcoming Anime** 」──
-> `upcoming`
returns a list of new anime in the upcoming seasons.
"""

jikan = Jikan()

@app.on_message(Filters.me & Filters.command(["anime"], Command))
async def anime(client, message):
    cmd = message.command
    query = ""
    if len(cmd) > 1:
        query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        query = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`cant find anime.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    res = ""
    try:
        res = jikan.search("anime", query)
    except APIException:
        await message.edit("Error connecting to the API. Please try again!")
        return ""
    try:
        res = res.get("results")[0].get("mal_id") # Grab first result
    except APIException:
        await message.edit("Error connecting to the API. Please try again!")
        return ""
    if res:
        anime = jikan.anime(res)
        title = anime.get("title")
        japanese = anime.get("title_japanese")
        type = anime.get("type")
        duration = anime.get("duration")
        synopsis = anime.get("synopsis")
        source = anime.get("source")
        status = anime.get("status")
        episodes = anime.get("episodes")
        score = anime.get("score")
        rating = anime.get("rating")
        genre_lst = anime.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        studios = ""
        studio_lst = anime.get("studios")
        for studio in studio_lst:
            studios += studio.get("name") + ", "
        studios = studios[:-2]
        duration = anime.get("duration")
        premiered = anime.get("premiered")
        image_url = anime.get("image_url")
        url = anime.get("url")
    else:
        await message.edit("No results found!")
        return
    rep = f"<b>{title} ({japanese})</b>\n"
    rep += f"<b>Type:</b> <code>{type}</code>\n"
    rep += f"<b>Source:</b> <code>{source}</code>\n"
    rep += f"<b>Status:</b> <code>{status}</code>\n"
    rep += f"<b>Genres:</b> <code>{genres}</code>\n"
    rep += f"<b>Episodes:</b> <code>{episodes}</code>\n"
    rep += f"<b>Duration:</b> <code>{duration}</code>\n"
    rep += f"<b>Score:</b> <code>{score}</code>\n"
    rep += f"<b>Studio(s):</b> <code>{studios}</code>\n"
    rep += f"<b>Premiered:</b> <code>{premiered}</code>\n"
    rep += f"<b>Rating:</b> <code>{rating}</code>\n\n"
    rep += f"<a href='{image_url}'>\u200c</a>"
    rep += f"<i>{synopsis}</i>\n"
    rep += f'Read More: <a href="{url}">MyAnimeList</a>'
    await message.edit(rep)

@app.on_message(Filters.me & Filters.command(["character"], Command))
async def character(client, message):
    res = ""
    cmd = message.command
    query = ""
    if len(cmd) > 1:
        query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        query = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`cant find character.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    try:
        search = jikan.search("character", query).get("results")[0].get("mal_id")
    except APIException:
        message.edit("No results found!")
        return ""
    if search:
        try:
            res = jikan.character(search)
        except APIException:
            message.edit("Error connecting to the API. Please try again!")
            return ""
    if res:
        name = res.get("name")
        kanji = res.get("name_kanji")
        about = res.get("about")
        if len(about) > 4096:
            about = about[:4000] + "..."
        image = res.get("image_url")
        url = res.get("url")
        rep = f"<b>{name} ({kanji})</b>\n\n"
        rep += f"<a href='{image}'>\u200c</a>"
        rep += f"<i>{about}</i>\n"
        rep += f'Read More: <a href="{url}">MyAnimeList</a>'
        await message.edit(replace_text(rep))

@app.on_message(Filters.me & Filters.command(["manga"], Command))
async def manga(client, message):
    cmd = message.command
    query = ""
    if len(cmd) > 1:
        query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        query = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`cant find manga.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    res = ""
    manga = ""
    try:
        res = jikan.search("manga", query).get("results")[0].get("mal_id")
    except APIException:
        await message.edit("Error connecting to the API. Please try again!")
        return ""
    if res:
        try:
            manga = jikan.manga(res)
        except APIException:
            message.edit("Error connecting to the API. Please try again!")
            return ""
        title = manga.get("title")
        japanese = manga.get("title_japanese")
        type = manga.get("type")
        status = manga.get("status")
        score = manga.get("score")
        volumes = manga.get("volumes")
        chapters = manga.get("chapters")
        genre_lst = manga.get("genres")
        genres = ""
        for genre in genre_lst:
            genres += genre.get("name") + ", "
        genres = genres[:-2]
        synopsis = manga.get("synopsis")
        image = manga.get("image_url")
        url = manga.get("url")
        rep = f"<b>{title} ({japanese})</b>\n"
        rep += f"<b>Type:</b> <code>{type}</code>\n"
        rep += f"<b>Status:</b> <code>{status}</code>\n"
        rep += f"<b>Genres:</b> <code>{genres}</code>\n"
        rep += f"<b>Score:</b> <code>{score}</code>\n"
        rep += f"<b>Volumes:</b> <code>{volumes}</code>\n"
        rep += f"<b>Chapters:</b> <code>{chapters}</code>\n\n"
        rep += f"<a href='{image}'>\u200c</a>"
        rep += f"<i>{synopsis}</i>"
        rep += f'Read More: {url}'
        await message.edit(rep)

@app.on_message(Filters.me & Filters.command(["upcoming"], Command))
async def upcoming(_client, message):
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