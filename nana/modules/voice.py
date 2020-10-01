import asyncio
import os
from datetime import datetime

import requests
from gtts import gTTS
from pyrogram import filters

from nana import app, Command, IBM_WATSON_CRED_URL, IBM_WATSON_CRED_PASSWORD, AdminSettings, edrep
from nana.modules.downloads import download_reply_nocall

__MODULE__ = "TTS / STT"
__HELP__ = """
Convert text to voice chat.

──「 **Text-To-Speech** 」──
-> `tts (text)`
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

──「 **Speech-To-Text** 」──
-> `stt`
Reply to a voice message to output trascript
"""
lang = "en"  # Default Language for voice


@app.on_message(filters.user(AdminSettings) & filters.command("tts", Command))
async def voice(client, message):
    global lang
    cmd = message.command
    if len(cmd) > 1:
        v_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        v_text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="Usage: `reply to a message or send text arg to convert to voice`"
        )
        await asyncio.sleep(2)
        await message.delete()
        return
    await client.send_chat_action(message.chat.id, "record_audio")
    # noinspection PyUnboundLocalVariable
    tts = gTTS(v_text, lang=lang)
    tts.save("nana/cache/voice.mp3")
    await message.delete()
    if message.reply_to_message:
        await client.send_voice(
            message.chat.id,
            voice="nana/cache/voice.mp3",
            reply_to_message_id=message.reply_to_message.message_id,
        )
    else:
        await client.send_voice(message.chat.id, voice="nana/cache/voice.mp3")
    await client.send_chat_action(message.chat.id, action="cancel")
    os.remove("nana/cache/voice.mp3")


@app.on_message(filters.user(AdminSettings) & filters.command("voicelang", Command))
async def voicelang(_client, message):
    global lang
    temp = lang
    lang = message.text.split(None, 1)[1]
    try:
        gTTS("tes", lang=lang)
    except Exception as e:
        print(e)
        await edrep(message, text="Wrong Language id !")
        lang = temp
        return
    await edrep(message, text="Language Set to {}".format(lang))


@app.on_message(filters.user(AdminSettings) & filters.command("stt", Command))
async def speach_to_text(client, message):
    start = datetime.now()
    input_str = message.reply_to_message.voice
    if input_str:
        required_file_name = await download_reply_nocall(client, message)
        if IBM_WATSON_CRED_URL is None or IBM_WATSON_CRED_PASSWORD is None:
            await edrep(message, text="`no ibm watson key provided, aborting...`")
            await asyncio.sleep(3)
            await message.delete()
        else:
            headers = {
                "Content-Type": message.reply_to_message.voice.mime_type,
            }
            data = open(required_file_name, "rb").read()
            response = requests.post(
                IBM_WATSON_CRED_URL + "/v1/recognize",
                headers=headers,
                data=data,
                auth=("apikey", IBM_WATSON_CRED_PASSWORD),
            )
            r = response.json()
            if "results" in r:
                # process the json to appropriate string format
                results = r["results"]
                transcript_response = ""
                transcript_confidence = ""
                for alternative in results:
                    alternatives = alternative["alternatives"][0]
                    transcript_response += " " + str(alternatives["transcript"])
                    transcript_confidence += (
                        " " + str(alternatives["confidence"])
                    )
                end = datetime.now()
                ms = (end - start).seconds
                if transcript_response != "":
                    string_to_show = f"""
<b>TRANSCRIPT</b>:
<pre>{transcript_response}<pre>

<b>Time Taken</b>: <pre>{ms} seconds<pre>
<b>Confidence</b>: <pre>{transcript_confidence}<pre>
                                    """
                else:
                    string_to_show = f"<pre>Time Taken<pre>: {ms} seconds\n<pre>No Results Found<pre>"
                await edrep(message, text=string_to_show, parse_mode='html')
            else:
                await edrep(message, text=r["error"])
            # now, remove the temporary file
            os.remove(required_file_name)
    else:
        await edrep(message, text="`Reply to a voice message`")
        await asyncio.sleep(3)
        await message.delete()
