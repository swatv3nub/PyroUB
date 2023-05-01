import random
from pyroub import *
from core.helpers.pyrohelper import get_arg
from core.helpers.passhelper import *

@app.on_message(cmd("genpass") & filters.user(AUTH))
async def password(_, message):
    length = int(get_arg(message))
    if not length:
        await eor(message, 'give the pass length buddy')
        return
    try:
        password = "".join(random.sample(sup, length))
    except Exception as e:
        await eor(message, e)
        return
    await eor(message, f"Random Password:\n`{password}`")
    