import urbandict

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
		message.edit("Usage: `ud example`")
		return
	text = message.text.split(None, 1)[1]
	mean = urbandict.define(text)
	if len(mean) >= 0:
		teks = "**Result of {}**\n\n**{}**\n**Meaning:**\n`{}`\n\n**Example:**\n`{}`".format(text, mean[0]["word"].replace("unknown", ""), mean[0]["def"], mean[0]["example"])
		await client.edit_message_text(message.chat.id, message.message_id, teks)
	else:
		await client.edit_message_text(message.chat.id, message.message_id, "Result not found!")
