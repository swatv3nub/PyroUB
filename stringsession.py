from pyrogram import Client

t = "Session sent in your Saved Messages too!"
API_ID = int(input("Enter API ID: "))
API_HASH = input("Enter API HASH: ")
with Client(":memory:", api_id=API_ID, api_hash=API_HASH) as app:
    e = app.export_session_string()
    print(f"{e}\n\n{t}")
    app.send_message("me", f"**YOUR SESSION STRING**\n\n{e}`")