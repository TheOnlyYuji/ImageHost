import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Enable logging (to show logs in Render)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

if not BOT_TOKEN or not IMGBB_API_KEY:
    raise RuntimeError("❌ BOT_TOKEN and IMGBB_API_KEY must be set in environment variables")

# Upload function
def upload_to_imgbb(image_bytes):
    url = "https://api.imgbb.com/1/upload"
    payload = {"key": IMGBB_API_KEY}
    files = {"image": image_bytes}
    response = requests.post(url, data=payload, files=files)
    response.raise_for_status()
    return response.json()["data"]["url"]

# Handle photos
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("📩 Received photo from %s (%s)", user.username, user.id)

    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    image_bytes = await photo_file.download_as_bytearray()

    try:
        logger.info("⬆️ Uploading photo to ImgBB...")
        link = upload_to_imgbb(image_bytes)
        await update.message.reply_text(f"✅ Uploaded!\n{link}")
        logger.info("✅ Uploaded successfully: %s", link)
    except Exception as e:
        logger.error("❌ Upload failed: %s", e)
        await update.message.reply_text("❌ Failed to upload. Please try again later.")

# Main
def main():
    logger.info("🚀 Starting Telegram ImgBB Bot...")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("✅ Bot is running. Waiting for photos...")
    app.run_polling()

if __name__ == "__main__":
    main()