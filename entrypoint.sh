#!/bin/sh

# Apply migrations and run the server
python OJ/manage.py makemigrations --noinput
python OJ/manage.py migrate --noinput
python OJ/manage.py runserver 0.0.0.0:8000
