import os
from asyncio import sleep, gather

from pyrogram import filters
from pyrogram import utils
from pyrogram.raw import functions

from nana import app, Command, DB_AVAILABLE, AdminSettings, edrep

if DB_AVAILABLE:
    from nana.modules.database.cloner_db import backup_indentity, restore_identity

__MODULE__ = "User"
__HELP__ = """
Modules that interact with user

──「 **Profile Picture** 」──
-> `setpfp`
Reply to any photo to set as pfp

-> `vpfp`
View current pfp of user

──「 **Cloner** 」──
-> `clone` or `revert`
clone user identity or revert to original identity

-> `clone origin`
clone user identity with original backup

──「 **Group** 」──
-> `join <groupname>`
joins a public groupchat

-> `leave`
Leave chat

──「 **Tag All** 」──
-> `tagall`
tags most recent 100 members in a group

──「 **Unread** 」──
-> `un` or `unread`
Set chat status to unread

──「 **Save Message** 」──
-> `s` or `save`
Forward a message into Saved Messages

──「 **Link Message** 」──
-> `link`
Creates message link to a message
"""

profile_photo = "nana/downloads/pfp.jpg"


@app.on_message(filters.user(AdminSettings) & filters.command("link", Command))
async def link_message(client, message):
    if message.chat.type == "private" and message.chat.type ==  "bot":
        await message.delete()
        return
    else:
        if message.reply_to_message:
            b = message.reply_to_message.message_id
        else:
            b = message.message_id
        a = utils.get_channel_id(message.chat.id)
        await edrep(message, text=f'https://t.me/c/{a}/{b}')


@app.on_message(filters.user(AdminSettings) & filters.command(["e", "edit"], Command))
async def edit_text(client, message):
    cmd = message.command
    teks = ""
    if len(cmd) > 1:
        teks = " ".join(cmd[1:])
    rep = message.reply_to_message
    if rep.text:
        await message.delete()
        await client.edit_message_text(message.chat.id, message.reply_to_message.message_id, teks)
        return
    elif rep.photo or rep.video or rep.audio or rep.voice or rep.sticker or rep.animation:
        await message.delete()
        await client.edit_message_caption(message.chat.id, message.reply_to_message.message_id, teks)
    else:
        await edrep(message, text='`reply to a message to edit caption`')
        await sleep(3)
        await message.delete()



@app.on_message(filters.user(AdminSettings) & filters.command("setpfp", Command))
async def set_pfp(client, message):
    replied = message.reply_to_message
    if (replied and replied.media and (
            replied.photo or (
            replied.document and "image" in replied.document.mime_type
    )
    )
    ):
        await client.download_media(
            message=replied,
            file_name=profile_photo
        )
        await client.set_profile_photo(profile_photo)
        if os.path.exists(profile_photo):
            os.remove(profile_photo)
        await edrep(message, text="<code>Profile picture changed.</code>",
            parse_mode='html'
        )
    else:
        await edrep(message, text="```Reply to any photo to set as pfp```")
        await sleep(3)
        await message.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("vpfp", Command))
async def view_pfp(client, message):
    replied = message.reply_to_message
    if replied:
        user = await client.get_users(replied.from_user.id)
    else:
        user = await client.get_me()
    if not user.photo:
        await edrep(message, text="profile photo not found!")
        return
    await client.download_media(
        user.photo.big_file_id,
        file_name=profile_photo
    )
    await client.send_photo(message.chat.id, profile_photo)
    await message.delete()
    if os.path.exists(profile_photo):
        os.remove(profile_photo)


@app.on_message(filters.user(AdminSettings) & filters.command("clone", Command))
async def clone(client, message):
    if message.reply_to_message:
        target = message.reply_to_message.from_user.id
    elif len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
        await edrep(message, text="Select target user to clone their identity!")
    else:
        await edrep(message, text="Select target user to clone their identity!")
    if "origin" in message.text:
        my_self = await app.get_me()
        my_self = await client.send(functions.users.GetFullUser(id=await client.resolve_peer(my_self['id'])))

        # Backup my first name, last name, and bio
        backup_indentity(my_self['user']['first_name'], my_self['user']['last_name'], my_self['about'])
    q = await app.get_profile_photos(target)
    await client.download_media(q[0], file_name="nana/downloads/pp.png")
    await app.set_profile_photo("nana/downloads/pp.png")
    t = await app.get_users(target)
    t = await client.send(functions.users.GetFullUser(id=await client.resolve_peer(t['id'])))
    p_file = functions.account
    await client.send(
        p_file.UpdateProfile(first_name=t['user']['first_name'] if t['user']['first_name'] is not None else "",
                             last_name=t['user']['last_name'] if t['user']['last_name'] is not None else "",
                             about=t['about'] if t['about'] is not None else ""))
    await edrep(message, text="`New identity has changed!`")
    await sleep(5)
    await message.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("revert", Command))
async def revert(client, message):
    first_name, last_name, bio = restore_identity()

    await client.send(functions.account.UpdateProfile(first_name=first_name if first_name is not None else "",
                                                      last_name=last_name if last_name is not None else "",
                                                      about=bio if bio is not None else ""))

    photos = await app.get_profile_photos("me")

    await app.delete_profile_photos(photos[0].file_id)

    await edrep(message, text="`Identity Reverted`")
    await sleep(5)
    await message.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("join", Command))
async def join_chat(client, message):
    cmd = message.command
    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="`cant join the void.`")
        await sleep(2)
        await message.delete()
        return
    await client.join_chat(text.replace('@', ''))
    await edrep(message, text=f'joined {text} successfully!')
    await sleep(2)
    await message.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("leave", Command))
async def leave_chat(client, message):
    await edrep(message, text='__adios__')
    await client.leave_chat(message.chat.id)


@app.on_message(filters.command('unread', Command) & filters.user(AdminSettings))
async def mark_chat_unread(client, message):
    await gather(
        message.delete(),
        client.send(
            functions.messages.MarkDialogUnread(
                peer=await client.resolve_peer(message.chat.id), unread=True
            )
        )
    )


@app.on_message(filters.command('s', Command) & filters.user(AdminSettings))
async def to_saved(_client, message):
    await message.delete()
    await message.reply_to_message.forward('self')