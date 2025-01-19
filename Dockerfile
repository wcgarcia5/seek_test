FROM python:3.12-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# Set the working directory for the application
WORKDIR /app

# Copy only the dependencies file (requirements.txt) to the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . /app/

# Copy the script to create a user into the container
COPY create_user.sh /app/
RUN chmod +x /app/create_user.sh

# Set environment variable to prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Run migrations and create the user, then start the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]