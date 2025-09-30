#!/bin/bash

# Build the project
echo "Building the project..."

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Make migrations
cd server
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# Collect static files
python3 manage.py collectstatic --noinput --clear