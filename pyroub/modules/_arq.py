from core.helpers.pyrohelper import get_arg
from pyrogram import filters
from pyroub import *


@app.on_message(cmd("pypi") & filters.user(AUTH))
async def pypi(_, message):
    query = get_arg(message)
    if not query:
        await eor(message, "I need a Query to Search too")
        return
    res = await arq.pypi(query)
    if not res.ok:
        await eor(message, "404: Not Found!")
        return
    res = res.result
    urls = [
        f"{key}: {value}"
        for key, value in res.projectURLS.items()
    ]
    urls = ("\n" + "\n".join(url)) if url else None
    result = f"""
**Name:** {res.name}
**Pypi:** {res.pypiURL}
**Version:** {res.version}
**License:** {res.license}
**Description:** {res.description}
**Size:** {res.size}
**Last Update:** {res.uploadTime}
**Author:** {res.author}
**Author's Email:** {res.authorEmail}
**Requirememts:** {(f'{" | ".join(res.requirements)}') if res.requirements else None}
**Min. Python Version:** {res.minPyVersion}
**Homepage:** {res.homepage}
**Bug Tracker:** {res.bugTrackURL}
**Docs:** {res.docsURL}
**Releases:** {res.releaseURL}
**ProjectURL:** {urls}
    """
    await eor(message, result)
    
@app.on_message(cmd("tmdb") & filters.user(AUTH))
async def tmdb(_, message):
    query = get_arg(message)
    if not query:
        await eor(message, "I need a Query to Search too")
        return
    res = await arq.tmdb(query)
    if not res.ok:
        await eor(message, "404: Not Found!")
        return
    res = res.result[:49]
    for result in res:
        if not res.poster and not res.backdrop:
            continue
        if not res.genre:
            genre = None
        else:
            genre = " | ".join(res.genre)
        description = (
            res.overview[0:900] if res.overview else "None"
        )
        result = f"""
**{res.title}**
**Type:** {res.type}
**Rating:** {res.rating}
**Genre:** {res.genre}
**Release Date:** {res.releaseDate}
**Description:** {res.description}
"""
        await eor(message, result)

"""        
@app.on_message(cmd("img") & filters.user(AUTH))
async def img(_, message):
    query = get_arg(query)
"""
