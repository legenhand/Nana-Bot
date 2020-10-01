import os
from platform import python_version

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from nana import app, setbot, AdminSettings, DB_AVAILABLE, USERBOT_VERSION, ASSISTANT_VERSION, BotUsername, Owner, \
    OwnerName
from nana.assistant.settings import get_text_settings, get_button_settings
from nana.assistant.theme.theme_helper import get_theme

if DB_AVAILABLE:
    from nana.modules.database.chats_db import get_all_chats


@setbot.on_message(filters.user(AdminSettings) & filters.command(["start"]))
async def start(_client, message):
    if len(message.text.split()) >= 2:
        helparg = message.text.split()[1]
        if helparg == "help_inline":
            await message.reply("""**Inline Guide**
Just type `@{} (command)` in text box, and wait for response.

──「 **Get Note from Inline** 」──
-> `#note <*notetag>`
And wait for list of notes in inline, currently support Text and Button only.

──「 **Stylish Generator Inline** 」──
-> `#stylish your text`
Convert a text to various style, can be used anywhere!

* = Can be used as optional
""".format(BotUsername))
            return
        if helparg == "createown":
            await message.reply(
                "Want to create your own Userbot and Assistant?\n[Go here]("
                "https://github.com/AyraHikari/Nana-TgBot/wiki), read guide carefully.\nIf you want to ask, "
                "join our community @AyraSupport")
            return
    try:
        me = await app.get_me()
    except ConnectionError:
        me = None
    start_message = f"Hi {OwnerName},\n"
    start_message += "Nana is Ready at your Service!\n"
    start_message += f"===================\n"
    start_message += "-> Python: `{}`\n".format(python_version())
    if not me:
        start_message += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
    else:
        start_message += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
    start_message += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
    start_message += "-> Database: `{}`\n".format(DB_AVAILABLE)
    if DB_AVAILABLE:
        start_message += f"-> Group joined: `{len(get_all_chats())} groups`\n"
    start_message += f"===================\n"
    start_message += f"`For more about the bot press button down below`"
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Help", callback_data="help_back")]])
    img = await get_theme("start")
    await setbot.send_photo(Owner, img, caption=start_message, reply_markup=buttons)


@setbot.on_message(filters.user(AdminSettings) & filters.command(["getme"]))
async def get_myself(client, message):
    try:
        me = await app.get_me()
    except ConnectionError:
        message.reply("Bot is currently turned off!")
        return
    getphoto = await client.get_profile_photos(me.id)
    if len(getphoto) == 0:
        getpp = None
    else:
        getpp = getphoto[0].file_id
    text = "**ℹ️ Your profile:**\n"
    text += "First name: {}\n".format(me.first_name)
    if me.last_name:
        text += "Last name: {}\n".format(me.last_name)
    text += "User ID: `{}`\n".format(me.id)
    if me.username:
        text += "Username: @{}\n".format(me.username)
    text += "Phone number: `{}`\n".format(me.phone_number)
    text += "`Nana Version    : v{}`\n".format(USERBOT_VERSION)
    text += "`Manager Version : v{}`".format(ASSISTANT_VERSION)
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])
    if me.photo:
        await client.send_photo(message.chat.id, photo=getpp, caption=text, reply_markup=button)
    else:
        await message.reply(text, reply_markup=button)


@setbot.on_callback_query(filters.regex("^hide_number"))
async def get_myself_btn(client, query):
    try:
        me = await app.get_me()
    except ConnectionError:
        await client.answer_callback_query(query.id, "Bot is currently turned off!", show_alert=True)
        return

    if query.message.caption:
        text = query.message.caption.markdown
    else:
        text = query.message.text.markdown

    num = ["*" * len(me.phone_number)]

    if "***" not in text.split("Phone number: `")[1].split("`")[0]:
        text = text.replace("Phone number: `{}`\n".format(me.phone_number), "Phone number: `{}`\n".format("".join(num)))
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Show phone number", callback_data="hide_number")]])
    else:
        text = text.replace("Phone number: `{}`\n".format("".join(num)), "Phone number: `{}`\n".format(me.phone_number))
        button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])

    if query.message.caption:
        await query.message.edit_caption(caption=text, reply_markup=button)
    else:
        await query.message.edit(text, reply_markup=button)


@setbot.on_callback_query(filters.regex("^report_errors"))
async def report_some_errors(client, query):
    app.join_chat("@AyraSupport")
    text = "Hi @AyraHikari, i got an error for you.\nPlease take a look and fix it if possible.\n\nThank you ❤️"
    err = query.message.text
    open("nana/cache/errors.txt", "w").write(err)
    await query.message.edit_reply_markup(reply_markup=None)
    await app.send_document("AyraSupport", "nana/cache/errors.txt", caption=text)
    os.remove("nana/cache/errors.txt")
    await client.answer_callback_query(query.id, "Report was sent!")


@setbot.on_message(filters.user(AdminSettings) & filters.command(["settings"]) & filters.private)
async def settings(_client, message):
    text = await get_text_settings()
    button = await get_button_settings()
    img = await get_theme("settings")
    await setbot.send_photo(Owner, img, caption=text, reply_markup=button)
