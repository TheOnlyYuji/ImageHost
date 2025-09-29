import os
import requests
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# ----------------------------
# 🔑 Config from environment
# ----------------------------
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")

# ----------------------------
# 🤖 Telegram Bot
# ----------------------------
tg_app = Client(
    "ibbUploaderBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


def upload_to_ibb(file_path: str) -> str:
    """Upload an image to i.ibb.co via ImgBB API"""
    try:
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://api.imgbb.com/1/upload",
                params={"key": IMGBB_API_KEY},
                files={"image": f},
            )
        data = response.json()
        if data.get("success"):
            return data["data"]["url"]
        return "❌ Upload failed!"
    except Exception as e:
        return f"⚠️ Error: {e}"


@tg_app.on_message(filters.photo)
async def handle_photo(client, message):
    msg = await message.reply_text("⬆️ Uploading to i.ibb.co ...")
    file_path = await message.download()
    link = upload_to_ibb(file_path)
    await msg.edit_text(f"✅ Uploaded: {link}")


# ----------------------------
# 🌐 Flask Keepalive App
# ----------------------------
flask_app = Flask(__name__)


@flask_app.route("/")
def home():
    return "Bot is running ✅", 200


# ----------------------------
# 🚀 Start Telegram bot thread
# ----------------------------
def run_bot():
    print("🚀 Starting Telegram bot...")
    tg_app.run()


# Start bot immediately on import (important for Gunicorn)
Thread(target=run_bot, daemon=True).start()