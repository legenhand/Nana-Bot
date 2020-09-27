import random
from asyncio import sleep

from pyrogram import filters

from nana import app, Command

__MODULE__ = "Quotly"
__HELP__ = """
This module can make message text to sticker. (Experimental)

──「 **Make Quote From Message** 」──
-> `q`
Reply To Message Text To Create Quote Sticker

"""


@app.on_message(filters.me & filters.command(["q"], Command))
async def q_maker(_client, message):
    if not message.reply_to_message:
        await message.edit("Reply to any users text message")
        return
    await message.edit("```Making a Quote```")
    await message.reply_to_message.forward("@QuotLyBot")
    is_sticker = False
    progress = 0
    while not is_sticker:
        try:
            msg = await app.get_history("@QuotLyBot", 1)
            check = msg[0]["sticker"]["file_id"]
            is_sticker = True
        except:
            await sleep(0.5)
            progress += random.randint(0, 10)
            try:
                await message.edit("```Making a Quote```\nProcessing {}%".format(progress))
            except:
                await message.edit("ERROR")
    await message.edit("```Complete !```")
    msg_id = msg[0]["message_id"]
    await message.delete()
    await app.forward_messages(message.chat.id, "@QuotLyBot", msg_id)