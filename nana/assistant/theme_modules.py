from pyrogram import Filters
from nana import setbot
from .theme.theme_helper import theme_list


@setbot.on_callback_query(Filters.regex("theme"))
async def chgtheme(_client, query):
    print("test")
    text = "**⚙️Theme Configuration **\n" \
           "`Change Your Nana Theme Here! `\n"

    button = await theme_list()
    await query.message.edit_text(text, reply_markup=button)


