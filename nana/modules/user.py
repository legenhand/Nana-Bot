import os
from nana import app, Command
from pyrogram import Filters

__MODULE__ = "User"
__HELP__ = """
Modules that interact with user

──「 **Profile Picture** 」──
-> `setpfp`
Reply to any photo to set as pfp

-> `vpfp`
View current pfp of user

"""

profile_photo = "nana/downloads/pfp.jpg"

@app.on_message(Filters.me & Filters.command(["setpfp"], Command))
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
        await message.edit(
            "<code>Profile picture changed.</code>",
            parse_mode='html'
        )
    else:
        await message.edit("```Reply to any photo to set as pfp```")


@app.on_message(Filters.me & Filters.command(["vpfp"], Command))
async def view_pfp(client, message):
    replied = message.reply_to_message
    if replied:
        user = await client.get_users(replied.from_user.id)
    else:
        user = await client.get_me()
    if not user.photo:
        await message.edit("profile photo not found!")
        return
    await client.download_media(
        user.photo.big_file_id,
        file_name=profile_photo
    )
    await client.send_photo(message.chat.id, profile_photo)
    await message.delete()
    if os.path.exists(profile_photo):
        os.remove(profile_photo)