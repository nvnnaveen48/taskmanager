# Task Management System

A Django-based task management system that allows administrators to assign and track tasks for users. Built with Django and Bootstrap for a modern, responsive interface.

## Features

- User Management:
  - Admin can create and manage users
  - User authentication and authorization
  - Optional email field for users

- Task Management:
  - Create and assign tasks to users
  - Task status tracking (Pending, In Progress, Done)
  - Support for CSV data and image attachments
  - Real-time status updates
  - Task notifications

- Admin Features:
  - Dashboard with task statistics
  - User management interface
  - Task monitoring and management
  - Real-time updates

## Technology Stack

- Python 3.13+
- Django 5.2.1
- Bootstrap 5.3
- jQuery 3.6
- Font Awesome 6.0

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/task-management.git
cd task-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root and add:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

## Production Deployment

1. Set up your production server (e.g., Ubuntu with Nginx and Gunicorn)
2. Configure your web server to serve static and media files
3. Set up SSL certificate for HTTPS
4. Configure your database (PostgreSQL recommended)
5. Set up environment variables
6. Run migrations and collect static files

## Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start development server: `python manage.py runserver`

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
