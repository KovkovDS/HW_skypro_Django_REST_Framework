"""
ASGI config for HW_skypro_Django_REST_Framework project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HW_skypro_Django_REST_Framework.settings')

application = get_asgi_application()
