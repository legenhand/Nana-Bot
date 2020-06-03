import datetime
import html
import textwrap
import bs4
import jikanpy
import requests
import asyncio

from pyrogram import Filters

from nana.helpers.PyroHelpers import ReplyCheck
from nana import app, Command

def replace_text(text):
        return text.replace("\"", "").replace("\\r", "").replace("\\n", "\n").replace(
            "\\", "")

def getPosterLink(mal):
    # grab poster from kitsu
    kitsu = getKitsu(mal)
    image = requests.get(f'https://kitsu.io/api/edge/anime/{kitsu}').json()
    return image['data']['attributes']['posterImage']['original']

def getKitsu(mal):
    # get kitsu id from mal id
    link = f'https://kitsu.io/api/edge/mappings?filter[external_site]=myanimelist/anime&filter[external_id]={mal}'
    result = requests.get(link).json()['data'][0]['id']
    link = f'https://kitsu.io/api/edge/mappings/{result}/item?fields[anime]=slug'
    kitsu = requests.get(link).json()['data']['id']
    return kitsu

def getBannerLink(mal, kitsu_search=True):
    # try getting kitsu backdrop
    if kitsu_search:
        kitsu = getKitsu(mal)
        image = f'http://media.kitsu.io/anime/cover_images/{kitsu}/original.jpg'
        response = requests.get(image)
        if response.status_code == 200:
            return image
    # try getting anilist banner
    query = """
    query ($idMal: Int){
        Media(idMal: $idMal){
            bannerImage
        }
    }
    """
    data = {'query': query, 'variables': {'idMal': int(mal)}}
    image = requests.post('https://graphql.anilist.co', json=data).json()['data']['Media']['bannerImage']
    if image:
        return image
    return getPosterLink(mal)

def get_anime_manga(mal_id, search_type, user_id):
    jikan = jikanpy.jikan.Jikan()
    if search_type == "anime_anime":
        result = jikan.anime(mal_id)
        image = getBannerLink(mal_id)
        studio_string = ', '.join([studio_info['name'] for studio_info in result['studios']])
        producer_string = ', '.join([producer_info['name'] for producer_info in result['producers']])
    elif search_type == "anime_manga":
        result = jikan.manga(mal_id)
        image = result['image_url']
    caption = f"<a href=\'{result['url']}\'>{result['title']}</a>"
    if result['title_japanese']:
        caption += f" ({result['title_japanese']})\n"
    else:
        caption += "\n"
    alternative_names = []
    if result['title_english'] is not None:
        alternative_names.append(result['title_english'])
    alternative_names.extend(result['title_synonyms'])
    if alternative_names:
        alternative_names_string = ", ".join(alternative_names)
        caption += f"\n<b>Also known as</b>: <code>{alternative_names_string}</code>"
    genre_string = ', '.join([genre_info['name'] for genre_info in result['genres']])
    if result['synopsis'] is not None:
        synopsis = result['synopsis'].split(" ", 60)
        try:
            synopsis.pop(60)
        except IndexError:
            pass
        synopsis_string = ' '.join(synopsis) + "..."
    else:
        synopsis_string = "Unknown"
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    if search_type == "anime_anime":
        caption += textwrap.dedent(f"""
        <b>Type</b>: <code>{result['type']}</code>
        <b>Status</b>: <code>{result['status']}</code>
        <b>Aired</b>: <code>{result['aired']['string']}</code>
        <b>Episodes</b>: <code>{result['episodes']}</code>
        <b>Score</b>: <code>{result['score']}</code>
        <b>Premiered</b>: <code>{result['premiered']}</code>
        <b>Duration</b>: <code>{result['duration']}</code>
        <b>Genres</b>: <code>{genre_string}</code>
        <b>Studios</b>: <code>{studio_string}</code>
        <b>Producers</b>: <code>{producer_string}</code>
        📖 <b>Synopsis</b>: {synopsis_string} <a href='{result['url']}'>read more</a>
        <i>Search an encode on..</i>
        """)
    elif search_type == "anime_manga":
        caption += textwrap.dedent(f"""
        <b>Type</b>: <code>{result['type']}</code>
        <b>Status</b>: <code>{result['status']}</code>
        <b>Volumes</b>: <code>{result['volumes']}</code>
        <b>Chapters</b>: <code>{result['chapters']}</code>
        <b>Score</b>: <code>{result['score']}</code>
        <b>Genres</b>: <code>{genre_string}</code>
        📖 <b>Synopsis</b>: {synopsis_string}
        """)
    related = result['related']
    mal_url = result['url']
    prequel_id, sequel_id = None, None

    if "Prequel" in related:
        try:
            prequel_id = related["Prequel"][0]["mal_id"]
        except IndexError:
            pass
    if "Sequel" in related:
        try:
            sequel_id = related["Sequel"][0]["mal_id"]
        except IndexError:
            pass
    if search_type == "anime_anime":
        kaizoku = f"https://animekaizoku.com/?s={result['title']}"
        kayo = f"https://animekayo.com/?s={result['title']}"
    return caption, image

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
        if character[entity] == None:
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
async def upcoming(client, message):
    jikan = jikanpy.jikan.Jikan()
    upcoming = jikan.top('anime', page=1, subtype="upcoming")

    upcoming_list = [entry['title'] for entry in upcoming['top']]
    upcoming_message = ""

    for entry_num in range(len(upcoming_list)):
        if entry_num == 10:
            break
        upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

    await message.edit(upcoming_message)