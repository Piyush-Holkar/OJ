FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=OJ.settings

# Install system packages
RUN apt update && apt install -y --no-install-recommends \
    gcc g++ libffi-dev libssl-dev python3-dev \
 && apt clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy entire project
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set entrypoint permissions
RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Start with entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
