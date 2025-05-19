# Task Manager

A Django-based task management system with user management, CSV/image upload, and real-time notifications.

## Features

- User authentication and authorization
- Admin and user dashboards
- CSV and image upload functionality
- Real-time task updates
- Task assignment and tracking
- Notification system
- Responsive design

## Prerequisites

- Python 3.8+
- MySQL 5.7+
- Virtual environment (recommended)

## Quick Setup

### For Linux/Mac Users:
```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

### For Windows Users:
```bash
# Run the setup script
setup.bat
```

The setup scripts will:
1. Check for required dependencies
2. Create a virtual environment
3. Install required packages
4. Set up the database
5. Create necessary directories
6. Run migrations
7. Collect static files
8. Optionally create a superuser

## Manual Installation

If you prefer to set up manually, follow these steps:

1. Clone the repository:
```bash
git clone <repository-url>
cd taskmanager
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=taskmanager
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```

5. Set up the database:
```bash
mysql -u root -p
CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
```
taskmanager/
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── forms.py         # Form definitions
│   └── admin.py         # Admin configurations
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   └── core/            # App-specific templates
├── static/             # Static files
│   ├── css/            # CSS files
│   ├── js/             # JavaScript files
│   └── images/         # Image files
├── media/              # User-uploaded files
├── manage.py           # Django management script
├── setup.sh           # Linux/Mac setup script
├── setup.bat          # Windows setup script
└── requirements.txt    # Project dependencies
```

## Development Guidelines

1. Code Style:
   - Follow PEP 8 guidelines
   - Use meaningful variable names
   - Add comments for complex logic

2. Git Workflow:
   - Create feature branches
   - Write descriptive commit messages
   - Keep commits focused and atomic

3. Testing:
   - Write tests for new features
   - Run tests before committing
   - Maintain test coverage

## Deployment

1. Update settings:
   - Set DEBUG=False
   - Configure ALLOWED_HOSTS
   - Set up proper SECRET_KEY

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Set up a production database:
   - Use a production-grade database
   - Configure proper backups
   - Set up monitoring

4. Configure web server:
   - Set up Nginx/Apache
   - Configure SSL
   - Set up proper caching

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 