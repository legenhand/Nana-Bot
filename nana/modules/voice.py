import os

from gtts import gTTS
from pyrogram import Filters

from nana import app, Command

__MODULE__ = "Voice"
__HELP__ = """
Convert text to voice chat.

──「 **Voice** 」──
-> `voice (text)`
Convert text to voice by google 

──「 **Voice Language** 」──
-> `voicelang (lang_id)`
Set language of your voice,Some Available Voice lang:
`ID| Language  | ID| Language`
`af: Afrikaans | ar: Arabic
cs: Czech     | de: German  
el: Greek     | en: English
es: Spanish   | fr: French  
hi: Hindi     | id: Indonesian
is: Icelandic | it: Italian
ja: Japanese  | jw: Javanese
ko: Korean    | la: Latin   
my: Myanmar   | ne: Nepali  
nl: Dutch     | pt: Portuguese
ru: Russian   | su: Sundanese 
sv: Swedish   | th: Thai 
tl: Filipino  | tr: Turkish
vi: Vietname  |
zh-cn: Chinese (Mandarin/China)
zh-tw: Chinese (Mandarin/Taiwan)`
"""
lang = "en"  # Default Language for voice


@app.on_message(Filters.me & Filters.command(["voice"], Command))
async def voice(client, message):
    global lang
    if len(message.text.split()) == 1:
        await message.edit("Send text then change to audio")
        return
    await message.delete()
    await client.send_chat_action(message.chat.id, "record_audio")
    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang=lang)
    tts.save('nana/cache/voice.mp3')
    if message.reply_to_message:
        await client.send_voice(message.chat.id, voice="nana/cache/voice.mp3",
                                reply_to_message_id=message.reply_to_message.message_id)
    else:
        await client.send_voice(message.chat.id, voice="nana/cache/voice.mp3")
    await client.send_chat_action(message.chat.id, action="cancel")
    os.remove("nana/cache/voice.mp3")


@app.on_message(Filters.me & Filters.command(["voicelang"], Command))
async def voicelang(_client, message):
    global lang
    temp = lang
    lang = message.text.split(None, 1)[1]
    try:
        gTTS("tes", lang=lang)
    except:
        await message.edit("Wrong Language id !")
        lang = temp
        return
    await message.edit("Language Set to {}".format(lang))
