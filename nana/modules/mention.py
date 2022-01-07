from asyncio import sleep
from functools import partial

from pyrogram import filters

from nana import Command, app, AdminSettings, edrep

__MODULE__ = "Mention"
__HELP__ = """
──「 **Mention** 」──
-> `mention @(username) Pokurt`
Mention a user with a different name

-> `hmention @(username)`
Mention a user with a hidden text

"""

mention = partial(
    "<a href='tg://user?id={}'>{}</a>".format
)

hmention = partial(
    "<a href='tg://user?id={}'>\u200B</a>{}".format
)


@app.on_message(filters.user(AdminSettings) & filters.command("mention", Command))
async def mention_user(client, message):
    if len(message.command) < 3:
        await edrep(message, text="Incorrect format\nExample: mention @pokurt CTO")
        await sleep(3)
        await message.delete()
        return
    try:
        user = await client.get_users(message.command[1])
    except Exception:
        await edrep(message, text="User not found")
        await sleep(3)
        await message.delete()
        return

    _mention = mention(user.id, ' '.join(message.command[2:]))
    await edrep(message, text=_mention)


@app.on_message(filters.me & filters.command("hmention", Command))
async def hidden_mention(client, message):
    if len(message.command) < 3:
        await edrep(message, text="Incorrect format\nExample: hmention @pokurt")
        await sleep(3)
        await message.delete()
        return
    try:
        user = await client.get_users(message.command[1])
    except Exception:
        await edrep(message, text="User not found")
        await sleep(3)
        await message.delete()
        return

    _hmention = hmention(user.id, ' '.join(message.command[2:]))
    await edrep(message, text=_hmention)