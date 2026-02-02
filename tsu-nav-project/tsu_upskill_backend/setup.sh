#!/bin/bash
# Setup script for TSU UPSKILL Backend

echo "🚀 TSU UPSKILL Backend Setup"
echo "============================"

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "✅ Virtual environment created"

# Install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📄 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your configuration"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
echo "Creating admin user: 6820310216@tsu.ac.th"
python manage.py shell << END
from apps.users.models import CustomUser
if not CustomUser.objects.filter(student_id='6820310216').exists():
    user = CustomUser.objects.create_superuser(
        student_id='6820310216',
        email='6820310216@tsu.ac.th',
        password='James@ninjadam9',
        username='admin_tsu'
    )
    user.is_email_verified = True
    user.role = 'admin'
    user.save()
    print("✅ Admin user created successfully")
else:
    print("⚠️  Admin user already exists")
END

# Create sample location categories
echo "📍 Creating sample location categories..."
python manage.py shell << END
from apps.locations.models import LocationCategory

categories = [
    ('Building', 'University Buildings', 'fa-building'),
    ('Classroom', 'Classrooms and Lecture Halls', 'fa-chalkboard'),
    ('Library', 'Libraries', 'fa-book'),
    ('Cafeteria', 'Cafeterias and Dining', 'fa-utensils'),
    ('Parking', 'Parking Areas', 'fa-parking'),
    ('Toilet', 'Restrooms', 'fa-restroom'),
]

for name, desc, icon in categories:
    LocationCategory.objects.get_or_create(
        name=name,
        defaults={'description': desc, 'icon': icon}
    )
    print(f"✅ Created category: {name}")
END

echo ""
echo "✅ Setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000/admin/"
echo "4. Login with: admin_tsu / James@ninjadam9"
echo ""
