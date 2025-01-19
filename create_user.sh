#!/bin/bash

# Define the username, email, and password for the user
USERNAME="seek_test"
EMAIL="seek_test@example.com"
PASSWORD="seek_password"

echo "Checking if the user '$USERNAME' exists..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
try:
    if not User.objects.filter(username="$USERNAME").exists():
        User.objects.create_user(username="$USERNAME", email="$EMAIL", password="$PASSWORD")
        print("User '$USERNAME' created successfully.")
    else:
        print("User '$USERNAME' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")
EOF
