📸 Telegram i.ibb.co Uploader Bot

A simple Telegram bot that uploads images sent to it onto **[i.ibb.co](https://i.ibb.co)** (via ImgBB API) and returns the direct image link.  
Built with **Pyrogram** + **Flask** (for Render keep-alive).

---

## 🚀 Features
- Upload any photo sent to the bot
- Returns **direct i.ibb.co URL**
- Supports **Render worker deployment** (keeps alive with Flask ping server)
- Docker-ready

---

## 🛠️ Setup

### 1. Clone repo
```bash
git clone https://github.com/yourusername/ibb-uploader-bot.git
cd ibb-uploader-bot

2. Install dependencies

pip install -r requirements.txt

3. Environment variables

Create a .env file (or use Render dashboard):

API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_telegram_bot_token
IMGBB_API_KEY=your_imgbb_api_key

Get:

API_ID + API_HASH → my.telegram.org

BOT_TOKEN → @BotFather

IMGBB_API_KEY → ImgBB API



---

▶️ Run locally

python bot.py


---

🐳 Run with Docker

docker build -t ibb-bot .
docker run --env-file .env -p 8080:8080 ibb-bot


---

☁️ Deploy on Render

1. Push to a GitHub repo


2. Create new Web Service in Render


3. Add environment variables from .env


4. Render will build & run automatically



The bot will log:

Bot is running ✅


---

💡 Example

Send a photo → Bot replies:

✅ Uploaded: https://i.ibb.co/xxxxxx/yourphoto.jpg


---





