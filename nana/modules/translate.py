from googletrans import Translator
from pyrogram import Filters

from nana import app, Command

trl = Translator()

__MODULE__ = "Translate"
__HELP__ = """
Translate some text by give a text or reply that text/caption.
Translate by Google Translate

──「 **Translate** 」──
-> `tr (lang) (*text)`
Give a target language and text as args for translate to that target.
Reply a message to translate that.

* = Not used when reply a message!
"""


# TODO: Setlang for translation

@app.on_message(Filters.me & Filters.command(["tr"], Command))
async def translate(_client, message):
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        if len(message.text.split()) == 1:
            await message.edit("Usage: Reply to a message, then `tr <lang>`")
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit("Error: `{}`".format(str(err)))
            return
        await message.edit("Translated from `{}` to `{}`:\n```{}```".format(detectlang.lang, target, tekstr.text))
    else:
        if len(message.text.split()) <= 2:
            await message.edit("Usage: `tr <lang> <text>`")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit("Error: `{}`".format(str(err)))
            return
        await message.edit("Translated from `{}` to `{}`:\n```{}```".format(detectlang.lang, target, tekstr.text))
