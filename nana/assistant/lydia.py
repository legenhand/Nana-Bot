import asyncio
import random
import re

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI
from pyrogram import filters

import nana.modules.meme_strings as meme_strings
from nana import setbot, AdminSettings, lydia_api

lydia_status = False
coffeehouse_api = None
lydia = None
session = None
poki_uwu = False

@setbot.on_message(filters.user(AdminSettings) & filters.command(["lydia"]) & (filters.group | filters.private))
async def lydia_stats(_client, message):
    global lydia_status, coffeehouse_api, lydia, session
    if lydia_api == "":
        await message.reply("`lydia API key is not set!\nSet your lydia API key by adding Config Vars in heroku with "
                            "name lydia_api with value your lydia key API`")
        return
    if lydia_status:
        await message.reply("Turning off lydia...")
        asyncio.sleep(0.3)
        lydia_status = False
        await message.reply("Lydia will not reply your message")
    else:
        await message.reply("Turning on lydia...")
        try:
            coffeehouse_api = API(lydia_api)
            # Create Lydia instance
            lydia = LydiaAI(coffeehouse_api)
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
        except:
            await message.reply("Wrong lydia API key!")
            return
        lydia_status = True
        await message.reply("now Lydia will reply your message!")


@setbot.on_message(~filters.me & ~filters.edited & (filters.mentioned | filters.private), group=2)
async def lydia_settings(client, message):
    global lydia_status, session
    if lydia_status:
        await client.send_chat_action(chat_id=message.chat.id,action="typing")
        output = session.think_thought(message.text)
        await asyncio.sleep(0.3)
        if poki_uwu:
            reply_text = re.sub(r'[rl]', "w", output)
            reply_text = re.sub(r'[ｒｌ]', "ｗ", output)
            reply_text = re.sub(r'[RL]', 'W', reply_text)
            reply_text = re.sub(r'[ＲＬ]', 'Ｗ', reply_text)
            reply_text = re.sub(r'n([aeiouａｅｉｏｕ])', r'ny\1', reply_text)
            reply_text = re.sub(r'r([aeiouａｅｉｏｕ])', r'w\1', reply_text)
            reply_text = re.sub(r'ｎ([ａｅｉｏｕ])', r'ｎｙ\1', reply_text)
            reply_text = re.sub(r'N([aeiouAEIOU])', r'Ny\1', reply_text)
            reply_text = re.sub(r'Ｎ([ａｅｉｏｕＡＥＩＯＵ])', r'Ｎｙ\1', reply_text)
            reply_text = re.sub(r'\!+', ' ' + random.choice(meme_strings.faces), reply_text)
            reply_text = re.sub(r'！+', ' ' + random.choice(meme_strings.faces), reply_text)
            reply_text = reply_text.replace("ove", "uv")
            reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
            reply_text = reply_text.replace(".", ",,.")
            reply_text += ' ' + random.choice(meme_strings.faces)
            await message.reply_text(f"{reply_text.lower()}", quote=True)
        else:
            await message.reply_text(f"{output}", quote=True)
    else:
        return


@setbot.on_message(filters.user(AdminSettings) & filters.regex("^pokichan") & (filters.mentioned | filters.private))
async def lydia_uwu(client, message):
    global poki_uwu
    if poki_uwu:
        poki_uwu = False
    else:
        poki_uwu = True


