
# ffmpeg -i video_1573046696-542963.mp4 -vf scale=500x500 -strict -2 vid.mp4

import os
import subprocess
from asyncio import sleep

from pyrogram import filters

from nana import setbot, app, Command, Owner, AdminSettings, edrep
from nana.helpers.PyroHelpers import ReplyCheck
from nana.modules.downloads import download_reply_nocall

__MODULE__ = "Video Note"
__HELP__ = """
Video Note Maker
──「 **VN Maker** 」──
-> `mkvn`
Reply a video to make it as video note
"""

error_message = '''
Hello 🙂
You need to install ffmpeg to make audio works better, here is guide how to install it:
**If you're using linux**, go to your terminal, type:
`sudo apt install ffmpeg`
**If you're using Windows**, download ffmpeg here:
`https://ffmpeg.zeranoe.com/builds/`
And then extract (if was archive), and place ffmpeg.exe to workdir (in current dir)
**If you're using heroku**, type this in your workdir:
`heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`
Or if you not using heroku term, follow this guide:
1. Go to heroku.com
2. Go to your app in heroku
3. Change tabs/click Settings, then search for Buildpacks text
4. Click button Add build pack, then type `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`
5. Click Save changes, and you need to rebuild your heroku app to take changes!
'''


@app.on_message(filters.user(AdminSettings) & filters.command("mkvn", Command))
async def vn_maker(client, message):
	if message.reply_to_message and message.reply_to_message.video:
		dlvid = await download_reply_nocall(client, message)
		if dlvid:
			await edrep(message, text="__Converting...__")
			try:
				subprocess.Popen("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			except Exception as err:
				if "The system cannot find the file specified" in str(err) or "No such file or directory" in str(err):
					await edrep(message, text="an error occured! check assistant for more details")
					await sleep(5)
					await message.delete()
					await setbot.send_message(
                        Owner,
                        error_message
                    )
					return
			os.system(
                f'''ffmpeg -loglevel panic -i "{dlvid}" -vf scale="'if(gt(iw,ih),-1,299):if(gt(iw,ih),299,-1)', crop=299:299" -strict -2 -y "{dlvid}_converted.mp4"'''
                )
			await client.send_video_note(message.chat.id,
                                        f"{dlvid}_converted.mp4",
                                        reply_to_message_id=ReplyCheck(message)
                                    )
			await message.delete()
			os.remove(dlvid)
			os.remove(dlvid+"_converted.mp4")
