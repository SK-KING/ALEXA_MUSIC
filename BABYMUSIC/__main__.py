import threading
from flask import Flask
import asyncio
import importlib
import config
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from BABYMUSIC import LOGGER, app, userbot
from BABYMUSIC.core.call import BABY
from BABYMUSIC.misc import sudo
from BABYMUSIC.plugins import ALL_MODULES
from BABYMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Flask app definition
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "BABYMUSIC is running on Flask and Thread!"

async def init_bot():
    if not config.STRING1:
        LOGGER(__name__).error("String Session not filled, please provide a valid session.")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER("BABYMUSIC").error(f"Error loading banned users: {e}")

    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("BABYMUSIC.plugins" + all_module)
    LOGGER("BABYMUSIC.plugins").info("All Features Loaded!")

    await userbot.start()
    await BABY.start()
    try:
        await BABY.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("BABYMUSIC").error("Start a voice chat in your log group/channel.")
        exit()
    except Exception as e:
        LOGGER("BABYMUSIC").error(f"Error starting BABY stream: {e}")

    await BABY.decorators()
    LOGGER("BABYMUSIC").info("BABYMUSIC Bot is running!")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("BABYMUSIC").info("BABYMUSIC Bot stopped.")

def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run the async bot
    asyncio.get_event_loop().run_until_complete(init_bot())
