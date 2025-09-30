import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')

# Import Django WSGI application
import django
django.setup()

from djangoproj.wsgi import application

# Vercel expects the WSGI application to be called 'app'
app = application