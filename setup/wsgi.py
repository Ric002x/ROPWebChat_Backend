"""
WSGI config for setup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

import eventlet
import eventlet.wsgi
import socketio
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

from setup.socket import socket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

application = StaticFilesHandler(get_wsgi_application())
application = socketio.WSGIApp(socket, application)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
