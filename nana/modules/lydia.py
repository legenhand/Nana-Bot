import time

from coffeehouse.api import API
from coffeehouse.lydia import LydiaAI
from pyrogram import Filters

from nana import lydia_api, app, Command

lydia_status = False
coffeehouse_api = None
lydia = None
session = None

__MODULE__ = "Chatbot"
__HELP__ = """
──「 **Lydia AI** 」──
-> `lydiapv`
works in private messages by replying to a users message
"""



@app.on_message(Filters.me & Filters.command(["lydiapv"], Command))
async def lydia_private(client, message):
    global lydia_status, coffeehouse_api, lydia, session
    if lydia_api == "":
        await message.edit("`lydia API key is not set!\nSet your lydia API key by adding Config Vars in heroku with "
                           "name lydia_api with value your lydia key API`")
        return
    if lydia_status:
        await message.edit("Turning off lydia...")
        time.sleep(0.5)
        lydia_status = False
        await message.edit("Lydia will not reply your message")
    else:
        await message.edit("Turning on lydia...")
        try:
            coffeehouse_api = API(lydia_api)
            # Create Lydia instance
            lydia = LydiaAI(coffeehouse_api)
            # Create a new chat session (Like a conversation)
            session = lydia.create_session()
        except:
            await message.edit("Wrong lydia API key!")
            return
        lydia_status = True
        await message.edit("now Lydia will reply your message!")


@app.on_message(Filters.incoming & Filters.private)
async def lydia_reply(client, message):
    global lydia_status, session
    if lydia_status:
        output = session.think_thought(message.text)
        await message.reply_text("`{0}`".format(output), quote=True)
    else:
        return
