import os
import requests
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# --- Config ---
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "your_imgbb_api_key")

# --- Pyrogram Bot ---
tg_app = Client("ibbUploaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def upload_to_ibb(file_path: str) -> str:
    """Upload image to ImgBB and return URL"""
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": f},
        )
    data = response.json()
    if data.get("success"):
        return data["data"]["url"]
    else:
        return "❌ Upload failed!"

@tg_app.on_message(filters.photo)
async def handle_photo(client, message):
    msg = await message.reply_text("⬆️ Uploading to i.ibb.co ...")
    file_path = await message.download()
    link = upload_to_ibb(file_path)
    await msg.edit_text(f"✅ Uploaded: {link}")

# --- Flask Keep-Alive Server ---
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running ✅", 200

# --- Start Telegram bot automatically ---
def run_bot():
    tg_app.run()

Thread(target=run_bot, daemon=True).start()