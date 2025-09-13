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

✅ Usage
Send a photo to the bot in Telegram.
It replies with a public ImgBB link.
Copy code

---

⚠️ Important for Render:  
- Deploy as a **Worker Service**, not a Web Service.  
- Set `BOT_TOKEN` and `IMGBB_API_KEY` in **Environment Variables**.  

---

👉 Do you want me to also generate the **Procfile** version (for Heroku/Koyeb style deployments), or just keep it as **Dockerfile-only** since you’re using Render Worker?