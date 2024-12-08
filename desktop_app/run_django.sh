#!/bin/bash

# Set environment variable for Python (you can customize this based on your environment)
export PYTHONPATH=$(pwd)

# Check if virtualenv exists, if not create it
if [ ! -d "myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Run Django development server
echo "Starting Django server..."
python manage.py runserver
