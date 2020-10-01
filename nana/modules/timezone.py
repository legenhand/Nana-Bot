from datetime import datetime

from pyrogram import filters
from pytz import timezone

from nana import app, Command, time_country, AdminSettings, edrep

__MODULE__ = "Time"
__HELP__ = """
Modules that helps a user to get date and time
here are the timezone list: [link](https://telegra.ph/Time-Zone-list-for-Nana-Remix-07-21)

──「 **Time and Date** 」──
-> `time`
Returns the Date and Time for a selected country

"""


@app.on_message(filters.user(AdminSettings) & filters.command("time", Command))
async def grabTime(client, message):
    if not time_country:
        await message.delete()
        return
    tz = time_country.replace('_', ' ')
    tzDateTime = datetime.now(timezone(tz))
    date = tzDateTime.strftime(r'%d-%m-%Y')
    militaryTime = tzDateTime.strftime('%H:%M')
    time = datetime.strptime(militaryTime, "%H:%M").strftime("%I:%M %p")
    time_string = '__Currently it is__' +f' **{time}** '+'__on__'+f' **{date}** '+'__in__ '+f'**{tz}**'
    await edrep(message, text=time_string)