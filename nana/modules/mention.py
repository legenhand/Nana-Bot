from pyrogram import Filters
from nana import Command, app

__MODULE__ = "Mention"
__HELP__ = """
──「 **Mention** 」──
-> `mention (username without @) (custom text)`
Generate a  hyperlink username you refer with a custom single text.

"""

@app.on_message(Filters.me & Filters.command(["mention"], Command))
async def mention(_client, message):
    args = message.text.split(None, 2)
    if len(args) == 3:
        user = args[1]
        name = args[2]
        rep = f'<a href="tg://resolve?domain={user}">{name}</a>'
        await message.edit(
            rep,
            disable_web_page_preview=True,
            parse_mode="html"
        )
    else:
        await message.edit("Usage: `mention (username without @) (custom text)`")
        return