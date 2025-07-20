# STAGE 1: Build stage
FROM python:3.12-slim as build

ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt update && apt install -y \
    gcc g++ libffi-dev libssl-dev python3-dev

WORKDIR /app

COPY . /app

# Install dependencies into a temp dir
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# STAGE 2: Final runtime image

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=OJ.settings

# Only installing required runtime packages
RUN apt update && apt install -y g++

WORKDIR /app

COPY --from=build /install /usr/local
COPY . /app

EXPOSE 8000
COPY entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
