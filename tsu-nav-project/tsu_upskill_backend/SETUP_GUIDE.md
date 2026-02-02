# TSU UPSKILL Backend - Quick Start Guide

## 🎯 First Time Setup (Windows)

### Step 1: Install PostgreSQL
1. Download from https://www.postgresql.org/download/
2. Install and remember the password
3. Verify installation: Open PostgreSQL Shell and run `\version`

### Step 2: Install Redis (Optional but Recommended)
1. Download from https://github.com/microsoftarchive/redis/releases
2. Install and start Redis

### Step 3: Setup Python Environment

```powershell
# Navigate to project folder
cd c:\Users\dogga\Downloads\tsu-nav-project\tsu_upskill_backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

```powershell
# Copy the example file
copy .env.example .env

# Edit .env with your editor (Replace values)
notepad .env
```

**Important settings to update in .env:**
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_PASSWORD=your_postgres_password
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Step 5: Initialize Database

```powershell
# Create migrations (if needed)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Follow prompts (Student ID: 6820310216, Email: 6820310216@tsu.ac.th)
```

### Step 6: Run Server

```powershell
# Start development server
python manage.py runserver

# Server should be at: http://localhost:8000
# Admin panel at: http://localhost:8000/admin/
```

---

## 🐳 Using Docker (Easier Alternative)

```powershell
# Install Docker Desktop from https://www.docker.com/products/docker-desktop

# Start containers
docker-compose up

# Server at: http://localhost:8000
# Database ready in PostgreSQL container
# Redis ready for Celery
```

---

## 📝 Configuration Details

### Database Setup
```
Default PostgreSQL:
- Host: localhost
- Port: 5432
- Database: tsu_upskill
- User: postgres
- Password: (set during PostgreSQL installation)
```

### Gemini API
1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Paste in `.env` as `GEMINI_API_KEY`

### Email Setup (Gmail Example)
1. Enable 2FA on Gmail
2. Create App Password: https://myaccount.google.com/apppasswords
3. Use app password in `.env`

---

## 🧪 Testing the API

### Using cURL (Command Line)

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "1234567890",
    "email": "test@tsu.ac.th",
    "username": "testuser",
    "password": "TestPass123",
    "password_confirm": "TestPass123"
  }'

# Verify Email (use token from email)
curl -X POST http://localhost:8000/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{"token": "verification_token"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "1234567890",
    "password": "TestPass123"
  }'

# Get Locations (with token)
curl -X GET http://localhost:8000/api/locations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Postman (GUI)
1. Download Postman: https://www.postman.com/downloads/
2. Import API collection or create requests manually
3. See API_DOCUMENTATION.md for all endpoints

### Using Python
```python
import requests

# Register
response = requests.post('http://localhost:8000/api/auth/register/', json={
    'student_id': '1234567890',
    'email': 'test@tsu.ac.th',
    'username': 'testuser',
    'password': 'TestPass123',
    'password_confirm': 'TestPass123'
})
print(response.json())

# Login
response = requests.post('http://localhost:8000/api/auth/login/', json={
    'student_id': '1234567890',
    'password': 'TestPass123'
})
token = response.json()['access']

# Use token
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/locations/', headers=headers)
print(response.json())
```

---

## 🔧 Common Issues

### Error: "No module named 'django'"
```powershell
# Activate virtual environment
venv\Scripts\activate
# Then install requirements
pip install -r requirements.txt
```

### Error: "PSYCOPG2 Connection refused"
```powershell
# Make sure PostgreSQL is running
# Windows: Services app > PostgreSQL service > Start
```

### Error: "GEMINI_API_KEY not set"
1. Get API key from https://makersuite.google.com/app/apikey
2. Add to .env: `GEMINI_API_KEY=your_key`
3. Restart server

### Email not sending
1. Enable "Less secure apps" if using Gmail
2. OR use App Password (recommended)
3. Check .env SMTP settings

---

## 📚 Useful Commands

```powershell
# Create app migrations
python manage.py makemigrations apps.users

# See pending migrations
python manage.py showmigrations

# Revert last migration
python manage.py migrate apps.users zero

# Clear all data (careful!)
python manage.py flush

# Create sample data
python manage.py shell
>>> from apps.locations.models import LocationCategory
>>> LocationCategory.objects.create(name="Building", icon="fa-building")

# Export data
python manage.py dumpdata > backup.json

# Import data
python manage.py loaddata backup.json

# Check settings
python manage.py diffsettings

# Run specific tests
python manage.py test apps.users.tests

# Collect static files
python manage.py collectstatic --noinput
```

---

## 🚀 Deployment to Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://render.com
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repo
   - Choose branch: `main`

3. **Configure**
   - Runtime: `Python 3.11`
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2`

4. **Environment Variables**
   - Add all from `.env` (except DEBUG=True, use DEBUG=False)
   - `SECRET_KEY`: Generate strong key
   - Database credentials: Auto-configured if using Render Postgres

---

## 📞 Support

- Admin Email: 6820310216@tsu.ac.th
- Issues? Check logs: `logs/django.log`
- Test Django Shell: `python manage.py shell`

---

## ✅ Next Steps After Setup

1. ✅ Customize location data in Django Admin
2. ✅ Train Gemini AI with campus-specific info
3. ✅ Setup Frontend (React/Vue)
4. ✅ Configure production environment
5. ✅ Setup monitoring and logging
6. ✅ Create backup strategy for database
