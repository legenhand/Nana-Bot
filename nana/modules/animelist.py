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


@app.on_message(Filters.me & Filters.command(["manga"], Command))
async def manga(client, message):
    cmd = message.command
    search_query = ""
    if len(cmd) > 1:
        search_query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        search_query = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Usage: `anime`")
        await asyncio.sleep(2)
        await message.delete()
        return
    await message.delete()
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("manga", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_manga", message.from_user.id)
    await client.send_photo(message.chat.id, photo=image,
                                caption=caption
                            )


@app.on_message(Filters.me & Filters.command(["anime"], Command))
async def anime(client, message):
    cmd = message.command
    search_query = ""
    if len(cmd) > 1:
        search_query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        search_query = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Usage: `anime`")
        await asyncio.sleep(2)
        await message.delete()
        return
    await message.delete()
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("anime", search_query)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_anime", message.from_user.id)
    try:
        await client.send_photo(photo=image,
                                caption=caption
                            )
    except:
        image = getBannerLink(first_mal_id, False)
        await client.send_photo(message.chat.id, photo=image,
                                caption=caption
                            )


@app.on_message(Filters.me & Filters.command(["character"], Command))
async def character(client, message):
    cmd = message.command
    search_query = ""
    if len(cmd) > 1:
        search_query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        search_query = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Usage: `character`")
        await asyncio.sleep(2)
        await message.delete()
        return
    await message.delete()
    jikan = jikanpy.jikan.Jikan()
    try:
        search_result = jikan.search("character", search_query)
    except jikanpy.APIException:
        await message.edit("Character not found.")
        return
    first_mal_id = search_result["results"][0]["mal_id"]
    character = jikan.character(first_mal_id)
    caption = f"[{character['name']}]({character['url']})"
    if character['name_kanji'] != "Japanese":
        caption += f" ({character['name_kanji']})\n"
    else:
        caption += "\n"

    if character['nicknames']:
        nicknames_string = ", ".join(character['nicknames'])
        caption += f"\n**Nicknames** : `{nicknames_string}`"
    about = character['about'].split(" ", 60)
    try:
        about.pop(60)
    except IndexError:
        pass
    about_string = ' '.join(about)
    mal_url = search_result["results"][0]['url']
    for entity in character:
        if character[entity] is None:
            character[entity] = "Unknown"
    caption += f"\n**About**: {about_string}"
    caption += f" [Read More]({mal_url})..."
    await client.send_photo(message.chat.id,
                            photo=character['image_url'],
                            caption=replace_text(caption),
                            reply_to_message_id=ReplyCheck(message),
                            parse_mode='markdown'
                        )


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