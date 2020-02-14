import requests
import json


from nana import app, Command
from pyrogram import Filters

__MODULE__ = "Urban Dictionary"
__HELP__ = """
Search for urban dictionary

──「 **Urban Dictionary** 」──
-> `ud (text)`
Search urban for dictionary
"""

@app.on_message(Filters.user("self") & Filters.command(["ud"], Command))
async def urban_dictionary(client, message):
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
		teks = "**Result of {}**\n\n**{}**\n**Meaning:**\n`{}`\n\n**Example:**\n`{}`".format(text,word,definition.replace("[","").replace("]","").replace("\"","").replace("\\",""),example.replace("[","").replace("]","").replace("\"","").replace("\\","") )
		await message.edit(teks)
		return
	elif response.status_code == 404:
		await message.edit("Cannot connect to Urban Dictionary")