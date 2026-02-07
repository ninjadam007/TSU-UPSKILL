"""
WSGI config for TSU UPSKILL Backend
"""
import os
from django.core.wsgi import get_wsgi_application

# 1. กำหนดค่าสภาพแวดล้อมให้ชี้ไปที่ไฟล์ settings.py หลักที่เราเพิ่งแก้กันไป
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. สร้างตัวแปร application เพื่อให้ Web Server (เช่น gunicorn) เรียกใช้งาน
application = get_wsgi_application()
