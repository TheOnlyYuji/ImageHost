import os
import requests
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

# Telegram + ImgBB config
API_ID = int(os.getenv("API_ID", "12345"))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "your_imgbb_key")

app = Client("ibbUploaderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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

@app.on_message(filters.photo)
async def handle_photo(client, message):
    msg = await message.reply_text("⬆️ Uploading to i.ibb.co ...")
    file_path = await message.download()
    link = upload_to_ibb(file_path)
    await msg.edit_text(f"✅ Uploaded: {link}")

# --- Flask keepalive server for Render ---
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is running ✅", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Run Flask server in a thread
    Thread(target=run_flask).start()
    # Run Telegram bot
    app.run()