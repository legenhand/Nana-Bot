import asyncio
import os
import random
import re
import subprocess

import aiohttp
from pyrogram import filters
from pyrogram.raw import functions

import nana.modules.meme_strings as meme_strings
from nana import app, Command, AdminSettings, edrep
from nana.helpers.PyroHelpers import ReplyCheck

__MODULE__ = "Memes"
__HELP__ = """
This module can help you for generate memes and style text, just take a look and try in here!

──「 **Stretch Text** 」──
-> `str`
__stretch text__

──「 **Copy Pasta** 」──
-> `cp`
__add randoms emoji to text.__

──「 **Scam** 」──
-> `scam <action>`
__chat input action.__

**scame types**: '`typing`', '`upload_photo`', '`record_video`', '`upload_video`', '`record_audio`', '`upload_audio`', '`upload_document`', '`find_location`', '`record_video_note`', '`upload_video_note`', '`playing`'

──「 **Mock text** 」──
-> `mocktxt`
__Mock someone with text.__

──「 **Vaporwave/Aestethic** 」──
-> `aes`
__Convert your text to Vaporwave.__

──「 **SPAM** 」──
-> `spam` (value) (word)
__spams a word with value given__

-> `spamstk` (value)
__Reply to a sticker to spam the sticker__

──「 **Shrugs** 」──
-> `shg`
__Free Shrugs?..__

──「 **Pat** 」──
-> `pat`
__pat gifs__

——「 **the F sign** 」──
-> `f`
__press **f** to show some respect!__

──「 **Fake Screenshot** 」──
-> `fakess`
__fake screenshot notification toasts__
"""


async def mocking_text(text):
    teks = list(text)
    for i, ele in enumerate(teks):
        teks[i] = ele.upper() if i % 2 != 0 else ele.lower()
    pesan = ""
    for tek in teks:
        pesan += tek
    return pesan


@app.on_message(filters.user(AdminSettings) & filters.command("pat", Command))
async def pat(client, message):
    async with aiohttp.ClientSession() as session:
        URL = "https://some-random-api.ml/animu/pat"
        async with session.get(URL) as request:
            if request.status == 404:
                return await edrep(message, text="**no Pats for u :c**")
            result = await request.json()
            url = result.get("link", None)
            await message.delete()
            await client.send_video(message.chat.id, url,
                                    reply_to_message_id=ReplyCheck(message)
                                    )


@app.on_message(filters.user(AdminSettings) & filters.command("scam", Command))
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
        await edrep(message, text="**Invalid Syntax!**")
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


@app.on_message(filters.user(AdminSettings) & filters.command("shg", Command))
async def shg(_client, message):
    await edrep(message, text=random.choice(meme_strings.shgs))


@app.on_message(filters.user(AdminSettings) & filters.command("spam", Command))
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


@app.on_message(filters.user(AdminSettings) & filters.command("spamstk", Command))
async def spam_stick(client, message):
    if not message.reply_to_message:
        await edrep(message, text="**reply to a sticker with amount you want to spam**")
        return
    if not message.reply_to_message.sticker:
        await edrep(message, text="**reply to a sticker with amount you want to spam**")
        return
    else:
        times = message.command[1]
        if message.chat.type in ['supergroup', 'group']:
            for _ in range(int(times)):
                await client.send_sticker(message.chat.id,
                sticker=message.reply_to_message.sticker.file_id,
                reply_to_message_id=ReplyCheck(message)
                )
                await asyncio.sleep(0.20)

        if message.chat.type == "private":
            for _ in range(int(times)):
                await client.send_message(message.chat.id,
                sticker=message.reply_to_message.sticker.file_id)
                await asyncio.sleep(0.20)


@app.on_message(filters.user(AdminSettings) & filters.command("owo", Command))
async def owo(_client, message):
    cmd = message.command
    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="**cant uwu the void.**")
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
    await edrep(message, text=reply_text)


@app.on_message(filters.user(AdminSettings) & filters.command("f", Command))
async def pay_respecc(_client, message):
    cmd = message.command
    paytext = ""
    if len(cmd) > 1:
        paytext = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        paytext = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="**Press F to Pay Respecc!**")
        await asyncio.sleep(2)
        await message.delete()
        return
    pay = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(
        paytext * 8, paytext * 8, paytext * 2, paytext * 2, paytext * 2,
        paytext * 6, paytext * 6, paytext * 2, paytext * 2, paytext * 2,
        paytext * 2, paytext * 2
    )
    await edrep(message, text=pay)


@app.on_message(filters.user(AdminSettings) & filters.command("str", Command))
async def stretch(_client, message):
    cmd = message.command
    stretch_text = ""
    if len(cmd) > 1:
        stretch_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        stretch_text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="`Giiiiiiiv sooooooomeeeeeee teeeeeeext!`")
        await asyncio.sleep(2)
        await message.delete()
        return
    count = random.randint(3, 10)
    reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                        stretch_text)
    await edrep(message, text=reply_text)


@app.on_message(filters.user(AdminSettings) & filters.command("cp", Command))
async def haha_emojis(_client, message):
    if not message.reply_to_message.message_id:
        return

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
            reply_text += c.upper() if bool(random.getrandbits(1)) else c.lower()
    reply_text += random.choice(meme_strings.emojis)
    await edrep(message, text=reply_text)


@app.on_message(filters.user(AdminSettings) & filters.command("mocktxt", Command))
async def mock_text(client, message):
    if message.reply_to_message:
        teks = message.reply_to_message.text
        if teks is None:
            teks = message.reply_to_message.caption
        if teks is None:
            return
        pesan = await mocking_text(teks)
        await client.edit_message_text(message.chat.id, message.message_id, pesan)


@app.on_message(filters.user(AdminSettings) & filters.command("fakess", Command))
async def fake_ss(client, message):
    await asyncio.gather(
        message.delete(),
        client.send(
            functions.messages.SendScreenshotNotification(
                    peer=await client.resolve_peer(message.chat.id),
                    reply_to_msg_id=0,
                    random_id=client.rnd_id(),
                )
            )
        )


@app.on_message(filters.user(AdminSettings) & filters.command("g", Command))
async def glitch(client, message):
    cmd = message.command
    amount = ""
    if len(cmd) > 1:
        amount = " ".join(cmd[1:])
    elif len(cmd) == 1:
        amount = '2'
    profile_photo = "nana/downloads/pfp.jpg"
    glitched_gif = "nana/downloads/glitched_pfp.gif"
    replied = message.reply_to_message
    if not replied:
        await message.delete()
        return
    user = await client.get_users(replied.from_user.id)
    await client.download_media(user.photo.big_file_id, file_name=profile_photo)
    subprocess.run(
        ["glitch_this",
        profile_photo,
        f"{amount}",
        "--gif"],
        capture_output=True,
        text=True
        )
    await client.send_animation(message.chat.id,
                                glitched_gif,
                                reply_to_message_id=ReplyCheck(message)
                                )
    await message.delete()
    os.remove(profile_photo)
    os.remove(glitched_gif)