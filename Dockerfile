# Use lightweight Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for Sevalla health checks)
EXPOSE 8080

# Start the bot
CMD ["bash", "start.sh"]