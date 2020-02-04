import pyrogram
import os

from gtts import gTTS
from nana import app, Command
from pyrogram import Filters

__MODULE__ = "Voice"
__HELP__ = """
Convert text to voice chat.
Currently avaiable for english only.

──「 **Voice** 」──
-> `voice (text)`
Convert text to voice by google tts
"""

# TODO setlang

@app.on_message(Filters.user("self") & Filters.command(["voice"], Command))
async def voice(client, message):
	if len(message.text.split()) == 1:
		await message.edit(bantuan)
		return
	await message.delete()
	await client.send_chat_action(message.chat.id, "record_audio")
	text = message.text.split(None, 1)[1]
	tts = gTTS(text, lang="en")
	tts.save('nana/cache/voice.mp3')
	if message.reply_to_message:
		await client.send_voice(message.chat.id, voice="nana/cache/voice.mp3", reply_to_message_id=message.reply_to_message.message_id)
	else:
		await client.send_voice(message.chat.id, voice="nana/cache/voice.mp3")
	await client.send_chat_action(message.chat.id, action="cancel")
	os.remove("nana/cache/voice.mp3")
