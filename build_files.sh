#!/bin/bash

# Build the project
echo "Building the project..."

# Install Python dependencies
pip install -r requirements.txt

# Make migrations
python server/manage.py makemigrations --noinput
python server/manage.py migrate --noinput

# Collect static files
python server/manage.py collectstatic --noinput --clear