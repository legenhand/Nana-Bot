# Based on https://github.com/cyberboysumanjay/Carbon-API
# Author of Carbon API: Sumanjay (https://github.com/cyberboysumanjay) (@cyberboysumanjay)
# All rights reserved.

import requests
from pyrogram import Filters
from nana import app, Command

__MODULE__ = "Carbon API"
__HELP__ = """
Create Beautiful Snippets of your code!

──「 **Carbon** 」──
-> `carbon (text or reply to msg | theme-name | colour code)`

Example: carbon print('Hello World') | lucario | #48e8e3
Themes Supported:
`3024-night`, `a11y-dark`, `blackboard`, `base16-dark`, `base16-light`,
`cobalt`, `dracula`, `duotone-dark`, `hopscotch`, `lucario`, `material`,
`monokai`, `night-owl`, `nord`, `oceanic-next`, `one-light`, `one-dark`,
`panda-syntax`, `paraiso-dark`, `seti`, `shades-of-purple`, `solarized-dark`,
`solarized-light`, `synthwave-84`, `twilight`, `verminal`, `vscode`,`yeti`, `zenburn`"
"""

theme = 'dracula'
bg = "rgba(0, 255, 230, 100)"
themes = [
    '3024-night', 'a11y-dark', 'blackboard', 'base16-dark', 'base16-light',
    'cobalt', 'dracula', 'duotone-dark', 'hopscotch', 'lucario', 'material',
    'monokai', 'night-owl', 'nord', 'oceanic-next', 'one-light', 'one-dark',
    'panda-syntax', 'paraiso-dark', 'seti', 'shades-of-purple', 'solarized-dark',
    'solarized-light', 'synthwave-84', 'twilight', 'verminal', 'vscode',
    'yeti', 'zenburn']

@app.on_message(Filters.user("self") & Filters.command(["carbon"], Command))
async def carbon(client, message):
    replied = message.reply_to_message
    if replied:
        text = replied.text
        args = message.text.split('|')
    else:
        text = message.text
        args = text.split('|')

    if len(args) > 0:
        for arg in args:
            arg = arg.strip()
            if arg.lower().replace(" ", "-") in themes:
                theme = arg.lower()
            elif arg.startswith("#") or arg.startswith("rgb"):
                if arg[0] == "#" and len(arg) == 7:
                    arg = arg[1:]
                bg = arg
            elif len(arg) > 0:
                text = arg

    if not text:
        await message.err("Code not found!")
        return
    await message.edit("Carbonizing the Code")
    try:
        carbon_result = requests.get(
            "https://sjprojectsapi.herokuapp.com/carbon/?"
            f"text={text}&theme={theme}&bg={bg}").json()
        await client.send_photo(chat_id=message.chat.id, photo=carbon_result['link'])
        await message.delete()
    except Exception:
        await message.edit("API is Down! Try again later.")