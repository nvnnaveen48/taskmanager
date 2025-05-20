#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Define project directory
PROJECT_DIR="/home/myntra/proj"
cd "$PROJECT_DIR"

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

# Create fresh virtual environment
echo "Creating new virtual environment..."
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Ensure pip is installed and up to date
echo "Setting up pip..."
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create necessary directories if they don't exist
echo "Setting up directories..."
mkdir -p staticfiles_proj
mkdir -p media
mkdir -p logs

# Set proper permissions
echo "Setting permissions..."
chmod -R 755 staticfiles_proj
chmod -R 755 media
chmod -R 755 logs

# Restart Gunicorn (if using systemd)
echo "Restarting Gunicorn..."
if systemctl is-active --quiet gunicorn; then
    sudo systemctl restart gunicorn
else
    echo "Warning: Gunicorn service not active"
    sudo systemctl start gunicorn
fi

# Restart Nginx
echo "Restarting Nginx..."
if systemctl is-active --quiet nginx; then
    sudo systemctl restart nginx
else
    echo "Warning: Nginx service not active"
    sudo systemctl start nginx
fi

echo "Deployment completed!" 