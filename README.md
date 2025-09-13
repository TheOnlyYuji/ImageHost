# Telegram ImgBB Uploader Bot

A Telegram bot that uploads photos to [ImgBB](https://imgbb.com) and returns a shareable link.

## 🚀 Deployment on Render

1. Fork this repo to your GitHub.
2. Create a **Render Worker** service (NOT Web Service).
3. Add these environment variables:
   - `BOT_TOKEN` = your Telegram BotFather token
   - `IMGBB_API_KEY` = your ImgBB API key
4. Render will auto-build and run the bot.

## 🐳 Run Locally (Docker)

```bash
docker build -t telegram-imgbb-bot .
docker run -e BOT_TOKEN=12345:abc -e IMGBB_API_KEY=your_key telegram-imgbb-bot