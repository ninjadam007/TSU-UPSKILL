# TSU UPSKILL Backend

Django backend for TSU UPSKILL campus navigation and AI chatbot system.

## Features

- ✅ User Authentication with JWT (Student ID + @tsu.ac.th email)
- ✅ Email Verification System
- ✅ Google Gemini AI Chatbot Integration
- ✅ Admin Panel for Question Management
- ✅ Location/Pin Management with GPS coordinates
- ✅ Bookmark/Favorites System
- ✅ Chat History & Session Management
- ✅ Comprehensive Security (CSRF, SQL Injection prevention, XSS protection)
- ✅ Rate Limiting
- ✅ Django Admin Panel (built-in)
- ✅ RESTful API with DRF

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **AI**: Google Gemini API
- **Authentication**: JWT (PyJWT)
- **Task Queue**: Celery + Redis
- **Email**: SMTP
- **Deployment**: Render.com compatible

## Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- Redis (optional, for Celery)

### Setup

1. **Clone and enter directory**
```bash
cd tsu_upskill_backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Create database**
```bash
python manage.py migrate
```

6. **Create superuser (admin)**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py loaddata initial_data  # if available
```

## Running the Project

### Development
```bash
python manage.py runserver
```

### With Celery (for background tasks)
```bash
celery -A config worker -l info
celery -A config beat -l info  # for scheduled tasks
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/verify-email/` - Verify email with token
- `POST /api/auth/login/` - Login and get JWT token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/update-profile/` - Update profile
- `POST /api/auth/change-password/` - Change password

### Locations
- `GET /api/locations/` - List all locations
- `GET /api/locations/{id}/` - Get location details
- `POST /api/locations/{id}/bookmark/` - Bookmark location
- `DELETE /api/locations/{id}/unbookmark/` - Remove bookmark
- `GET /api/locations/my-bookmarks/` - Get user's bookmarks
- `GET /api/location-categories/` - Get location categories

### Chat (AI & Admin)
- `POST /api/chat/sessions/` - Create new chat session
- `GET /api/chat/sessions/` - List user's chat sessions
- `POST /api/chat/sessions/{id}/send-message/` - Send message to AI
- `GET /api/chat/sessions/{id}/messages/` - Get session messages
- `GET /api/admin/pending-questions/` - List pending questions (admin only)
- `POST /api/admin/pending-questions/{id}/respond/` - Admin responds (admin only)

### Admin Dashboard
- `GET /api/admin/dashboard/` - Get dashboard stats
- `GET /api/admin/dashboard/users/` - List all users
- `GET /api/admin/dashboard/pending-questions/` - Pending questions
- `POST /api/admin/dashboard/respond-to-question/` - Respond to question
- `GET /api/admin/dashboard/activity-log/` - Recent activity log

## Django Admin Panel

Access at `/admin/`

Manage:
- Users (Student ID, Email, Verification status, Role)
- Locations (Buildings, Rooms, GPS coordinates)
- Chat Sessions & Messages
- Pending Admin Questions

## Security Features

- ✅ JWT Token Authentication
- ✅ Email Domain Validation (@tsu.ac.th)
- ✅ CSRF Protection (middleware)
- ✅ SQL Injection Prevention (ORM)
- ✅ XSS Protection (middleware)
- ✅ Password Hashing (Django built-in)
- ✅ Rate Limiting (DRF throttling)
- ✅ CORS Configuration
- ✅ HTTPS Required in Production
- ✅ Environment variables for secrets
- ✅ Logging & Monitoring

## Admin Credentials

- **Email**: 6820310216@tsu.ac.th
- **Password**: James@ninjadam9

(Change these in production!)

## Deployment to Render

1. Create GitHub repository
2. Connect to Render.com
3. Set environment variables in Render dashboard
4. Deploy

Key settings for Render:
```
Start Command: gunicorn config.wsgi:application
```

## Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Revert migrations
python manage.py migrate app_name zero
```

## Troubleshooting

### PostgreSQL Connection Error
- Check DB credentials in .env
- Ensure PostgreSQL is running
- Verify network connectivity

### Gemini API Error
- Add GEMINI_API_KEY to .env
- Check API quota and billing

### Email Not Sending
- Configure SMTP in .env
- Check firewall/network settings
- Verify sender email

## Development Notes

- Keep .env in .gitignore
- Always run migrations before pushing
- Write tests for new features
- Follow PEP 8 style guide
- Document API changes in README

## Support

For issues or questions, contact the admin at 6820310216@tsu.ac.th
