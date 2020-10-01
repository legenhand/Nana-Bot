from pyrogram import filters, errors
from pyrogram.types import InlineKeyboardMarkup

from nana import app, setbot, Command, Owner, BotUsername, DB_AVAILABLE, edrep
from nana.helpers.PyroHelpers import ReplyCheck
from nana.helpers.msg_types import Types, get_note_type
from nana.helpers.string import parse_button, build_keyboard

if DB_AVAILABLE:
    from nana.modules.database import notes_db as db

# TODO: Add buttons support in some types
# TODO: Add group notes, but whats for? since only you can get notes

__MODULE__ = "Notes"
__HELP__ = """
Save a note, get that, even you can delete that note.
This note only avaiable for yourself only!
Also notes support inline button powered by inline query assistant bot.

──「 **Save Note** 」──
-> `save (note)`
Save a note, you can get or delete that later.

──「 **Get Note** 」──
-> `get (note)`
Get that note, if avaiable.

──「 **Delete Note** 」──
-> `clear (note)`
Delete that note, if avaiable.

──「 **All Notes** 」──
-> `saved`
-> `notes`
Get all your notes, if too much notes, please use this in your saved message instead!


── **Note Format** ──
-> **Button**
`[Button Text](buttonurl:google.com)`
-> **Bold**
`**Bold**`
-> __Italic__
`__Italic__`
-> `Code`
`Code` (grave accent)
"""

GET_FORMAT = {
    Types.TEXT.value: app.send_message,
    Types.DOCUMENT.value: app.send_document,
    Types.PHOTO.value: app.send_photo,
    Types.VIDEO.value: app.send_video,
    Types.STICKER.value: app.send_sticker,
    Types.AUDIO.value: app.send_audio,
    Types.VOICE.value: app.send_voice,
    Types.VIDEO_NOTE.value: app.send_video_note,
    Types.ANIMATION.value: app.send_animation,
    Types.ANIMATED_STICKER.value: app.send_sticker,
    Types.CONTACT: app.send_contact
}


@app.on_message(filters.user(Owner) & filters.command("save", Command))
async def save_note(_client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    note_name, text, data_type, content = get_note_type(message)

    if not note_name:
        await message.edit("```" + message.text + '```\n\nError: You must give a name for this note!')
        return

    if data_type == Types.TEXT:
        teks, _ = parse_button(text)
        if not teks:
            await message.edit("```" + message.text + '```\n\nError: There is no text in here!')
            return

    db.save_selfnote(message.from_user.id, note_name, text, data_type, content)
    await message.edit(f'Saved note `{note_name}`!')


@app.on_message(filters.user(Owner) & filters.command("get", Command))
async def get_note(client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    if len(message.text.split()) >= 2:
        note = message.text.split()[1]
    else:
        await message.edit("Give me a note tag!")

    getnotes = db.get_selfnote(message.from_user.id, note)
    if not getnotes:
        await message.edit("This note does not exist!")
        return

    if getnotes['type'] == Types.TEXT:
        teks, button = parse_button(getnotes.get('value'))
        button = build_keyboard(button)
        button = InlineKeyboardMarkup(button) if button else None
        if button:
            try:
                inlineresult = await app.get_inline_bot_results(f"@{BotUsername}", f"note {note}")
            except errors.exceptions.bad_request_400.BotInlineDisabled:
                await message.edit("Your bot inline isn't available!\nCheck your bot for more information!")
                await setbot.send_message(Owner, "Hello, your notes is look like include button, but i can't do that "
                                                 "because **inline mode** is not enabled.\n\n**To enable inline "
                                                 "mode:**\n1. Go to @BotFather and type `/mybots`\n2. Select your bot, "
                                                 "then click **Bot Settings**, click **Inline Mode**, then click "
                                                 "**Turn on**.\nOther option is optional, you can edit inline "
                                                 "placeholder as you like!\n\nAfter that, you can try again to get "
                                                 "that note!")
                return
            try:
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message)
                )
            except IndexError:
                await message.edit("An error has accured! Check your assistant for more information!")
                return
        else:
            await message.edit(teks)
    elif getnotes['type'] in (Types.STICKER, Types.VOICE, Types.VIDEO_NOTE, Types.CONTACT, Types.ANIMATED_STICKER):
        await GET_FORMAT[getnotes['type']](message.chat.id, getnotes['file'], reply_to_message_id=ReplyCheck(message))
    else:
        if getnotes.get('value'):
            teks, button = parse_button(getnotes.get('value'))
            button = build_keyboard(button)
            button = InlineKeyboardMarkup(button) if button else None
        else:
            teks = None
            button = None
        if button:
            try:
                inlineresult = await app.get_inline_bot_results(f"@{BotUsername}", f"note {note}")
            except errors.exceptions.bad_request_400.BotInlineDisabled:
                await message.edit("Your bot inline isn't available!\nCheck your bot for more information!")
                await setbot.send_message(Owner,
                                          "Hello, your notes is look like include button, but i can't do that because "
                                          "**inline mode** is not enabled.\n\n**To enable inline mode:**\n1. Go to "
                                          "@BotFather and type `/mybots`\n2. Select your bot, then click **Bot "
                                          "Settings**, click **Inline Mode**, then click **Turn on**.\nOther option is "
                                          "optional, you can edit inline placeholder as you like!\n\nAfter that, "
                                          "you can try again to get that note!")
                return
            try:
                await message.delete()
                await client.send_inline_bot_result(
                    message.chat.id,
                    inlineresult.query_id,
                    inlineresult.results[0].id,
                    reply_to_message_id=ReplyCheck(message)
                )
            except IndexError:
                message.edit("An error has accured! Check your assistant for more information!")
                return
        else:
            await GET_FORMAT[getnotes['type']](message.chat.id, getnotes['file'], caption=teks,
                                               reply_to_message_id=ReplyCheck(message))


@app.on_message(filters.user(Owner) & filters.command(["notes", "saved"], Command))
async def local_notes(_client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    getnotes = db.get_all_selfnotes(message.from_user.id)
    if not getnotes:
        await message.edit("There are no notes in local notes!")
        return
    rply = "**Local notes:**\n"
    for x in getnotes:
        if len(rply) >= 1800:
            await edrep(message, text=rply)
            rply = "**Local notes:**\n"
        rply += f"- `{x}`\n"

    await message.edit(rply)


@app.on_message(filters.user(Owner) & filters.command("clear", Command))
async def clear_note(_client, message):
    if not DB_AVAILABLE:
        await message.edit("Your database is not avaiable!")
        return
    if len(message.text.split()) <= 1:
        await message.edit("What do you want to clear?")
        return

    note = message.text.split()[1]
    getnote = db.rm_selfnote(message.from_user.id, note)
    if not getnote:
        await message.edit("This note does not exist!")
        return

    await message.edit(f"Deleted note `{note}`!")
