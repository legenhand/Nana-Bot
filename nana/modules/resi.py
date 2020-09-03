import requests
import json

from pyrogram import Filters

from nana import app, Command, BINDERBYTE_API


@app.on_message(Filters.me & Filters.command(["lacak"], Command))
async def resi(client, message):
    msg = message.command
    result = await cek_resi(msg[1], msg[2])
    parsed_result = await parse_pos(result)
    await message.edit("`{}`".format(parsed_result))
    return


async def cek_resi(courier, awb):
    URL = "https://api.binderbyte.com/cekresi?awb={}&api_key={}&courier={}".format(awb, BINDERBYTE_API, courier)
    r = requests.get(url=URL)
    return r.json()


async def parse_pos(r):
    if r["result"]:
        msg = r['message']
        no_resi = r['data']['waybill']
        ekspedisi = r['data']['courier']
        tracking = r['data']['tracking']
        hasil_track = ""
        for i in tracking:
            hasil_track += f"Tanggal : {i['date']}\n" \
                           f"Status : {i['desc']}\n"
        result = f"{msg} \n" \
                 f"No Resi : {no_resi} \n" \
                 f"Ekspedisi : {ekspedisi} \n" \
                 f"Hasil Pelacakan : \n" \
                 f"{hasil_track}"
    else:
        result = "No Resi Tidak Ditemukan !"
    return result
