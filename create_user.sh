#!/bin/bash
# create_user.sh

echo "Starting user creation script..."

# Check if the user already exists
if ! python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='user_test').exists()" > /dev/null; then
    echo "Creating regular user..."
    
    # Create a normal user (not a superuser)
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('test', 'user@test.com', 'password')"
    
    if [ $? -eq 0 ]; then
        echo "Regular user created successfully."
    else
        echo "Error creating user."
    fi
else
    echo "User already exists."
fi

echo "User creation script completed."
