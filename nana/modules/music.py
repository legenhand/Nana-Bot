import asyncio

from pyrogram import filters

from nana import app, Command, AdminSettings, edrep

__MODULE__ = "Deezer"
__HELP__ = """
This Module is to send music into a chat.

──「 **Deezer** 」──
-> `music`(track)
Search a track on Deezer and send into a chat
"""


@app.on_message(filters.user(AdminSettings) & filters.command("music", Command))
async def send_music(client, message):
    try:
        cmd = message.command
        song_name = ""
        if len(cmd) > 1:
            song_name = " ".join(cmd[1:])
        elif message.reply_to_message and len(cmd) == 1:
            song_name = message.reply_to_message.text or message.reply_to_message.caption
        elif len(cmd) == 1:
            await edrep(message, text="Give a song name")
            await asyncio.sleep(2)
            await message.delete()
            return

        song_results = await client.get_inline_bot_results("deezermusicbot", song_name)

        try:
            # send to Saved Messages because hide_via doesn't work sometimes
            saved = await client.send_inline_bot_result(
                chat_id="me",
                query_id=song_results.query_id,
                result_id=song_results.results[0].id,
                hide_via=True)

            # forward as a new message from Saved Messages
            saved = await client.get_messages("me", int(saved.updates[1].message.id))
            reply_to = message.reply_to_message.message_id if message.reply_to_message else None
            await client.send_audio(
                chat_id=message.chat.id,
                audio=str(saved.audio.file_id),
                file_ref=str(saved.audio.file_ref),
                reply_to_message_id=reply_to
            )

            # delete the message from Saved Messages
            await client.delete_messages("me", saved.message_id)
        except TimeoutError:
            await edrep(message, text="That didn't work out")
            await asyncio.sleep(2)
        await message.delete()
    except Exception as e:
        print(e)
        await edrep(message, text="`Failed to find song`")
        await asyncio.sleep(2)
        await message.delete()
        