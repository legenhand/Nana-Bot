import datetime
import time
import random

from nana import app, setbot, Command
from pyrogram import Filters

__MODULE__ = "Quotly"
__HELP__ = """
This module can make message text to sticker. (Experimental)

──「 **Make Quote From Message** 」──
-> `q`
Reply To Message Text To Create Quote Sticker

"""

@app.on_message(Filters.user("self") & Filters.command(["q"], Command))
async def quotly(client, message):    
   if not message.reply_to_message:
      await message.edit("Reply to any users text message")
      return
   await message.edit("```Making a Quote```")
   await message.reply_to_message.forward("@QuotLyBot")
   is_sticker = False
   progress = 0
   while is_sticker == False:
      try:
         msg = await app.get_history("@QuotLyBot",1)
         check = msg[0]["sticker"]["file_id"]
         is_sticker = True
      except:
         time.sleep(0.5)
         progress += random.randint(0,10)
         try:
            await message.edit("```Making a Quote```\nProcessing {}%".format(progress))
         except:
            await message.edit("ERROR SUUUU")
   await message.edit("```Complete !```")
   msg_id = msg[0]["message_id"]
   await app.forward_messages(message.chat.id,"@QuotLyBot",msg_id)
              