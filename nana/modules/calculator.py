from currency_converter import CurrencyConverter
from pyrogram import filters

from nana import app, Command, AdminSettings, edrep

__MODULE__ = "Calculator"
__HELP__ = """
Calculator, converting, math, etc.

──「 **Money converter** 」──
-> `curr (value) (from) (to)`
Examlpe: `curr 100 USD IDR`
Output: `USD 100 = IDR 1,409,500.40`

──「 **Temperature converter** 」──
-> `temp (value) (Type)`
Examlpe: `temp 30 C`
Output: `30°C = 86.0°F`
"""

c = CurrencyConverter()


# For converting
def convert_f(fahrenheit):
    f = float(fahrenheit)
    f = (f * 9 / 5) + 32
    return f


def convert_c(celsius):
    cel = float(celsius)
    cel = (cel - 32) * 5 / 9
    return cel


@app.on_message(filters.user(AdminSettings) & filters.command("curr", Command))
async def evaluation_curr(_client, message):
    if len(message.text.split()) <= 3:
        await edrep(message, text="Usage: `curr 100 USD IDR`")
        return
    value = message.text.split(None, 3)[1]
    curr1 = message.text.split(None, 3)[2].upper()
    curr2 = message.text.split(None, 3)[3].upper()
    try:
        conv = c.convert(int(value), curr1, curr2)
        text = "{} {} = {} {}".format(curr1, value, curr2, f'{conv:,.2f}')
        await edrep(message, text=text)
    except ValueError as err:
        await edrep(message, text=str(err))


@app.on_message(filters.user(AdminSettings) & filters.command("temp", Command))
async def evaluation_temp(_client, message):
    if len(message.text.split()) <= 2:
        await edrep(message, text="Usage: `temp 30 C` or `temp 60 F`")
        return
    temp1 = message.text.split(None, 2)[1]
    temp2 = message.text.split(None, 2)[2]
    try:
        if temp2 == "F":
            result = convert_c(temp1)
            text = "`{}°F` = `{}°C`".format(temp1, result)
            await edrep(message, text=text)
        elif temp2 == "C":
            result = convert_f(temp1)
            text = "`{}°C` = `{}°F`".format(temp1, result)
            await edrep(message, text=text)
        else:
            await edrep(message, text="Unknown type {}".format(temp2))
    except ValueError as err:
        await edrep(message, text=str(err))
