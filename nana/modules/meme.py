import asyncio
import os
import random
import re
import shutil
from difflib import get_close_matches

import aiohttp
import requests
from pyrogram import filters

import nana.modules.meme_strings as meme_strings
from nana import app, Command
from nana.helpers.PyroHelpers import ReplyCheck

__MODULE__ = "Memes"
__HELP__ = """
This module can help you for generate memes and style text, just take a look and try in here!

──「 **Stretch Text** 」──
-> `str`
stretch text

──「 **Copy Pasta** 」──
-> `cp`
add randoms emoji to his/her text.

──「 **Scam** 」──
-> `scam <action>`
User decides time/action, bot decides the other.

scame types: `'typing','upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio', 'upload_document', 'find_location','record_video_note', 'upload_video_note', 'choose_contact', 'playing'`

──「 **Mock text** 」──
-> `mocktxt`
Mock someone with text.

──「 **Meme generator** 」──
-> `meme`
For get avaiable type, just send `meme`, just send `meme (type)`.
To leave it blank, set text to _
Usage:
```meme (up text)
(down text)```

──「 **Vaporwave/Aestethic** 」──
-> `aes`
Convert your text to Vaporwave.

──「 **Shrugs** 」──
-> `shg`
Free Shrugs? Anyone?...

──「 **Pat** 」──
-> `pat`
pat gifs

──「 **TypeWriter** 」──
-> `type`
typing message
"""


async def mocking_text(text):
    teks = list(text)
    for i, ele in enumerate(teks):
        if i % 2 != 0:
            teks[i] = ele.upper()
        else:
            teks[i] = ele.lower()
    pesan = ""
    for x in range(len(teks)):
        pesan += teks[x]
    return pesan


@app.on_message(filters.me & filters.command(["pat"], Command))
async def pat(client, message):
    URL = "https://some-random-api.ml/animu/pat"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.edit("`no Pats for u :c")
            result = await request.json()
            url = result.get("link", None)
            await message.delete()
            await client.send_video(message.chat.id, url,
                                    reply_to_message_id=ReplyCheck(message)
                                    )


@app.on_message(filters.me & filters.command(["scam"], Command))
async def scam(client, message):
    input_str = message.command
    if len(input_str) == 1:  # Let bot decide action and time
        scam_action = random.choice(meme_strings.options)
        scam_time = random.randint(30, 60)
    elif len(input_str) == 2:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(input_str[1]).lower()
            scam_time = random.randint(30, 60)
        except ValueError:
            scam_action = random.choice(meme_strings.options)
            scam_time = int(input_str[1])
    elif len(input_str) == 3:  # User decides both action and time
        scam_action = str(input_str[1]).lower()
        scam_time = int(input_str[2])
    else:
        await message.edit("`Invalid Syntax !!`")
        return
    try:
        if scam_time > 0:
            chat_id = message.chat.id
            await message.delete()
            count = 0
            while count <= scam_time:
                await client.send_chat_action(chat_id, scam_action)
                await asyncio.sleep(5)
                count += 5
    except Exception:
        return


@app.on_message(filters.me & filters.command(["shg"], Command))
async def shg(_client, message):
    await message.edit(random.choice(meme_strings.shgs))


@app.on_message(filters.me & filters.command(["spam"], Command))
async def spam(client, message):
    await message.delete()
    times = message.command[1]
    to_spam = ' '.join(message.command[2:])
    if message.chat.type in ['supergroup', 'group']:
        for _ in range(int(times)):
            await client.send_message(message.chat.id, to_spam, reply_to_message_id=ReplyCheck(message))
            await asyncio.sleep(0.20)

    if message.chat.type == "private":
        for _ in range(int(times)):
            await client.send_message(message.chat.id, to_spam)
            await asyncio.sleep(0.20)


@app.on_message(filters.me & filters.command(["owo"], Command))
async def owo(_client, message):
    cmd = message.command
    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`cant uwu the void.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    reply_text = re.sub(r'[rl]', "w", text)
    reply_text = re.sub(r'[ｒｌ]', "ｗ", text)
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
    reply_text += ' ' + random.choice(meme_strings.faces)
    await message.edit(reply_text)


@app.on_message(filters.me & filters.command(["f"], Command))
async def pay_respecc(_client, message):
    cmd = message.command
    paytext = ""
    if len(cmd) > 1:
        paytext = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        paytext = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Press F to Pay Respecc`")
        await asyncio.sleep(2)
        await message.delete()
        return
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2
    )
    await message.edit(pay)


@app.on_message(filters.me & filters.command(["str"], Command))
async def stretch(_client, message):
    cmd = message.command
    stretch_text = ""
    if len(cmd) > 1:
        stretch_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        stretch_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Giiiiiiiv sooooooomeeeeeee teeeeeeext!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    count = random.randint(3, 10)
    reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                        stretch_text)
    await message.edit(reply_text)


@app.on_message(filters.me & filters.command(["cp"], Command))
async def haha_emojis(_client, message):
    if message.reply_to_message.message_id:
        teks = message.reply_to_message.text
        reply_text = random.choice(meme_strings.emojis)
        b_char = random.choice(teks).lower()
        for c in teks:
            if c == " ":
                reply_text += random.choice(meme_strings.emojis)
            elif c in meme_strings.emojis:
                reply_text += c
                reply_text += random.choice(meme_strings.emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(meme_strings.emojis)
        await message.edit(reply_text)


@app.on_message(filters.me & filters.command(["mocktxt"], Command))
async def mock_text(client, message):
    if message.reply_to_message:
        teks = message.reply_to_message.text
        if teks is None:
            teks = message.reply_to_message.caption
            if teks is None:
                return
        pesan = await mocking_text(teks)
        await client.edit_message_text(message.chat.id, message.message_id, pesan)


@app.on_message(filters.me & filters.command(["type"], Command))
async def typingmeme(_client, message):
    teks = message.text[3:]
    total = len(teks)
    for loop in range(total):
        try:
            await message.edit(teks[:loop + 1])
        except:
            pass


@app.on_message(filters.me & filters.command(["meme"], Command))
async def meme_gen(client, message):
    meme_types = requests.get(
        "https://raw.githubusercontent.com/legenhand/Nana-Bot/master/nana/helpers/memes.json").json()
    if len(message.text.split()) <= 2:
        if len(message.text.split()) == 2:
            closematch = get_close_matches(message.text.split(None, 1)[1], list(meme_types))
            text = "Search result:\n"
            for x in closematch:
                text += "\n`{}`\n-> **{}**\n-> [Example]({})\n".format(x, meme_types[x]['title'],
                                                                       meme_types[x]['example'])
            await message.edit(text)
        else:
            await message.edit("Avaiable type: `{}`".format("`, `".join(list(meme_types))))
        return
    memetype = message.text.split(None, 2)[1]
    if memetype not in list(meme_types):
        await message.edit("Unknown type!")
        return
    await message.delete()
    sptext = message.text.split(None, 2)[2].split("\n")
    if len(sptext) == 1:
        text1 = "_"
        text2 = sptext[0]
    else:
        text1 = sptext[0]
        text2 = sptext[1]
    getimg = requests.get("https://memegen.link/{}/{}/{}.jpg?font=impact".format(memetype, text1, text2), stream=True)
    if getimg.status_code == 200:
        with open("nana/cache/meme.png", 'wb') as f:
            getimg.raw.decode_content = True
            shutil.copyfileobj(getimg.raw, f)
        if message.reply_to_message:
            await client.send_sticker(message.chat.id, "nana/cache/meme.png",
                                      reply_to_message_id=message.reply_to_message.message_id)
        else:
            await client.send_sticker(message.chat.id, "nana/cache/meme.png", reply_to_message_id=message.message_id)
        os.remove("nana/cache/meme.png")
