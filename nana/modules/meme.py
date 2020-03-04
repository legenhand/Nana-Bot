import os
import random
import shutil
import textwrap
from difflib import get_close_matches

import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Filters

from nana import app, Command

__MODULE__ = "Memes"
__HELP__ = """
This module can help you for generate memes and style text, just take a look and try in here!
Please note this can cause spams on group!

──「 **Spongebob Mocking** 」──
-> `mock (*text)`
Reply someone message, and mock his/her text! This will generate spongebob mocking sticker, for text use `mocktxt` instead.

──「 **Emoji insertion** 」──
-> `😂`
Reply someone message, then add randoms emoji to his/her text.

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

──「 **Stylish edited text** 」──
-> `1` (forward)
-> `1a` (backward)
-> `2` (mocking)
-> `3` (typing message)
"""

MOCK_SPONGE = "https://telegra.ph/file/c2a5d11e28168a269e136.jpg"


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


@app.on_message(Filters.user("self") & Filters.command(["mock"], Command))
async def mock_spongebob(client, message):
    await message.delete()
    if message.reply_to_message:
        splitter = message.text.split(None, 1)
        if len(splitter) == 1:
            text = message.reply_to_message.text or message.reply_to_message.caption
        else:
            text = splitter[1]
    else:
        splitter = message.text.split(None, 1)
        if len(splitter) == 1:
            return
        else:
            text = splitter[1]

    getimg = requests.get(MOCK_SPONGE, stream=True)
    with open("nana/cache/sponge.png", 'wb') as f:
        getimg.raw.decode_content = True
        shutil.copyfileobj(getimg.raw, f)

    pesan = await mocking_text(text)
    para = textwrap.wrap(pesan, width=50)
    im = Image.open("nana/cache/sponge.png")
    max_w, max_h = im.size
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('nana/helpers/IMPACT.TTF', 35)
    newline = 0
    for line in para:
        newline += 1.25
    current_h, pad = (max_h / 1.25) + newline, 6
    x, y = 3, 3
    for line in para:
        w, h = draw.textsize(line, font=font)
        # stroke
        draw.text(((max_w - w) / 2 - x, current_h - y), line, font=font, fill=(0, 0, 0, 255))
        draw.text(((max_w - w) / 2 + x, current_h - y), line, font=font, fill=(0, 0, 0, 255))
        draw.text(((max_w - w) / 2 - x, current_h + y), line, font=font, fill=(0, 0, 0, 255))
        draw.text(((max_w - w) / 2 + x, current_h + y), line, font=font, fill=(0, 0, 0, 255))
        # Teks
        draw.text(((max_w - w) / 2, current_h), line, font=font, fill=(255, 255, 255, 255))
        current_h += h + pad
    im.save('nana/cache/sponge.png')
    if message.reply_to_message:
        await client.send_sticker(message.chat.id, "nana/cache/sponge.png",
                                  reply_to_message_id=message.reply_to_message.message_id)
    else:
        await client.send_sticker(message.chat.id, "nana/cache/sponge.png")
    os.remove("nana/cache/sponge.png")


@app.on_message(Filters.user("self") & Filters.command(["😂"], Command))
async def haha_emojis(client, message):
    if message.reply_to_message.message_id:
        teks = message.reply_to_message.text
        emojis = ["😂", "😂", "👌", "✌️", "💞", "👍", "👌", "💯", "🎶", "👀", "😂", "👓", "👏", "👐", "🍕", "💥", "🍴",
                  "💦", "💦", "🍑", "🍆", "😩", "😏", "👉👌", "👀", "👅", "😩", "🚰"]
        reply_text = random.choice(emojis)
        b_char = random.choice(teks).lower()
        for c in teks:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                if bool(random.getrandbits(1)):
                    reply_text += c.upper()
                else:
                    reply_text += c.lower()
        reply_text += random.choice(emojis)
        await message.edit(reply_text)


@app.on_message(Filters.user("self") & Filters.command(["mocktxt"], Command))
async def mock_text(client, message):
    if message.reply_to_message:
        teks = message.reply_to_message.text
        if teks is None:
            teks = message.reply_to_message.caption
            if teks is None:
                return
        pesan = await mocking_text(teks)
        await client.edit_message_text(message.chat.id, message.message_id, pesan)


@app.on_message(Filters.user("self") & Filters.command(["1", "1a"], Command))
async def marquee(client, message):
    teks = message.text[3:] + " "
    jumlah = teks.count('') - 1
    if message.text[:3] == ".1a":
        teks = message.text[4:] + " "
        jumlah = teks.count('') - 1
        maju = True
    else:
        maju = False
    for loop in range(jumlah * 2):
        if maju:
            teks = teks[1] + teks[2:] + teks[0]
        else:
            teks = teks[-1] + teks[:-1]
        try:
            await client.edit_message_text(message.chat.id, message.message_id, teks, parse_mode="")
        except:
            pass


@app.on_message(Filters.user("self") & Filters.command(["2"], Command))
async def dancedance(client, message):
    teks = list(message.text[3:])
    for loop in range(4):
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


@app.on_message(Filters.user("self") & Filters.command(["3"], Command))
async def typingmeme(client, message):
    teks = message.text[3:]
    total = len(teks)
    for loop in range(total):
        try:
            await message.edit(teks[:loop + 1])
        except:
            pass


@app.on_message(Filters.user("self") & Filters.command(["meme"], Command))
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
