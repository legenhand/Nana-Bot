import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from nana import app, setbot, Owner, OwnerName, Command, DB_AVAILABLE, edrep
from nana.helpers.msg_types import Types, get_message_type
from nana.helpers.parser import mention_markdown, escape_markdown

if DB_AVAILABLE:
    from nana.modules.database.afk_db import set_afk, get_afk

__MODULE__ = "AFK"
__HELP__ = """
Set yourself to afk.
When marked as AFK, any mentions will be replied to with a message to say you're not available!
And that mentioned will notify you by your Assistant.

If you're restart your bot, all counter and data in cache will be reset.
But you will still in afk, and always reply when got mentioned.

──「 **Set AFK status** 」── -> `afk (*reason)` Set yourself to afk, give a reason if need. When someone tag you, 
you will says in afk with reason, and that mentioned will sent in your assistant PM. 

To exit from afk status, send anything to anywhere, exclude PM and saved message.

* = Optional
"""

# Set priority to 11 and 12
MENTIONED = []
AFK_RESTIRECT = {}
DELAY_TIME = 60  # seconds


@app.on_message(filters.me & (filters.command("afk", Command)))
async def afk(_client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    if len(message.text.split()) >= 2:
        set_afk(True, message.text.split(None, 1)[1])
        await message.edit(
            "{} is now AFK!\nBecause of {}".format(mention_markdown(message.from_user.id, message.from_user.first_name),
                                                   message.text.split(None, 1)[1]))
        await setbot.send_message(Owner, "You are now AFK!\nBecause of {}".format(message.text.split(None, 1)[1]))
    else:
        set_afk(True, "")
        await message.edit(
            "{} is now AFK!".format(mention_markdown(message.from_user.id, message.from_user.first_name)))
        await setbot.send_message(Owner, "You are now AFK!")
    await message.stop_propagation()


@app.on_message(filters.mentioned & ~filters.bot, group=11)
async def afk_mentioned(_client, message):
    if not DB_AVAILABLE:
        return
    global MENTIONED
    get = get_afk()
    if get and get['afk']:
        if "-" in str(message.chat.id):
            cid = str(message.chat.id)[4:]
        else:
            cid = str(message.chat.id)

        if cid in list(AFK_RESTIRECT) and int(AFK_RESTIRECT[cid]) >= int(
            time.time()
        ):
            return
        AFK_RESTIRECT[cid] = int(time.time()) + DELAY_TIME
        if get['reason']:
            await edrep(message, text=f"Sorry, {mention_markdown(Owner, OwnerName)} is AFK!\nBecause of {get['reason']}")
        else:
            await edrep(message, text=f"Sorry, {mention_markdown(Owner, OwnerName)} is AFK!")

        _, message_type = get_message_type(message)
        if message_type == Types.TEXT:
            text = message.text if message.text else message.caption
        else:
            text = message_type.name

        MENTIONED.append(
            {"user": message.from_user.first_name, "user_id": message.from_user.id, "chat": message.chat.title,
             "chat_id": cid, "text": text, "message_id": message.message_id})
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Go to message", url="https://t.me/c/{}/{}".format(cid, message.message_id))]])
        await setbot.send_message(Owner, "{} mentioned you in {}\n\n{}\n\nTotal count: `{}`".format(
            mention_markdown(message.from_user.id, message.from_user.first_name), message.chat.title, text[:3500],
            len(MENTIONED)), reply_markup=button)


@app.on_message(filters.me & filters.group, group=12)
async def no_longer_afk(_client, message):
    if not DB_AVAILABLE:
        return
    global MENTIONED
    get = get_afk()
    if get and get['afk']:
        await setbot.send_message(message.from_user.id, "You are no longer afk!")
        set_afk(False, "")
        text = "**Total {} mentioned you**\n".format(len(MENTIONED))
        for x in MENTIONED:
            msg_text = x["text"]
            if len(msg_text) >= 11:
                msg_text = "{}...".format(x["text"])
            text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(escape_markdown(x["user"]), x["chat_id"],
                                                                     x["message_id"], x["chat"], msg_text)
        await setbot.send_message(message.from_user.id, text)
        MENTIONED = []
