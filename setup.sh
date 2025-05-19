#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Task Manager Setup...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}MySQL is not installed. Please install MySQL 5.7 or higher.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${GREEN}Installing requirements...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${GREEN}Creating .env file...${NC}"
    cat > .env << EOL
DEBUG=True
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
DB_NAME=taskmanager
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
EOL
    echo -e "${GREEN}Please update the .env file with your database credentials.${NC}"
fi

# Create database if it doesn't exist
echo -e "${GREEN}Setting up database...${NC}"
mysql -u root -e "CREATE DATABASE IF NOT EXISTS taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migrations
echo -e "${GREEN}Running migrations...${NC}"
python manage.py makemigrations
python manage.py migrate

# Create static and media directories if they don't exist
echo -e "${GREEN}Setting up static and media directories...${NC}"
mkdir -p static
mkdir -p media
mkdir -p staticfiles

# Collect static files
echo -e "${GREEN}Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo -e "${GREEN}Would you like to create a superuser? (y/n)${NC}"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}To start the development server, run:${NC}"
echo -e "source venv/bin/activate"
echo -e "python manage.py runserver" 