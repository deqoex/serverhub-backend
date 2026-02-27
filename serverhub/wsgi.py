"""
WSGI config for serverhub project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serverhub.settings')
application = get_wsgi_application()
