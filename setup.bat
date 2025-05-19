@echo off
echo Starting Task Manager Setup...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if MySQL is installed
mysql --version >nul 2>&1
if errorlevel 1 (
    echo MySQL is not installed. Please install MySQL 5.7 or higher.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo DEBUG=True
        echo SECRET_KEY=%RANDOM%%RANDOM%%RANDOM%%RANDOM%
        echo DB_NAME=taskmanager
        echo DB_USER=root
        echo DB_PASSWORD=
        echo DB_HOST=localhost
        echo DB_PORT=3306
    ) > .env
    echo Please update the .env file with your database credentials.
)

REM Create database if it doesn't exist
echo Setting up database...
mysql -u root -e "CREATE DATABASE IF NOT EXISTS taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create static and media directories if they don't exist
echo Setting up static and media directories...
if not exist static mkdir static
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Create superuser if requested
set /p create_superuser=Would you like to create a superuser? (y/n): 
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo Setup completed successfully!
echo To start the development server, run:
echo venv\Scripts\activate.bat
echo python manage.py runserver

pause 