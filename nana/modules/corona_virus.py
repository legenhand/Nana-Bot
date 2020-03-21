from datetime import datetime

from covid import Covid
from pyrogram import Filters

from nana import Command, app

__MODULE__ = "Covid Info"
__HELP__ = """
Check info of cases corona virus disease 2019

──「 **Info Covid** 」──
-> `corona (country)`
"""


@app.on_message(Filters.user("self") & Filters.command(["corona"], Command))
async def corona(client, message):
    args = message.text.split(None, 1)
    covid = Covid()
    data = covid.get_data()
    country = args[1]
    country_data = get_country_data(country.capitalize(), data)
    output_text = "`Confirmed : {}\n`".format(country_data["confirmed"])
    output_text += "`Active : {}`\n".format(country_data["active"])
    output_text += "`Deaths : {}`\n".format(country_data["deaths"])
    output_text += "`Recovered : {}`\n".format(country_data["recovered"])
    output_text += "`Last update : {}`\n". \
        format(datetime.utcfromtimestamp(country_data["last_update"] // 1000).strftime('%Y-%m-%d %H:%M:%S'))
    await message.edit("**Corona Virus Info in {}**:\n\n{}".format(country.capitalize(), output_text))


def get_country_data(country, world):
    for country_data in world:
        if country_data["country"] == country:
            return country_data
    return {"Status": "No information yet about this country!"}
