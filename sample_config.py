import os

API_ID = os.environ.get("API_ID", 6)
API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
SESSION = os.environ.get("SESSION", None)
VC_SESSION = os.environ.get("VC_SESSION", None)
PREFIX = os.environ.get("PREFIX", ".")
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
AUTH_USERS = list(int(x) for x in os.environ.get("AUTH_USERS", "").split())
VC_PREFIX = os.environ.get("VC_PREFIX", "!")
LOG_CHAT = os.environ.get("LOG_CHAT", None)
GLOBAL_LOG_CHAT = os.environ.get("GLOBAL_LOG_CHAT", None)
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
ARQ_X_API = os.environ.get("ARQ_X_API", None)

"""I Know You Guys are Genius....You can setup Self Host!"""