from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminDashboardViewSet, AnnouncementViewSet

# ใช้ Router สำหรับจัดการ ViewSet
router = DefaultRouter()

# เส้นทางหลักสำหรับดูสถิติและภาพรวม (Dashboard)
router.register(r'dashboard', AdminDashboardViewSet, basename='admin-dashboard')

# เส้นทางสำหรับจัดการประกาศข่าวสาร (Announcements)
router.register(r'announcements', AnnouncementViewSet, basename='admin-announcements')

urlpatterns = [
    # เชื่อมต่อ router ทั้งหมดเข้ากับแอป
    path('', include(router.urls)),
]
