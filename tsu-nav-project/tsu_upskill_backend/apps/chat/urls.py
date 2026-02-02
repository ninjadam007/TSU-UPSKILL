from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, PendingAdminQuestionViewSet

router = DefaultRouter()
router.register(r'chat/sessions', ChatSessionViewSet, basename='chat-session')
router.register(r'admin/pending-questions', PendingAdminQuestionViewSet, basename='pending-question')

urlpatterns = router.urls
