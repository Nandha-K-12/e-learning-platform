#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create or update superuser on deploy
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
u, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
u.set_password('AdminPass123!')
u.is_superuser = True
u.is_staff = True
u.is_active = True
u.save()
print('Superuser admin ready')
"
