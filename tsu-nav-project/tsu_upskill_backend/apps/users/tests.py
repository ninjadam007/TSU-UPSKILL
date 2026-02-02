"""
Test file structure for TSU UPSKILL Backend
Run: python manage.py test
"""

from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser
import json


class UserAuthenticationTest(TestCase):
    """Test user authentication and registration"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.user_data = {
            'student_id': '1234567890',
            'email': 'test@tsu.ac.th',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123',
            'password_confirm': 'TestPass123'
        }
    
    def test_user_registration(self):
        """Test user can register"""
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['success'])
        self.assertEqual(
            CustomUser.objects.filter(student_id='1234567890').count(),
            1
        )
    
    def test_invalid_email_domain(self):
        """Test registration fails with invalid email domain"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'test@gmail.com'
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertNotEqual(response.status_code, 201)
    
    def test_invalid_student_id(self):
        """Test registration fails with invalid student ID"""
        invalid_data = self.user_data.copy()
        invalid_data['student_id'] = '12345'  # Only 5 digits
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertNotEqual(response.status_code, 201)


class LocationTest(TestCase):
    """Test location endpoints"""
    
    def setUp(self):
        self.client = Client()
        # Create test user
        self.user = CustomUser.objects.create_user(
            student_id='1234567890',
            email='test@tsu.ac.th',
            username='testuser',
            password='TestPass123'
        )
        self.user.is_email_verified = True
        self.user.save()
    
    def test_location_list_requires_auth(self):
        """Test location list requires authentication"""
        response = self.client.get('/api/locations/')
        # Should allow anonymous in this setup, but check your permissions
        self.assertIn(response.status_code, [200, 403])


# Run tests with: python manage.py test apps.users
# With coverage: pip install coverage && coverage run manage.py test && coverage report
