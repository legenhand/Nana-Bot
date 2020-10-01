from pyrogram import filters

from nana import app

__MODULE__ = "Reddit"
__HELP__ = """
──「 **Reddit** 」──
-> `r/telegram`
As long as your message starts with r/, it will automatically generate a subreddit link and hyperlink your message.

"""
the_regex = r"^r\/([^\s\/])+"


@app.on_message(filters.me & filters.regex(the_regex))
async def r_gen(_client, message):
    html = "<a href='{link}'>{string}</a>"
    await message.edit(
        html.format(link="https://reddit.com/" + message.text, string=message.text),
        disable_web_page_preview=True,
        parse_mode="html"
    )
