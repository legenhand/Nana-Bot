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

# upcomming
jikan = jikanpy.jikan.Jikan()
upcoming = jikan.top('anime', page=1, subtype="upcoming")

upcoming_list = [entry['title'] for entry in upcoming['top']]
upcoming_message = ""

for entry_num in range(len(upcoming_list)):
    if entry_num == 10:
        break
    upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

await message.edit(upcoming_message)

def replace_text(text):
        return text.replace("\"", "").replace("\\r", "").replace("\\n", "\n").replace(
            "\\", "")