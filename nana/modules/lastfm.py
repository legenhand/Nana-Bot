
from pyrogram import filters

from nana import app, Command
from nana.helpers.PyroHelpers import ReplyCheck

__HELP__ = """
──「 **LastFM** 」──
-> `lastfm` or `lf`
Share what you're what listening to with the help of this module!

Note: you need to go to @lastfmrobot and set your username there

"""
__MODULE__ = "Last.FM"


@app.on_message(filters.me & filters.command(["lastfm", "lf"], Command))
async def lastfm(client, message):
    x = await client.get_inline_bot_results("lastfmrobot", "")
    await message.delete()
    await message.reply_inline_bot_result(x.query_id, x.results[0].id,
                                          reply_to_message_id=ReplyCheck(message),
                                          hide_via=True)