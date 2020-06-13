# Last.fm module by @TheRealPhoenix - https://github.com/rsktg

import requests
from pyrogram import Filters

from nana import app, Command, lastfm_username, lastfm_api

__HELP__ = """
──「 **LastFM** 」──
-> `lastfm`
Share what you're what listening to with the help of this module!

"""
__MODULE__ = "Last.FM"

LASTFM_API_KEY = lastfm_api

@app.on_message(Filters.me & Filters.command(["lastfm"], Command))
async def lastfm(_client, message):
    username = lastfm_username
    user = username
    if not username:
        await message.edit("You haven't set your username yet!")
        return
    
    base_url = "http://ws.audioscrobbler.com/2.0"
    res = requests.get(f"{base_url}?method=user.getrecenttracks&limit=3&extended=1&user={username}&api_key={LASTFM_API_KEY}&format=json")
    if not res.status_code == 200:
        await message.edit("Hmm... something went wrong.\nPlease ensure that you've set the correct username!")
        return
        
    try:
        first_track = res.json().get("recenttracks").get("track")[0]
    except IndexError:
        await message.edit("You don't seem to have scrobbled any songs...")
        return
    if first_track.get("@attr"):
        # Ensures the track is now playing
        image = first_track.get("image")[3].get("#text") # Grab URL of 300x300 image
        artist = first_track.get("artist").get("name")
        song = first_track.get("name")
        loved = int(first_track.get("loved"))
        rep = f"{user} is currently listening to:\n"
        if not loved:
            rep += f"🎧  <code>{artist} - {song}</code>"
        else:
            rep += f"🎧  <code>{artist} - {song}</code> (♥️, loved)"
        if image:
            rep += f"<a href='{image}'>\u200c</a>"
    else:
        tracks = res.json().get("recenttracks").get("track")
        track_dict = {tracks[i].get("artist").get("name"): tracks[i].get("name") for i in range(3)}
        rep = f"{user} was listening to:\n"
        for artist, song in track_dict.items():
            rep += f"🎧  <code>{artist} - {song}</code>\n"
        last_user = requests.get(f"{base_url}?method=user.getinfo&user={username}&api_key={LASTFM_API_KEY}&format=json").json().get("user")
        scrobbles = last_user.get("playcount")
        rep += f"\n(<code>{scrobbles}</code> scrobbles so far)"
        
    await message.edit(rep, parse_mode='html')