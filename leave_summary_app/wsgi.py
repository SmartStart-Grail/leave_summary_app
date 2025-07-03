"""
WSGI config for leave_summary_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'leave_summary_app.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

print("Using settings module:", settings_module)

application = get_wsgi_application()