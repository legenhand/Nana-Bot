from nana.helpers.aiohttp_helper import AioHttp
from nana.assistant.database.theme_db import get_name_theme_set
from nana import Owner
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup


async def get_theme(name, type):
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    name = await get_name_theme_set(Owner)
    return theme[name][type]


async def theme_list():
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    list_button = []
    for i in theme:
        theme_code = theme[i]["theme-code"]
        call_code = f"thm-{theme_code}"
        list_button.append([InlineKeyboardButton(i, callback_data=call_code)])
    list_button.append([InlineKeyboardButton("⬅ back️", callback_data="back")])
    return InlineKeyboardMarkup(list_button)


async def name_theme(theme_code):
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    for i in theme:
        if theme_code == theme[i]["theme-code"]:
            return i