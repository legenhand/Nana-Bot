from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import setbot, Owner
from .database.theme_db import set_name_theme_set
from .theme.theme_helper import theme_list, name_theme


@setbot.on_callback_query(filters.regex("^theme"))
async def chgtheme(_client, query):
    text = "**⚙ Theme Configuration **\n" \
           "`Change Your Nana Theme Here! `\n"

    button = await theme_list()
    await query.message.edit_text(text, reply_markup=button)


@setbot.on_callback_query(filters.regex("^thm"))
async def chgtheme(_client, query):
    code_theme = query.data[4:]
    name = await name_theme(code_theme)
    await set_name_theme_set(Owner, name, False)
    text = "**⚙️Theme Configuration **\n" \
           f"Theme Changed To `{name}`\n"

    await query.message.edit_text(text)


@setbot.on_callback_query(filters.regex("^cthm"))
async def chg_custom_theme(_client, query):
    code_theme = query.data
    await set_name_theme_set(Owner, code_theme, True)
    text = "**⚙️Theme Configuration **\n" \
           f"Theme Changed !\n"

    await query.message.edit_text(text)


@setbot.on_callback_query(filters.regex("^addtheme"))
async def addtheme(client, query):
    await query.message.delete()
    global temp_input
    temp_input = True
    text = "**⚙️Add Theme **\n" \
           f"Set Name theme \n"
    list_button = [[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]
    button = InlineKeyboardMarkup(list_button)
    await client.send_message(Owner, text, reply_markup=button)
