import os
from pyroub import *
from tswift import Song
from pytube import YouTube
from core.helpers.pyrohelper import get_arg
from youtubesearchpython import VideoSearch

@app.on_message(cmd("lyrics") & filters.user(AUTH))
async def lyrics(_, message):
    song = get_arg(message)
    if not song:
        await eor(message, "Give a Song name too!")
        return
    resp = Song.find_song(song)
    if resp:
        if resp.lyrics:
            reply = resp.format()
        else:
            await eor(message, "Lyrics Not Found! Try again Properly")
            return
    else:
        await eor(message, "Lyrics Not Found! Try again Properly")
        return
    file = "./DOWNLOAD/lyrics.txt"
    if os.path.exists(file):
        os.remove(file)
    open(file, "w").write(reply)
    await app.send_document(message.chat.id, file, caption=f"Lyrics of {song}!")
    await message.delete()
    os.remove(file)

def yt_search(song):
    VideoSearch = VideoSearch(song, limit=1)
    res = VideoSearch.result()
    if not res:
        return False
    else:
        vid = res["result"][0]["id"]
        url = f"https://youtu.be/{vid}"
        return url
    
@app.on_message(cmd(["song", "yt"]) & filters.user(AUTH))
async def song(_, message):
    song = get_arg(message)
    if not song:
        await eor(message, "Give a Song name too!")
        return
    song = song + " " + "song"
    vid = yt_search(song)
    if not vid:
        await eor(message, "404: Song Unavailable. Make sure you're spelling the song name properly")
        return
    yt = YouTube(vid)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        dl = audio.download(filename=f"{str(UB_ID)}")
    except Exception as e:
        await eor(message, f"Failed: Download Unavailable!\nThrown Error {e}")
        return
    name = os.rename(dl, f"{str(UB_ID)}.mp3")
    await app.send_chat_action(message.chat.id, "upload_audio")
    await app.send_audio(
        message.chat.id,
        audio=f"{str(UB_ID)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        caption=f"Song Link: [YouTube]({vid})"
        reply_to_message_id=message.message_id,
    )
    try:
        await message.delete()
    except:
        pass
    os.remove(f"{str(UB_ID)}.mp3")