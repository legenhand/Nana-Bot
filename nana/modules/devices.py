import requests

from nana import app, Command
from pyrogram import Filters

__MODULE__ = "Device"
__HELP__ = """
Check device codename

──「 **Device** 」──
-> `device (codename)`
"""


DEVICE_LIST = "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/devices.json"

@app.on_message(Filters.user("self") & Filters.command(["device"], Command))
async def get_device_info(client, message):
	if len(message.text.split()) == 1:
		await message.edit("Usage: `device (codename)`")
		return
	getlist = requests.get(DEVICE_LIST).json()
	targetdevice = message.text.split()[1]
	devicelist = []
	found = False
	for x in getlist:
		if x['device'].lower() == targetdevice:
			found = True
			await message.edit("Brand: `{}`\nName: `{}`\nDevice: `{}`\nCodename: `{}`".format(x['brand'], x['name'], x['model'], x['device']))
			break
	if not found:
		await message.edit("Device {} was not found!".format(targetdevice))
