import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "8550917261:AAGo6yoNZ38qUG9Q_okijMMLUE3LWdylW5Y")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "f1bfa51a474f677af33efbad5e14f0b5")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me an image and I'll upload it to i.ibb.co!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    # Upload to i.ibb.co
    with open(file_path, "rb") as f:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY}
        files = {"image": f}
        response = requests.post(url, data=payload, files=files)

    data = response.json()
    if data.get("success"):
        image_url = data["data"]["url"]
        await update.message.reply_text(f"✅ Uploaded!\n{image_url}")
    else:
        await update.message.reply_text("❌ Upload failed. Try again later.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🚀 Bot started successfully...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())