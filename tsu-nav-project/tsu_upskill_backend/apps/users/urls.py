from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# ใช้ DefaultRouter จัดการเส้นทางอัตโนมัติ
router = DefaultRouter()

# ลงทะเบียน UserViewSet ไว้ภายใต้ prefix 'auth'
# จะได้ URL เช่น: /api/users/auth/register/ และ /api/users/auth/login/
router.register(r'auth', UserViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
