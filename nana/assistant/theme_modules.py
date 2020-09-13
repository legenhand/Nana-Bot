from pyrogram import Filters
from nana import setbot, Owner
from .database.theme_db import set_name_theme_set
from .theme.theme_helper import theme_list, name_theme


@setbot.on_callback_query(Filters.regex("theme"))
async def chgtheme(_client, query):
    text = "**⚙️Theme Configuration **\n" \
           "`Change Your Nana Theme Here! `\n"

    button = await theme_list()
    await query.message.edit_text(text, reply_markup=button)


@setbot.on_callback_query(Filters.regex("^thm"))
async def chgtheme(_client, query):
    code_theme = query.data[4:]
    name = await name_theme(code_theme)
    await set_name_theme_set(Owner, name)
    text = "**⚙️Theme Configuration **\n" \
           f"Theme Changed To `{name}`\n"

    await query.message.edit_text(text)

# TODO : Added User Theme Customization
