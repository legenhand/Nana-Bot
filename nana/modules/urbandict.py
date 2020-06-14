import json

import requests
from pyrogram import Filters

from nana import app, Command
from nana.helpers.string import replace_text

__MODULE__ = "Urban Dictionary"
__HELP__ = """
Search for urban dictionary

──「 **Urban Dictionary** 」──
-> `ud (text or reply to a word)`
Search urban for dictionary
"""


@app.on_message(Filters.me & Filters.command(["ud"], Command))
async def urban_dictionary(_client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `ud example`")
        return
    text = message.text.split(None, 1)[1]
    response = requests.get("http://api.urbandictionary.com/v0/define?term={}".format(text))
    if response.status_code == 200:
        data = response.json()
        word = json.dumps(data['list'][0]['word'])
        definition = json.dumps(data['list'][0]['definition'])
        example = json.dumps(data['list'][0]['example'])
        teks = "**Text: {}**\n**Meaning:**\n`{}`\n\n**Example:**\n`{}`".format(replace_text(word),
                                                                               replace_text(definition),
                                                                               replace_text(example))
        await message.edit(teks)
        return
    elif response.status_code == 404:
        await message.edit("Cannot connect to Urban Dictionary")
