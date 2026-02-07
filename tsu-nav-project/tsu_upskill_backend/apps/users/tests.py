"""
Test file structure for TSU UPSKILL Backend
Run: python manage.py test apps.users
"""

from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import CustomUser
import json

class UserAuthenticationTest(TestCase):
    """ทดสอบระบบสมัครสมาชิกและเข้าสู่ระบบ"""
    
    def setUp(self):
        self.client = Client()
        # ใช้ชื่อ URL ที่ตั้งไว้ใน urls.py (ถ้าเปลี่ยนชื่อให้แก้ตรงนี้ครับ)
        self.register_url = reverse('user-register') 
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
        """ทดสอบ: นิสิตต้องสมัครสมาชิกได้สำเร็จด้วยข้อมูลที่ถูกต้อง"""
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        # เช็คว่า success: True ถูกส่งกลับมาไหม
        self.assertTrue(response.json().get('success', False))
        self.assertEqual(CustomUser.objects.filter(student_id='1234567890').count(), 1)
    
    def test_invalid_email_domain(self):
        """ทดสอบ: ต้องสมัครไม่ผ่านถ้าไม่ใช่อีเมล @tsu.ac.th"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'test@gmail.com'
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400) # เปลี่ยนเป็น 400 Bad Request
    
    def test_invalid_student_id(self):
        """ทดสอบ: ต้องสมัครไม่ผ่านถ้ารหัสนิสิตไม่ครบ 10 หลัก"""
        invalid_data = self.user_data.copy()
        invalid_data['student_id'] = '12345'
        
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

class LocationTest(TestCase):
    """ทดสอบการเข้าถึงข้อมูลสถานที่"""
    
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            student_id='1234567890',
            email='test@tsu.ac.th',
            username='testuser',
            password='TestPass123',
            is_email_verified=True # สมมติว่ายืนยันอีเมลแล้ว
        )
    
    def test_location_list_permissions(self):
        """ทดสอบ: ตรวจสอบสิทธิ์การเข้าถึง API สถานที่"""
        response = self.client.get('/api/locations/locations/')
        # เนื่องจากเราตั้งใน views.py ให้เป็น AllowAny ดังนั้นต้องได้ 200 OK
        self.assertEqual(response.status_code, 200)

# เคล็ดลับ: ใช้ 'python manage.py test --parallel' เพื่อรันเทสต์ให้เร็วขึ้นครับพี่!
