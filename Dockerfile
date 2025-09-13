FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render requires an exposed port, but this bot is a worker.
EXPOSE 8080

CMD ["python3", "bot.py"]