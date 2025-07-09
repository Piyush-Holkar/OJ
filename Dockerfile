FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=OJ.settings

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y g++
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "OJ/manage.py", "runserver", "0.0.0.0:8000"]
