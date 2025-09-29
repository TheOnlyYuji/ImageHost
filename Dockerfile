FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Run Flask with Gunicorn (production) + Pyrogram bot (in thread)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "bot:flask_app"]