import requests
import asyncio
import re

import requests
from pyrogram import filters

from nana import app, Command, AdminSettings, BotUsername, edrep, Owner, setbot
from nana.helpers.PyroHelpers import ReplyCheck
from nana.modules.database import anime_db as sql

__MODULE__ = "Anilist"

__HELP__ = """
Get information about anime, manga or characters from [Anilist](https://anilist.co).

──「 **Anime** 」──
-> `anime <anime>`
returns information about the anime.

__Original Module by @Zero_cooll7870__

──「 **Character** 」──
-> `character <character>`
returns information about the character.

──「 **Manga** 」──
-> `manga <manga>`
returns information about the manga.

──「 **Airing** 」──
-> `airing <anime>`
To get airing time of the anime.

──「 **Favourite List** 」──
-> `favourite`
Get your favourite Anime list.

"""


def shorten(description, info='anilist.co'):
    ms_g = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        ms_g += f"\n**Description**: __{description}__[Read More]({info})"
    else:
        ms_g += f"\n**Description**: __{description}__"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


# time formatter from uniborg
def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]


airing_query = '''
    query ($id: Int,$search: String) { 
        Media (id: $id, type: ANIME,search: $search) { 
            id
            episodes
            title {
                romaji
                english
                native
            }
            nextAiringEpisode {
                airingAt
                timeUntilAiring
                episode
            } 
        }
    }
    '''

fav_query = """
query ($id: Int) { 
      Media (id: $id, type: ANIME) { 
        id
        title {
          romaji
          english
          native
        }
     }
}
"""

anime_query = '''
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''
character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               image {
                        large
               }
               description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) { 
      Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""


url = 'https://graphql.anilist.co'


@app.on_message(filters.user(AdminSettings) & filters.command("airing", Command))
async def anime_airing(_client, message):
    search_str = message.text.split(' ', 1)
    if len(search_str) == 1:
        await edrep(message, text='Format: `airing <anime name>`')
        return
    variables = {'search': search_str[1]}
    response = requests.post(
        url, json={'query': airing_query, 'variables': variables}).json()['data']['Media']
    ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response['nextAiringEpisode']:
        airing_time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        airing_time_final = t(airing_time)
        ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
    else:
        ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await edrep(message, text=ms_g)


@app.on_message(filters.user(AdminSettings) & filters.command("anime", Command))
async def anime_search(client, message):
    cmd = message.command
    mock = ""
    if len(cmd) > 1:
        mock = " ".join(cmd[1:])
    elif len(cmd) == 1:
        await edrep(message, text="`Format: anime <anime name>`")
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results(f"{BotUsername}", f"anime {mock}")
    await message.delete()
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id=x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)


@app.on_message(filters.user(AdminSettings) & filters.command("character", Command))
async def character_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'query': search}
    json = requests.post(url, json={'query': character_query, 'variables': variables}).json()['data'].get('Character', None)
    if json:
        ms_g = f"**{json.get('name').get('full')}**(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        ms_g += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await message.delete()
            await client.send_photo(message.chat.id, photo=image, caption=ms_g)
        else:
            await edrep(message, text=ms_g)


@app.on_message(filters.user(AdminSettings) & filters.command("manga", Command))
async def manga_search(client, message):
    search = message.text.split(' ', 1)
    if len(search) == 1:
        await message.delete()
        return
    search = search[1]
    variables = {'search': search}
    json = requests.post(url, json={'query': manga_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    ms_g = ''
    if json:
        title, title_native = json['title'].get(
            'romaji', False), json['title'].get('native', False)
        start_date, status, score = json['startDate'].get('year', False), json.get(
            'status', False), json.get('averageScore', False)
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f"(`{title_native}`)"
        if start_date:
            ms_g += f"\n**Start Date** - `{start_date}`"
        if status:
            ms_g += f"\n**Status** - `{status}`"
        if score:
            ms_g += f"\n**Score** - `{score}`"
        ms_g += '\n**Genres** - '
        for x in json.get('genres', []):
            ms_g += f"{x}, "
        ms_g = ms_g[:-2]

        image = json.get("bannerImage", False)
        ms_g += f"_{json.get('description', None)}_"
        if image:
            try:
                await message.delete()
                await client.send_photo(message.chat.id, photo=image, caption=ms_g)
            except:
                ms_g += f" [〽️]({image})"
                await edrep(message, text=ms_g)
        else:
            await edrep(message, text=ms_g)


@app.on_message(filters.user(AdminSettings) & filters.command("favourite", Command))
async def favourite_animelist(client, message):
    x = await client.get_inline_bot_results(f"{BotUsername}", f"favourite")
    await message.delete()
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id=x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)


async def addfav_callback(_, __, query):
    if re.match(r"addfav_", query.data):
        return True


async def remfav_callback(_, __, query):
    if re.match(r"remfav_", query.data):
        return True


@setbot.on_callback_query(filters.create(addfav_callback))
async def add_favorite(client, query):
    if query.from_user.id in AdminSettings:
        match = query.data.split("_")[1]
        add = sql.add_fav(Owner, match)
        if add:
            await query.answer('Added to Favourites', show_alert=True)
        else:
            await query.answer('Anime already Exists in Favourites', show_alert=True)
    else:
        await query.answer('You are not Allowed to Press this', show_alert=True)


@setbot.on_callback_query(filters.create(remfav_callback))
async def rem_favorite(client, query):
    if query.from_user.id in AdminSettings:
        sql.remove_fav(Owner)
        await setbot.edit_inline_text(query.inline_message_id,'Removed from Favourites')
    else:
        await query.answer('You are not Allowed to Press this', show_alert=True)