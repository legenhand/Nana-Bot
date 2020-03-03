# This module created by @legenhand 3/3/2020
# any error / bugs please report to https://t.me/nanabotsupport
# this module only support to Nana-Bot userbot

from kbbi import KBBI
from pyrogram import Filters

from nana import app, Command

__MODULE__ = "KBBI"
__HELP__ = """
Search meaning some text from indonesian dictionary

──「 **kbbi** 」──
-> `kbbi (text)`
Search from kbbi, you can reply to text message. 

"""


@app.on_message(Filters.user("self") & Filters.command(["kbbi"], Command))
async def kbbi(client, message):
    await message.edit("`Processing...`")
    if message.reply_to_message:
        kata = message.reply_to_message.text
    else:
        args = message.text.split(None, 1)
        if len(args) == 1:
            await message.edit("Usage : kbbi (kata)")
            return
        kata = args[1]
    try:
        result = "KBBI Result of **{}** \n\n".format(kata)
        result += str(KBBI(kata))
        await message.edit(result)
    except Exception as e:
        await message.edit(e)
