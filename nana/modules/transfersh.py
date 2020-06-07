# This module created by @legenhand 10/3/2020
# any error / bugs please report to https://t.me/nanabotsupport
# this module only support to Nana-Bot userbot
import datetime
import os

import pycurl
from pyrogram import Filters

from nana import app, Command, log
from .downloads import download_file_from_tg, name_file, humanbytes

__MODULE__ = "transfer sh"
__HELP__ = """
Mirror any telegram file to transfer.sh

──「 **Transfer telegram file** 」──
-> `tfsh`
Reply to telegram file for mirroring to transfer.sh 

"""


@app.on_message(Filters.me & Filters.command(["tfsh"], Command))
async def tfsh(client, message):
    if not message.reply_to_message:
        await message.edit("`Reply to any file telegram message!`")
        return
    await message.edit("`Processing...`")
    name = await name_file(client, message)
    await download_file_from_tg(client, message)
    if len(name) > 10:
        name_file_upload = name[-10:]
    else:
        name_file_upload = name
    name_file_upload.encode('ascii', 'ignore')
    os.rename(r'nana/downloads/{}'.format(name), r'nana/downloads/{}'.format(name_file_upload))
    print(name_file_upload)
    await message.edit(
        await send_to_transfersh("nana/downloads/{}".format(name_file_upload), message, name_file_upload))
    os.remove("nana/downloads/{}".format(name_file_upload))
    return


async def send_to_transfersh(file, message, name):
    """
    send file to transfersh, retrieve download link, and copy it to clipboard
    :param file: absolute path to file
    :param message: a message atribute
    :return: download_link
    """
    size_of_file = get_size(file)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    await message.edit("\nSending file: {} (size of the file: {})".format(file_name, size_of_file))
    url = 'https://transfer.sh/{}'.format(name)
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    c.setopt(c.UPLOAD, 1)
    with open(file, 'rb') as f:
        c.setopt(c.READDATA, f)
        try:
            download_link = c.perform_rs()
        except pycurl.error as e:
            log.error(e)
            return "Unsupported file format!"
        c.close()
    f.close()
    return "`Success!\nwill be saved till {}`\n{}".format(final_date, download_link)


def get_size(file):
    """
    get file size, in megabytes
    :param file:
    :return: size of file
    """
    size_in_bytes = os.path.getsize(file)
    return humanbytes(size_in_bytes)


def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()
