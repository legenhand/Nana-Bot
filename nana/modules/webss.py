import os

from pyrogram import filters

from nana import app, Command, thumbnail_API, screenshotlayer_API, AdminSettings, edrep

__MODULE__ = "SS Website"
__HELP__ = """
Take a picture of website. You can select one for use this.

──「 **Take ss website** 」──
-> `print (url)`
Send web screenshot, not full webpage. Send as picture

──「 **Take ss website (more)** 」──
-> `ss (url) (*full)`
Take screenshot of that website, if `full` args given, take full of website and send image as document

* = optional
"""


@app.on_message(filters.user(AdminSettings) & filters.command("print", Command))
async def print_web(client, message):
    if len(message.text.split()) == 1:
        await edrep(message, text="Usage: `print web.url`")
        return
    if not thumbnail_API:
        await edrep(message, text="You need to fill thumbnail_API to use this!")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    teks = teks if "http://" in teks or "https://" in teks else "http://" + teks
    capt = f"Website: `{teks}`"
    await client.send_chat_action(message.chat.id, action="upload_photo")
    web_photo = f"https://api.thumbnail.ws/api/{thumbnail_API}/thumbnail/get?url={teks}&width=1280"
    await client.send_photo(message.chat.id, photo=web_photo, caption=capt,
                            reply_to_message_id=message.message_id)


@app.on_message(filters.user(AdminSettings) & filters.command("ss", Command))
async def ss_web(client, message):
    if len(message.text.split()) == 1:
        await edrep(message, text="Usage: `print web.url`")
        return
    if not screenshotlayer_API:
        await edrep(message, text="You need to fill screenshotlayer_API to use this!")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    full = False
    if (
        len(message.text.split()) >= 3
        and message.text.split(None, 2)[2] == "full"
    ):
        full = True

    teks = teks if "http://" in teks or "https://" in teks else "http://" + teks
    capt = f"Website: `{teks}`"

    await client.send_chat_action(message.chat.id, action="upload_photo")
    if full:
        r = f"http://api.screenshotlayer.com/api/capture?access_key={screenshotlayer_API}&url={teks}&fullpage=1"
    else:
        r = f"http://api.screenshotlayer.com/api/capture?access_key={screenshotlayer_API}&url={teks}&fullpage=0"

    await client.send_photo(message.chat.id, photo=r, caption=capt,
                               reply_to_message_id=message.message_id
                               )
    os.remove("nana/cache/web.png")
    await client.send_chat_action(message.chat.id, action="cancel")
