# Thanks to @Athfan for a Base Plugin.
# Go and Do a star on his repo: https://github.com/athphane/userbot
import time
from pyrogram import Filters

from nana import Command, app

__MODULE__ = "Metrics"
__HELP__ = """
This module can help you do the wordcount in the last 1000 messages in a groupchat or private chat.

──「 **Word Count** 」──
-> `wordcount`
Finds the 25 most used words in the last 1000 messages in a chat.

"""


class Custom(dict):
    def __missing__(self, key):
        return 0


@app.on_message(Filters.me & Filters.command(["wordcount"], Command))
async def word_count(client, message):
    await message.delete()
    words = Custom()
    progress = await client.send_message(message.chat.id, "`Processed 0 messages...`")
    total = 0
    async for msg in client.iter_history(message.chat.id, 1000):
        total += 1
        if total % 100 == 0:
            await progress.edit_text(f"`Processed {total} messages...`")
            time.sleep(0.5)
        if msg.text:
            for word in msg.text.split():
                words[word.lower()] += 1
        if msg.caption:
            for word in msg.caption.split():
                words[word.lower()] += 1
    freq = sorted(words, key=words.get, reverse=True)
    out = "Word Counter\n"
    for i in range(25):
        out += f"{i + 1}. **{words[freq[i]]}**: {freq[i]}\n"

    await progress.edit_text(out)