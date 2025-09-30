import os
from .wsgi import *

# This file contains the WSGI configuration required to serve up your
# web application at Vercel.
# It works by setting the variable 'application' to a WSGI handler of some
# description.

# To use this feature, we need to set this application variable to our WSGI handler.
# The default Django application is the 'application' variable in your project's wsgi.py

# Path to Django application
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from djangoproj.wsgi import application

# Vercel expects the WSGI application to be called 'app'
app = application