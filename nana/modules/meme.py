import os
import random
import shutil
from difflib import get_close_matches
import re
import asyncio
import aiohttp
import requests
from pyrogram import Filters
from pyrogram.errors.exceptions import FloodWait

import nana.modules.meme_strings as meme_strings
from nana.helpers.PyroHelpers import ReplyCheck
from nana import app, Command

__MODULE__ = "Memes"
__HELP__ = """
This module can help you for generate memes and style text, just take a look and try in here!
Please note this can cause spams on group!

──「 **Spongebob Mocking** 」──
-> `mock (*text)`
Reply someone message, and mock his/her text! This will generate spongebob mocking sticker, for text use `mocktxt` instead.

──「 **Waifu Stickerizer** 」──
-> `waifu`
Reply someone message to Stickerize with Waifu text.

──「 **Senpai Stickerizer** 」──
-> `senpai`
Reply someone message to Stickerize with senpai text.

──「 **Stretch Text** 」──
-> `stretch`
streeetcchhh

──「 **Copy Pasta** 」──
-> `cp`
Reply someone message, then add randoms emoji to his/her text.

──「 **Scam** 」──
-> `scam`
Let bot decide action and time
-> `scam <action>`
User decides time/action, bot decides the other.
-> `scam <action> <time>`
User decides both action and time
Types: `'typing','upload_photo', 'record_video', 'upload_video', 'record_audio', 'upload_audio', 'upload_document', 'find_location','record_video_note', 'upload_video_note', 'choose_contact', 'playing'`

──「 **Mocking text** 」──
-> `mocktxt`
Mock someone message, text only.

──「 **Meme generator** 」──
-> `meme`
For get avaiable type, just send `meme`, to get example image of type, just send `meme (type)`.
To leave it blank, set text to _
Usage:
```meme (up text)
(down text)```

──「 **Vaporwave/Aestethic** 」──
-> `aes`
Convert your text to Vaporwave/Aestethic style.

──「 **Type Writer** 」──
-> `type`
Just a small command to make your keyboard become a typewriter.

──「 **Shrugs** 」──
-> `shg`
Free Shrugs? Anyone?...

──「 **Pat** 」──
-> `pat`
Free pats ^_^

──「 **Stylish edited text** 」──
-> `1` (forward)
-> `1a` (backward)
-> `2` (mocking)
-> `3` (typing message)
"""

# MOCK_SPONGE = "https://telegra.ph/file/c2a5d11e28168a269e136.jpg"
waifus = [20, 32, 33, 40, 41, 42, 58]
senpais = [37, 38, 48, 55]


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

@app.on_message(Filters.me & Filters.command(["pat"], Command))
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

@app.on_message(Filters.me & Filters.command(["scam"], Command))
async def scam(client, message):
    input_str = message.command
    if len(input_str) == 1:  # Let bot decide action and time
        scam_action = random.choice(meme_strings.option)
        scam_time = random.randint(30, 60)
    elif len(input_str) == 2:  # User decides time/action, bot decides the other.
        try:
            scam_action = str(input_str[1]).lower()
            scam_time = random.randint(30, 60)
        except ValueError:
            scam_action = random.choice(meme_strings.option)
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

@app.on_message(Filters.me & Filters.command(["shg"], Command))
async def shg(_client, message):
    await message.edit(random.choice(meme_strings.shgs))


@app.on_message(Filters.me & Filters.command(["spam"], Command))
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


@app.on_message(Filters.me & Filters.command(["owo"], Command))
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


@app.on_message(Filters.me & Filters.command(["waifu"], Command))
async def waifu(client, message):
    await message.delete()
    cmd = message.command
    waifu = ""
    if len(cmd) > 1:
        waifu = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        waifu = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`No text Given hence the waifu Ran Away.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results("Stickerizerbot", f"#{random.choice(waifus)}{waifu}")
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id = x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)


@app.on_message(Filters.me & Filters.command(["type"], Command))
async def type_writer(_client, message):
    cmd = message.command
    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`You didnt give any text to type :c`")
        await asyncio.sleep(2)
        await message.delete()
        return
    sleept = 0.1
    char = '_'
    old = ''
    await message.edit(char)
    await asyncio.sleep(sleept)
    for character in text:
        sleeptime = sleept / random.randint(1, 100)
        old += character
        typing_text = old + char
        try:
            await message.edit(typing_text)
            await asyncio.sleep(sleeptime)
            await message.edit(old)
            await asyncio.sleep(sleeptime)
        except FloodWait as y:
            await asyncio.sleep(y.x)


@app.on_message(Filters.me & Filters.command(["f"], Command))
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


@app.on_message(Filters.me & Filters.command(["senpai"], Command))
async def senpai(client, message):
    await message.delete()
    cmd = message.command
    senpai = ""
    if len(cmd) > 1:
        senpai = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        senpai = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`No text Given hence the senpai Ran Away.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    x = await client.get_inline_bot_results("Stickerizerbot", f"#{random.choice(senpais)}{senpai}")
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id = x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)


@app.on_message(Filters.me & Filters.command(["mock"], Command))
async def mock_spongebob(client, message):
    await message.delete()
    mock = message.reply_to_message.text
    x = await client.get_inline_bot_results("Stickerizerbot", f"#7{mock}")
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id = x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)


@app.on_message(Filters.me & Filters.command(["stretch"], Command))
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


@app.on_message(Filters.me & Filters.command(["cp"], Command))
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


@app.on_message(Filters.me & Filters.command(["mocktxt"], Command))
async def mock_text(client, message):
    if message.reply_to_message:
        teks = message.reply_to_message.text
        if teks is None:
            teks = message.reply_to_message.caption
            if teks is None:
                return
        pesan = await mocking_text(teks)
        await client.edit_message_text(message.chat.id, message.message_id, pesan)


@app.on_message(Filters.me & Filters.command(["1", "1a"], Command))
async def marquee(client, message):
    teks = message.text[3:] + " "
    jumlah = teks.count('') - 1
    if message.text[:3] == ".1a":
        teks = message.text[4:] + " "
        jumlah = teks.count('') - 1
        maju = True
    else:
        maju = False
    for _ in range(jumlah * 2):
        if maju:
            teks = teks[1] + teks[2:] + teks[0]
        else:
            teks = teks[-1] + teks[:-1]
        try:
            await client.edit_message_text(message.chat.id, message.message_id, teks, parse_mode="")
        except:
            pass


@app.on_message(Filters.me & Filters.command(["2"], Command))
async def dancedance(client, message):
    teks = list(message.text[3:])
    for _ in range(4):
        for i, ele in enumerate(teks):
            if i % 2 != 0:
                teks[i] = ele.upper()
        pesan = ""
        for x in range(len(teks)):
            pesan += teks[x]
        await client.edit_message_text(message.chat.id, message.message_id, pesan)
        teks = list(message.text[3:])
        for i, ele in enumerate(teks):
            if i % 2 == 0:
                teks[i] = ele.upper()
        pesan = ""
        for x in range(len(teks)):
            pesan += teks[x]
        await client.edit_message_text(message.chat.id, message.message_id, pesan)
        teks = list(message.text[3:])
    teks = message.text[3:]
    await client.edit_message_text(message.chat.id, message.message_id, teks.capitalize())


@app.on_message(Filters.me & Filters.command(["3"], Command))
async def typingmeme(_client, message):
    teks = message.text[3:]
    total = len(teks)
    for loop in range(total):
        try:
            await message.edit(teks[:loop + 1])
        except:
            pass


@app.on_message(Filters.me & Filters.command(["meme"], Command))
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
