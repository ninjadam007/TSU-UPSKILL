from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, PendingAdminQuestionViewSet

# สร้าง Router สำหรับจัดการเส้นทางอัตโนมัติ
router = DefaultRouter()

# เส้นทางสำหรับนิสิตใช้งานแชท (Sessions & Messages)
router.register(r'sessions', ChatSessionViewSet, basename='chat-session')

# เส้นทางสำหรับแอดมินจัดการคำถามที่ค้างอยู่
router.register(r'pending-questions', PendingAdminQuestionViewSet, basename='pending-question')

urlpatterns = [
    # รวมเส้นทางทั้งหมดเข้าด้วยกัน
    path('', include(router.urls)),
]
