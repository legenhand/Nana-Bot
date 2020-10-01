import asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import Owner
from nana.__main__ import loop
from nana.assistant.database.custom_theme_db import get_list_costum_theme, get_custom_theme
from nana.assistant.database.theme_db import get_name_theme_set, is_custom_theme
from nana.helpers.aiohttp_helper import AioHttp

cache_theme = {}


async def clear_theme_cache():
    global cache_theme
    while True:
        if not cache_theme:
            await caching_theme()
            await asyncio.sleep(15)
            cache_theme = {}


loop.create_task(clear_theme_cache())


async def caching_theme():
    global cache_theme

    if not cache_theme:
        name = await get_name_theme_set(Owner)
        a = await is_custom_theme()
        if a:
            name = int(name[5:])
            cache_theme = await get_custom_theme(name)
        else:
            theme = await AioHttp().get_json('http://api.harumi.tech/theme')
            cache_theme = {
                "welcome": theme[name]["welcome"],
                "start": theme[name]["start"],
                "settings": theme[name]["settings"],
                "stats": theme[name]["stats"]
            }


async def get_theme(type):
    global cache_theme
    if not cache_theme:
        name = await get_name_theme_set(Owner)
        a = await is_custom_theme()
        if a:
            name = int(name[5:])
            theme = await get_custom_theme(name)
            return theme[type]
        else:
            theme = await AioHttp().get_json('http://api.harumi.tech/theme')
            return theme[name][type]
    return cache_theme[type]


async def theme_list():
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    list_button = []
    for i in theme:
        theme_code = theme[i]["theme-code"]
        call_code = f"thm-{theme_code}"
        list_button.append([InlineKeyboardButton(i, callback_data=call_code)])
    cus_theme = await get_list_costum_theme()
    print(cus_theme)
    for i in range(len(cus_theme)):
        print(cus_theme[i][0], cus_theme[i][1])
        list_button.append([InlineKeyboardButton(cus_theme[i][0], callback_data=cus_theme[i][1])])

    list_button.append([InlineKeyboardButton("⬅ back ", callback_data="back"),
                        InlineKeyboardButton("➕ Add Theme ", callback_data="addtheme")])
    return InlineKeyboardMarkup(list_button)


async def name_theme(theme_code):
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    for i in theme:
        if theme_code == theme[i]["theme-code"]:
            return i
