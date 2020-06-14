from bitlyshortener import Shortener
from pyrogram import Filters

from nana import app, Command, bitly_token

__MODULE__ = "Bitly"
__HELP__ = """
This module will shortener your link

──「 **shorten your url** 」──
-> `bitly (link)`
Shorten your url with bitly

"""


@app.on_message(Filters.me & Filters.command(["bitly"], Command))
async def bitly(_client, message):
    args = message.text.split(None, 1)
    shortener = Shortener(tokens=bitly_token, max_cache_size=8192)
    if len(args) == 1:
        await message.edit("Usage bitly (url)!")
        return
    if len(args) == 2:
        await message.edit("Processing")
        urls = [args[1]]
        shortlink = shortener.shorten_urls(urls)
        await message.edit("Here Your link\n{}".format(shortlink[0]), disable_web_page_preview=True)
