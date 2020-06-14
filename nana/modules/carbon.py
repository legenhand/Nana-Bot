# Based on https://github.com/cyberboysumanjay/Carbon-API
# Author of Carbon API: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
# All rights reserved.

import requests
import asyncio
from time import sleep

from pyrogram import Filters

from nana import app, Command
from nana.helpers.PyroHelpers import ReplyCheck

__MODULE__ = "Carbon API"
__HELP__ = """
Create Beautiful Snippets of your code!

──「 **Carbon** 」──
-> `carbon (reply to msg)`

-> `carbonbg (RGBA color code)`
`Example:` __carbonbg rgba(0, 255, 230, 100)__

-> `carbontheme (theme of your choice)`

──「 **Themes Supported** 」──
`3024-night`
`a11y-dark`
`blackboard`
`base16-dark`
`base16-light`
`cobalt`
`dracula`
`duotone-dark`
`hopscotch`
`lucario`
`material`
`monokai`
`night-owl`
`nord`
`oceanic-next`
`one-light`
`one-dark`
`panda-syntax`
`paraiso-dark`
`seti`,
`shades-of-purple`
`solarized-dark`
`solarized-light`
`synthwave-84`
`twilight`
`verminal`
`vscode`
`yeti`
`zenburn`
"""

theme = "dracula"
bg = "rgba(0, 255, 230, 100)"
themes = ['3024-night', 'a11y-dark', 'blackboard', 'base16-dark', 'base16-light',
    'cobalt', 'dracula', 'duotone-dark', 'hopscotch', 'lucario', 'material',
    'monokai', 'night-owl', 'nord', 'oceanic-next', 'one-light', 'one-dark',
    'panda-syntax', 'paraiso-dark', 'seti', 'shades-of-purple', 'solarized-dark',
    'solarized-light', 'synthwave-84', 'twilight', 'verminal', 'vscode',
    'yeti', 'zenburn']

@app.on_message(Filters.me & Filters.command(["carbon"], Command))
async def carbon(client, message):
    cmd = message.command
    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Usage: `carbon (reply to a text)`")
        await asyncio.sleep(2)
        await message.delete()
        return
    await message.edit("Carbonizing the Code")
    try:
        carbon_result = requests.get(
            "https://sjprojectsapi.herokuapp.com/carbon/?"
            f"text={text}&theme={theme}&bg={bg}").json()
        await client.send_photo(chat_id=message.chat.id, 
                                reply_to_message_id=ReplyCheck(message),
                                photo=carbon_result['link'])
        await message.delete()
    except Exception:
        await message.edit("`api is offline please try again later.`")

@app.on_message(Filters.me & Filters.command(["carbonbg"], Command))
async def carbonbg(_client, message):
    global bg
    cmd = message.command
    type_text = ""
    if len(cmd) > 1:
        type_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        type_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit_text(get_carbon_bg())
        await sleep(5)
        await message.delete()
    bg = type_text
    await message.edit_text("Carbon background set to {}".format(type_text))
    await sleep(2)
    await message.delete()

@app.on_message(Filters.me & Filters.command(["carbontheme"], Command))
async def carbontheme(_client, message):
    global theme
    cmd = message.command
    type_text = ""
    if len(cmd) > 1:
        type_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        type_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit_text(get_carbon_theme())
        await sleep(5)
        await message.delete()
    theme = type_text
    await message.edit_text("Carbon theme set to {}".format(type_text))
    await sleep(2)
    await message.delete()

def get_carbon_bg():
    return bg

def get_carbon_theme():
    return theme