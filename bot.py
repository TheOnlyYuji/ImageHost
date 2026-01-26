import os
import aiohttp
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8550917261:AAGo6yoNZ38qUG9Q_okijMMLUE3LWdylW5Y")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "f1bfa51a474f677af33efbad5e14f0b5")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me an image and I'll upload it to i.ibb.co!"
    )

# Handle photo uploads
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    url = "https://api.imgbb.com/1/upload"

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as img:
            data = aiohttp.FormData()
            data.add_field("key", IMGBB_API_KEY)
            data.add_field("image", img)

            async with session.post(url, data=data) as resp:
                result = await resp.json()

    # cleanup
    os.remove(file_path)

    if result.get("success"):
        image_url = result["data"]["url"]
        await update.message.reply_text(f"✅ Uploaded!\n{image_url}")
    else:
        await update.message.reply_text("❌ Upload failed. Try again later.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🚀 Bot started successfully")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())