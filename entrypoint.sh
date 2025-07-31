#!/bin/sh


# set -e
echo "Making migrations..."
python OJ/manage.py makemigrations --noinput

echo "Applying migrations..."
python OJ/manage.py migrate --noinput

echo "Collecting static files..."
python OJ/manage.py collectstatic --noinput

echo "Creating superuser..."
python OJ/manage.py shell << EOF
from django.contrib.auth import get_user_model
from accounts.models import UserExtension
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
    UserExtension.objects.create(user=user)
    print("Admin user and extension created.")
else:
    print("Admin user already exists.")
EOF

echo "Seeding default problems..."
python OJ/manage.py shell < OJ/seed.py


# Only suitable for developement
# python OJ/manage.py runserver 0.0.0.0:8000

echo "Starting Uvicorn server..."
cd OJ && uvicorn OJ.asgi:application --host 0.0.0.0 --port 8000



