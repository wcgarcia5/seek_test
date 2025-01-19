#!/bin/bash

# Define the username, email, and password for the user
USERNAME="seek_test"
EMAIL="seek_test@example.com"
PASSWORD="seek_password"

# Create the user if it doesn't already exist
echo "Creating user $USERNAME if it doesn't exist..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username="$USERNAME").exists():
    User.objects.create_user(username="$USERNAME", email="$EMAIL", password="$PASSWORD"
