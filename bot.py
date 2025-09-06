import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Load tokens from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a photo and I’ll upload it to ImgBB for you!")

# Handle photo upload
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # Best quality
    file = await context.bot.get_file(photo.file_id)
    file_path = "temp.jpg"
    await file.download_to_drive(file_path)

    # Upload to ImgBB
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": f}
        )

    if response.status_code == 200:
        data = response.json()
        link = data["data"]["url"]
        await update.message.reply_text(f"✅ Uploaded!\n🔗 {link}")
    else:
        await update.message.reply_text("❌ Upload failed. Try again later.")

# Main function
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running...
           Made By TheOnlyYuji")
    app.run_polling()

if __name__ == "__main__":
    main()
